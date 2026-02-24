"""
Rule 4 – Missing WHERE on large tables

Flags SELECT queries on known large tables that have no WHERE clause.

Example bad query:
    SELECT id, name FROM orders
"""

from sqlglot import exp
from utils import Category
from RuleEngine.base import make_result

ISSUE = "missing_where"
CATEGORY = Category.PERFORMANCE

# Tables considered "large" – in a real system this comes from metadata / stats
LARGE_TABLES = {"orders", "transactions", "events", "logs", "customers"}


def check(ast):
    if ast.find(exp.Where):
        return make_result(False, ISSUE, CATEGORY, "WHERE clause is present.")

    # Collect table names referenced in the query
    tables = {table.name.lower() for table in ast.find_all(exp.Table)}
    flagged = tables & LARGE_TABLES

    if flagged:
        return make_result(
            True,
            ISSUE,
            CATEGORY,
            f"Query reads from large table(s) {flagged} without a WHERE clause. "
            "This may scan millions of rows and hurt performance.",
        )

    return make_result(False, ISSUE, CATEGORY, "No large-table full scan detected.")
