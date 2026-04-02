"""
Base helper shared by all rule implementations.
"""

from config.enums import Category


def make_result(triggered, issue, category, explanation):
    """
    Build a standard rule-result dict.

    Args:
        triggered:   bool – whether the rule fired
        issue:       str  – machine-readable issue key (e.g. "missing_group_by")
        category:    Category enum member
        explanation: str  – human-readable description
    """
    if not isinstance(category, Category):
        raise ValueError(f"category must be a Category enum member. Got: {category}")

    return {
        "triggered": triggered,
        "issue": issue,
        "category": category.value,
        "explanation": explanation,
    }
