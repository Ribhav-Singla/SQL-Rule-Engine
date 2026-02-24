"""
Rule 3 – SELECT * usage

Flags usage of SELECT * which fetches all columns – bad practice in
production queries.

Example bad query:
    SELECT * FROM customers
"""

from sqlglot import exp
from utils import Category
from RuleEngine.base import make_result

ISSUE = "select_star"
CATEGORY = Category.BEST_PRACTICE


def check(ast):
    if list(ast.find_all(exp.Star)):
        return make_result(
            True,
            ISSUE,
            CATEGORY,
            "SELECT * fetches every column from the table. "
            "Specify only the columns you need to improve clarity and performance.",
        )

    return make_result(False, ISSUE, CATEGORY, "No SELECT * detected.")
