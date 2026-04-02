import sqlglot
from sqlglot.errors import ParseError


def normalize_sql(sql, dialect=None):
    """
    Parse and normalize a SQL query string.

    Returns:
        dict with keys: ast, normalized_sql, error
    """
    try:
        ast = sqlglot.parse_one(sql, read=dialect)
        normalized = ast.sql()
        return {
            "ast": ast,
            "normalized_sql": normalized,
            "error": None,
        }
    except ParseError as e:
        return {
            "ast": None,
            "normalized_sql": None,
            "error": str(e),
        }
