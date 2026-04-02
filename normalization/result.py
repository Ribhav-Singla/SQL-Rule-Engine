import json
from decimal import Decimal
from datetime import date, datetime


def _normalize_value(value):
    """Normalize a single cell value for stable comparison."""
    if value is None:
        return None
    if isinstance(value, float):
        return round(value, 6)
    if isinstance(value, Decimal):
        return round(float(value), 6)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return value


def normalize_result(rows):
    """
    Normalize DB query result rows for deterministic comparison.

    Steps:
    1. Lowercase all column names
    2. Round floats to 6 decimal places
    3. Convert Decimal/date/datetime to stable string formats
    4. Sort rows for order-independent comparison
    5. Serialize into a deterministic JSON string

    Returns:
        A deterministic JSON string representation.
    """
    if not rows:
        return json.dumps([])

    normalized = []
    for row in rows:
        normalized_row = {}
        for key, value in row.items():
            normalized_row[key.lower()] = _normalize_value(value)
        normalized.append(normalized_row)

    sorted_rows = sorted(
        normalized,
        key=lambda r: json.dumps(r, sort_keys=True, default=str),
    )
    return json.dumps(sorted_rows, sort_keys=True, default=str)
