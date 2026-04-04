from config.enums import Schema
from normalization.query import normalize_sql
from normalization.result import normalize_result
from hasher.fingerprint import generate_query_fingerprint, generate_sha256_hash
from cache.redis_cache import cache_service
from rules import run_rules
from execution.query_executor import query_executor
from comparison.comparator import hash_and_compare
from feedback.generator import generate_feedback
from database.pool import db_pool


def _get_expected_hash(problem_id: str) -> str | None:
    query = """
        SELECT result_hash
        FROM ecommerce.expected_results
        WHERE problem_id = %s
        LIMIT 1
    """
    with db_pool.get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (problem_id,))
            row = cur.fetchone()
    return row[0] if row else None


def evaluate_query(sql, schema, problem_id: str):
    """
    Full pipeline: evaluate a user's SQL query.

    Args:
        SQL: raw SQL string from the user
        schema: Schema enum member (e.g. Schema.ECOMMERCE)
        problem_id: identifier used to look up the expected hash in the DB

    Returns:
        dict with feedback, cached flag, and full details
    """
    # Step 1: Fetch expected hash from DB
    expected_hash = _get_expected_hash(problem_id)
    if expected_hash is None:
        return {"error": f"Problem '{problem_id}' not found in expected_results."}

    # Step 2: Normalize SQL
    parsed = normalize_sql(sql)
    if parsed["error"]:
        return {"error": f"Parse error: {parsed['error']}"}

    normalized_sql = parsed["normalized_sql"]
    ast = parsed["ast"]

    # Step 3: Generate fingerprint
    fingerprint = generate_query_fingerprint(problem_id, schema, normalized_sql)

    # Step 4: Cache lookup
    try:
        cached = cache_service.get(fingerprint)
        if cached:
            return {
                "cached": True,
                "fingerprint": fingerprint,
                # "feedback" : {},
                **cached,
            }
    except Exception:
        pass  # Cache unavailable — proceed without it

    # Step 5: Cache miss — run rule engine
    rule_results = run_rules(ast)

    # Step 6: Execute query safely
    execution = query_executor.execute_query(normalized_sql, schema)
    if execution["error"]:
        return {"error": f"Execution error: {execution['error']}"}

    # Step 7: Normalize + hash result
    normalized = normalize_result(execution["rows"])
    result_hash = generate_sha256_hash(normalized)

    # Step 8: Compare
    comparison = hash_and_compare(normalized, expected_hash)

    # Step 9: Generate feedback
    feedback = generate_feedback(comparison, rule_results)
    # feedback = {}

    # Step 10: Cache update
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
    except Exception as e:
        print(f"Cache unavailable — skip caching: {type(e).__name__}: {e}")

    return {
        "cached": False,
        "fingerprint": fingerprint,
        "feedback": feedback,
        **cache_entry,
    }
