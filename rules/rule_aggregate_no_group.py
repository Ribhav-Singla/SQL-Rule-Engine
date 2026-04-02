"""
Rule 1 – Aggregate used without GROUP BY

Detects aggregate functions (COUNT, SUM, AVG, MIN, MAX) in the SELECT
list alongside non-aggregated columns, but no GROUP BY clause.

Example bad query:
    SELECT customer_id, COUNT(*) FROM orders
"""

from sqlglot import exp
from config.enums import Category
from rules.base import make_result

ISSUE = "missing_group_by"
CATEGORY = Category.LOGIC


def check(ast):
    # Find all aggregate function calls anywhere in the query
    aggregates = list(ast.find_all(exp.AggFunc))

    if not aggregates:
        return make_result(False, ISSUE, CATEGORY, "No aggregates found.")

    # If a GROUP BY clause exists, the rule passes
    if ast.find(exp.Group):
        return make_result(False, ISSUE, CATEGORY, "GROUP BY is present.")

    # Check for non-aggregate columns mixed in the SELECT list
    select = ast.find(exp.Select)
    if select:
        non_agg_columns = [
            e for e in select.expressions
            if not isinstance(e, exp.AggFunc) and not e.find(exp.AggFunc)
        ]
        if non_agg_columns:
            return make_result(
                True,
                ISSUE,
                CATEGORY,
                "Aggregate function used with non-aggregated columns but no GROUP BY clause. "
                "This will cause an error or unexpected results in most databases.",
            )

    return make_result(
        False, ISSUE, CATEGORY,
        "Aggregate-only SELECT is valid without GROUP BY.",
    )
