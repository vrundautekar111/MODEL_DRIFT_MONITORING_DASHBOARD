
from src.models.evaluate import regression_metrics


def evaluate_labeled_predictions(records):
    if not records:
        return {
            "mae": None,
            "rmse": None,
            "bias": None,
            "rows": 0,
            "status": "waiting_for_actuals",
        }

    metrics = regression_metrics(
        [record["actual_units"] for record in records],
        [record["predicted_units"] for record in records],
    )

    metrics["status"] = "evaluated"

    return metrics
