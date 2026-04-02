import hashlib

from config.enums import Schema


def generate_sha256_hash(text):
    """Generic SHA256 hash for any text input."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def generate_query_fingerprint(problem_id, schema_name, normalized_sql):
    """
    Generate a unique fingerprint for a normalized SQL query.
    Format: problem_id:schema_name:sha256(normalized_sql)
    """
    if not isinstance(schema_name, Schema):
        raise ValueError(f"schema_name must be a Schema enum member. Got: {schema_name}")

    pid = problem_id if problem_id else "global"
    return f"{pid}:{schema_name.value}:{generate_sha256_hash(normalized_sql)}"
