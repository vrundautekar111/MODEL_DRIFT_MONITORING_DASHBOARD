
from pathlib import Path

import joblib
import pandas as pd

from src.common.config import MODEL_PATH
from src.features.build_features import build_features


def load_model(path=None):
    path = Path(path) if path else MODEL_PATH

    if not path.exists():
        raise FileNotFoundError(
            f"Model not found at {path}. "
            "Run python scripts/train_model.py first."
        )

    return joblib.load(path)


def predict_one(payload, model_bundle=None):
    bundle = model_bundle or load_model()

    frame = pd.DataFrame([payload])
    features = build_features(frame)

    prediction = float(
        bundle["pipeline"].predict(features)[0]
    )

    return max(0.0, prediction)
