from config.enums import Schema
from normalization.query import normalize_sql
from normalization.result import normalize_result
from hasher.fingerprint import generate_query_fingerprint, generate_sha256_hash
from cache.redis_cache import cache_service
from rules import run_rules
from execution.query_executor import query_executor
from comparison.comparator import hash_and_compare
from feedback.generator import generate_feedback


def evaluate_query(sql, schema, expected_hash, problem_id=None):
    """
    Full pipeline: evaluate a user's SQL query.

    Args:
        sql: raw SQL string from the user
        schema: Schema enum member (e.g. Schema.ECOMMERCE)
        expected_hash: pre-computed SHA256 of the expected normalized result

    Returns:
        dict with feedback, cached flag, and full details
    """
    # Step 1: Normalize SQL
    parsed = normalize_sql(sql)
    if parsed["error"]:
        return {"error": f"Parse error: {parsed['error']}"}

    normalized_sql = parsed["normalized_sql"]
    ast = parsed["ast"]

    # Step 2: Generate fingerprint
    fingerprint = generate_query_fingerprint(problem_id, schema, normalized_sql)

    # Step 3: Cache lookup
    try:
        cached = cache_service.get(fingerprint)
        if cached:
            return {
                "cached": True,
                "fingerprint": fingerprint,
                **cached,
            }
    except Exception:
        pass  # Cache unavailable — proceed without it

    # Step 4: Cache miss — run rule engine
    rule_results = run_rules(ast)

    # Step 5: Execute query safely
    execution = query_executor.execute_query(normalized_sql, schema)
    if execution["error"]:
        return {"error": f"Execution error: {execution['error']}"}

    # Step 6: Normalize + hash result
    normalized = normalize_result(execution["rows"])
    result_hash = generate_sha256_hash(normalized)

    # Step 7: Compare
    comparison = hash_and_compare(normalized, expected_hash)

    # Step 8: Generate feedback
    feedback = generate_feedback(comparison, rule_results)

    # Step 9: Cache update
    columns = execution.get("columns", [])
    rows = execution.get("rows", [])
    runtime_status = "success" if not execution["error"] else "error"

    cache_entry = {
        "result_hash": result_hash,
        "rule_results": rule_results,
        "correct": comparison["correct"],
        "question_attempt": {
            "problem_id": problem_id,
            "raw_sql": sql,
            "normalized_sql": normalized_sql,
            "runtime_status": runtime_status,
            "preview_columns": columns,
            "preview_rows": rows[:20],
            "row_count": len(rows),
        },
    }
    try:
        cache_service.set(fingerprint, cache_entry)
    except Exception:
        pass  # Cache unavailable — skip caching

    return {
        "cached": False,
        "fingerprint": fingerprint,
        "feedback": feedback,
        **cache_entry,
    }
