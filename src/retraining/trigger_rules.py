
def evaluate_retraining_trigger(
    monitoring_result,
    baseline_mae=None,
    current_mae=None,
    consecutive_windows=1,
):
    reasons = []

    if monitoring_result.get("status") == "critical":
        reasons.append(
            "Critical data-quality or feature-drift signals"
        )

    if (
        baseline_mae is not None
        and current_mae is not None
        and baseline_mae > 0
        and current_mae > baseline_mae * 1.30
        and consecutive_windows >= 3
    ):
        reasons.append(
            "MAE is more than 30% above baseline "
            "for at least three consecutive windows"
        )

    if reasons:
        return {
            "recommended": True,
            "severity": "high",
            "reasons": reasons,
            "action": (
                "Train and evaluate a candidate model. "
                "Do not automatically promote it."
            ),
        }

    if monitoring_result.get("status") == "warning":
        return {
            "recommended": False,
            "severity": "medium",
            "reasons": [
                "Investigate drift and wait for actual labels"
            ],
            "action": "Continue monitoring.",
        }

    return {
        "recommended": False,
        "severity": "low",
        "reasons": [],
        "action": "Continue normal monitoring.",
    }
