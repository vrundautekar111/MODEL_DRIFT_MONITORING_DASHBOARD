
from src.models.evaluate import regression_metrics


def test_regression_metrics():
    result = regression_metrics(
        [10, 20],
        [12, 18],
    )

    assert result["mae"] == 2
    assert result["bias"] == 0
