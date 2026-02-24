import sqlglot
from sqlglot.errors import ParseError
from fingerprint import generate_fingerprint
from utils import Schema
from Execution import _queryExecutor
from RuleEngine import run_rules

def parse_and_normalize(sql, dialect=None):
    try:
        ast = sqlglot.parse_one(sql, read=dialect)
        normalized = ast.sql()
        return {
            "ast": ast,
            "normalized_sql": normalized,
            "error": None
        }
    except ParseError as e:
        return {
            "ast": None,
            "normalized_sql": None,
            "error": str(e)
        }

query = "select * from customers"
result = parse_and_normalize(query)
print("Normalized SQL:", result["normalized_sql"])

if result["normalized_sql"]:
    fingerprint = generate_fingerprint(Schema.ECOMMERCE, result["normalized_sql"])
    print("Fingerprint:", fingerprint)

    # --- Rule Engine ---
    issues = run_rules(result["ast"])
    if issues:
        print(f"\n⚠ Rule Engine found {len(issues)} issue(s):")
        for issue in issues:
            print(f"  - [{issue['category']}] {issue['issue']}: {issue['explanation']}")
    else:
        print("\n✓ Rule Engine: no issues found.")

    execution_result = _queryExecutor.execute_query(query, Schema.ECOMMERCE)
    print("Execution Result:", execution_result)

