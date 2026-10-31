
import pandas as pd

from src.common.config import DATA_PATH, REFERENCE_PATH
from src.monitoring.data_quality import assess_data_quality
from src.monitoring.data_drift import detect_drift
from src.features.build_features import build_features
from src.models.predict import load_model


def run_monitoring():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Sales data not found: {DATA_PATH}"
        )

    raw = pd.read_csv(DATA_PATH)

    quality = assess_data_quality(raw)
    status = "healthy" if quality["ok"] else "critical"

    drift = []

    if REFERENCE_PATH.exists():
        reference = pd.read_csv(REFERENCE_PATH)
        current = build_features(raw)

        common_columns = [
            column for column in current.columns
            if column in reference.columns
        ]

        reference = reference[common_columns]
        current = current[common_columns]

        drift = detect_drift(reference, current)

    drift_count = sum(
        item["status"] == "drift"
        for item in drift
    )

    warning_count = sum(
        item["status"] == "warning"
        for item in drift
    )

    if quality["ok"]:
        if drift_count >= 3:
            status = "critical"
        elif drift_count > 0 or warning_count > 0:
            status = "warning"

    bundle = load_model()
    predictions = bundle["pipeline"].predict(
        build_features(raw)
    )

    prediction_summary = {
        "count": int(len(predictions)),
        "mean": float(pd.Series(predictions).mean()),
        "median": float(pd.Series(predictions).median()),
        "min": float(pd.Series(predictions).min()),
        "max": float(pd.Series(predictions).max()),
    }

    return {
        "status": status,
        "rows_checked": int(len(raw)),
        "quality": quality,
        "drift": drift,
        "drifted_features": int(drift_count),
        "warning_features": int(warning_count),
        "prediction_distribution": prediction_summary,
        "model_metrics": bundle.get("metrics", {}),
        "recommendation": (
            "Review drift and actual forecast errors. "
            "Retraining requires candidate evaluation."
        ),
    }
