
import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
)


def regression_metrics(actual, predicted):
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)

    if len(actual) == 0:
        return {
            "mae": None,
            "rmse": None,
            "bias": None,
            "rows": 0,
        }

    return {
        "mae": float(
            mean_absolute_error(actual, predicted)
        ),
        "rmse": float(
            mean_squared_error(actual, predicted) ** 0.5
        ),
        "bias": float(
            np.mean(predicted - actual)
        ),
        "rows": int(len(actual)),
    }
