import hashlib
from enum import Enum
from utils import Schema

def generate_md5_hash(text):
    encoded_text = text.encode('utf-8')
    md5_hash = hashlib.md5()
    md5_hash.update(encoded_text)
    return md5_hash.hexdigest()

def generate_fingerprint(schema_name, normalized_sql):
    if not isinstance(schema_name, Schema):
        raise ValueError(f"schema_name must be a Schema enum member. Got: {schema_name}")
    
    fingerprint = f"{schema_name.value}:{generate_md5_hash(normalized_sql)}"
    return fingerprint