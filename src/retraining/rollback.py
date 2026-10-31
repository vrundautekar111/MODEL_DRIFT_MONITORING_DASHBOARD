
def rollback_plan(previous_model_version, reason):
    return {
        "action": "manual_rollback_required",
        "target_version": previous_model_version,
        "reason": reason,
        "note": (
            "Verify model health and predictions "
            "before switching production traffic."
        ),
    }
