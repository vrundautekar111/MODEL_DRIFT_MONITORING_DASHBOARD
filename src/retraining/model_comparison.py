
def compare_metrics(
    current_metrics,
    candidate_metrics,
    max_mae_regression=0.02,
):
    current_mae = current_metrics.get("mae")
    candidate_mae = candidate_metrics.get("mae")

    if current_mae is None or candidate_mae is None:
        return {
            "eligible": False,
            "reason": "Missing MAE metric",
        }

    eligible = (
        candidate_mae
        <= current_mae * (1 + max_mae_regression)
    )

    return {
        "eligible": bool(eligible),
        "current_mae": current_mae,
        "candidate_mae": candidate_mae,
        "reason": (
            "Candidate passed MAE gate"
            if eligible
            else "Candidate did not meet MAE gate"
        ),
    }
