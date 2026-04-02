"""
Rule 5 – Incorrect JOIN type (RIGHT JOIN → LEFT JOIN)

Flags RIGHT JOINs which are harder to read. A LEFT JOIN with swapped
table order is usually preferred.

Example bad query:
    SELECT * FROM orders RIGHT JOIN customers ON orders.cid = customers.id
"""

from sqlglot import exp
from config.enums import Category
from rules.base import make_result

ISSUE = "right_join_detected"
CATEGORY = Category.READABILITY


def check(ast):
    for join in ast.find_all(exp.Join):
        kind = str(join.args.get("kind") or "").upper()
        if kind == "RIGHT":
            return make_result(
                True,
                ISSUE,
                CATEGORY,
                "RIGHT JOIN detected. Consider rewriting as a LEFT JOIN with the "
                "tables swapped for better readability.",
            )

    return make_result(False, ISSUE, CATEGORY, "No RIGHT JOIN detected.")
