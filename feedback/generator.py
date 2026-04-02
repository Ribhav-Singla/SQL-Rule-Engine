def generate_feedback(comparison_result, rule_results):
    """
    Build user-facing feedback from comparison + rule engine output.

    Args:
        comparison_result: dict from comparator (correct, result_hash, expected_hash)
        rule_results: list of triggered rule dicts from run_rules()

    Returns:
        dict with is_correct, score, messages
    """
    messages = []

    # Correctness feedback
    if comparison_result["correct"]:
        messages.append("✅ Your query produces the correct result!")
    else:
        messages.append("❌ Your query result does not match the expected output.")

    # Rule-based feedback
    if rule_results:
        messages.append(f"\n⚠ Rule Engine found {len(rule_results)} issue(s):")
        for issue in rule_results:
            messages.append(f"  - [{issue['category']}] {issue['issue']}: {issue['explanation']}")
    else:
        messages.append("\n✓ Rule Engine: no issues found.")

    # Simple score: correct = 70pts base, minus 10 per rule issue, min 0
    score = 70 if comparison_result["correct"] else 0
    score = max(0, score + (30 if not rule_results else 30 - 10 * len(rule_results)))

    return {
        "is_correct": comparison_result["correct"],
        "score": score,
        "rule_issues": rule_results,
        "messages": messages,
    }
