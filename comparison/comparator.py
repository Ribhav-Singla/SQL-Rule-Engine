from hasher.fingerprint import generate_sha256_hash


def compare_hashes(result_hash, expected_hash):
    """
    Compare the result hash against the expected hash.

    Returns:
        dict with correct (bool) and details
    """
    is_correct = result_hash == expected_hash
    return {
        "correct": is_correct,
        "result_hash": result_hash,
        "expected_hash": expected_hash,
    }


def hash_and_compare(normalized_result, expected_hash):
    """
    Hash the normalized result string and compare with expected.

    Args:
        normalized_result: deterministic JSON string from normalize_result()
        expected_hash: pre-computed SHA256 of expected result

    Returns:
        dict with correct (bool), result_hash, expected_hash
    """
    result_hash = generate_sha256_hash(normalized_result)
    return compare_hashes(result_hash, expected_hash)
