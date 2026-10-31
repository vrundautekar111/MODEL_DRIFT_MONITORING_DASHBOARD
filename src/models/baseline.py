
import numpy as np


def seasonal_naive(values, seasonal_period=7):
    values = np.asarray(values, dtype=float)

    if len(values) < seasonal_period:
        average = (
            float(np.mean(values))
            if len(values)
            else 0.0
        )

        return np.repeat(
            average, seasonal_period
        )

    return values[-seasonal_period:].copy()
