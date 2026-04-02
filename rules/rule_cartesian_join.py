"""
Rule 2 – Cartesian join detection

Detects implicit Cartesian joins – multiple tables in FROM without
a JOIN condition (comma-separated tables with no ON / USING).

Example bad query:
    SELECT * FROM customers, orders
"""

from sqlglot import exp
from config.enums import Category
from rules.base import make_result

ISSUE = "cartesian_join"
CATEGORY = Category.PERFORMANCE


def check(ast):
    from_clause = ast.find(exp.From)
    if not from_clause:
        return make_result(False, ISSUE, CATEGORY, "No FROM clause found.")

    # In sqlglot, comma-joins appear as Join nodes without an ON / USING clause
    for join in ast.find_all(exp.Join):
        has_condition = join.args.get("on") is not None or join.args.get("using") is not None
        if not has_condition:
            kind = str(join.args.get("kind") or "").upper()
            # Explicit CROSS JOIN is intentional – skip it
            if kind != "CROSS":
                return make_result(
                    True,
                    ISSUE,
                    CATEGORY,
                    "Tables are joined without a JOIN condition (implicit Cartesian product). "
                    "This creates a row for every combination and is usually a mistake.",
                )

    return make_result(False, ISSUE, CATEGORY, "No Cartesian join detected.")
