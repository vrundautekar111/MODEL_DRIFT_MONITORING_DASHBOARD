
from pathlib import Path
import json

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.common.config import MODEL_PATH, REFERENCE_PATH
from src.data.preprocessing import prepare_sales_frame
from src.features.build_features import (
    build_features,
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES,
)


def train_model(data_path=None, model_path=None):
    root = Path(__file__).resolve().parents[2]

    data_path = (
        Path(data_path)
        if data_path
        else root / "data/sample/sales_sample.csv"
    )

    model_path = (
        Path(model_path)
        if model_path
        else MODEL_PATH
    )

    df = prepare_sales_frame(pd.read_csv(data_path))

    if len(df) < 100:
        raise ValueError(
            "At least 100 valid sales rows are required."
        )

    # Split by time rather than randomly.
    cutoff = df["date"].quantile(0.80)

    train_df = df[df["date"] <= cutoff]
    test_df = df[df["date"] > cutoff]

    X_train = build_features(train_df)
    X_test = build_features(test_df)

    y_train = train_df["units_sold"]
    y_test = test_df["units_sold"]

    numeric_pipeline = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="median"),
        ),
        ("scaler", StandardScaler()),
    ])

    categorical_pipeline = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="most_frequent"),
        ),
        (
            "onehot",
            OneHotEncoder(handle_unknown="ignore"),
        ),
    ])

    preprocessor = ColumnTransformer([
        (
            "numeric",
            numeric_pipeline,
            NUMERIC_FEATURES,
        ),
        (
            "categorical",
            categorical_pipeline,
            CATEGORICAL_FEATURES,
        ),
    ])

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        (
            "model",
            RandomForestRegressor(
                n_estimators=180,
                max_depth=16,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1,
            ),
        ),
    ])

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    metrics = {
        "mae": round(
            float(mean_absolute_error(y_test, predictions)), 4
        ),
        "rmse": round(
            float(mean_squared_error(y_test, predictions) ** 0.5),
            4,
        ),
        "bias": round(
            float((predictions - y_test).mean()), 4
        ),
        "train_rows": int(len(train_df)),
        "test_rows": int(len(test_df)),
        "cutoff_date": str(cutoff.date()),
    }

    model_path.parent.mkdir(
        parents=True, exist_ok=True
    )

    joblib.dump(
        {
            "pipeline": pipeline,
            "metrics": metrics,
            "version": "local-v1",
        },
        model_path,
    )

    # Keep a reference distribution from the training period.
    REFERENCE_PATH.parent.mkdir(
        parents=True, exist_ok=True
    )

    build_features(train_df).to_csv(
        REFERENCE_PATH,
        index=False,
    )

    metrics_path = (
        model_path.parent / "evaluation_metrics.json"
    )

    metrics_path.write_text(
        json.dumps(metrics, indent=2),
        encoding="utf-8",
    )

    print("Model saved:", model_path)
    print(json.dumps(metrics, indent=2))

    return metrics


if __name__ == "__main__":
    train_model()
