
import numpy as np


def prediction_distribution(
    reference_predictions,
    current_predictions,
):
    reference = np.asarray(
        reference_predictions, dtype=float
    )

    current = np.asarray(
        current_predictions, dtype=float
    )

    def summarize(values):
        if not len(values):
            return {
                "count": 0,
                "mean": None,
                "median": None,
                "std": None,
            }

        return {
            "count": int(len(values)),
            "mean": float(np.mean(values)),
            "median": float(np.median(values)),
            "std": float(np.std(values)),
        }

    return {
        "reference": summarize(reference),
        "current": summarize(current),
    }
