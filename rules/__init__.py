"""
RuleEngine package – auto-registers every rule_*.py module.

Each rule module exposes a `check(ast)` function that returns
a standard result dict via `base.make_result()`.
"""

from rules.rule_aggregate_no_group import check as check_aggregate_no_group
from rules.rule_cartesian_join import check as check_cartesian_join
from rules.rule_select_star import check as check_select_star
from rules.rule_missing_where import check as check_missing_where
from rules.rule_right_join import check as check_right_join

# Ordered list of all rule check functions
ALL_RULES = [
    check_aggregate_no_group,
    check_cartesian_join,
    check_select_star,
    check_missing_where,
    check_right_join,
]


def run_rules(ast):
    """
    Run every registered rule against the parsed AST.
    Returns a list of result dicts (only triggered rules).
    """
    results = []
    for rule_fn in ALL_RULES:
        result = rule_fn(ast)
        if result["triggered"]:
            results.append(result)
    return results
