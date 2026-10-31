
import numpy as np

from src.monitoring.data_drift import psi


def test_psi_is_near_zero_for_same_distribution():
    rng = np.random.default_rng(1)
    values = rng.normal(0, 1, 2000)

    score = psi(values, values.copy())

    assert score is not None
    assert score < 0.05


def test_psi_increases_for_shifted_distribution():
    rng = np.random.default_rng(1)

    reference = rng.normal(0, 1, 2000)
    current = rng.normal(3, 1, 2000)

    assert psi(reference, current) > 0.1
