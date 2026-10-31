
import pandas as pd

NUMERIC_FEATURES = [
    "price",
    "discount_pct",
    "marketing_spend",
    "stock_available",
    "day_of_week",
    "is_weekend",
    "is_promotion",
    "month",
    "day_of_month",
]

CATEGORICAL_FEATURES = [
    "product_id",
    "category",
    "store_id",
]

FEATURE_COLUMNS = (
    NUMERIC_FEATURES + CATEGORICAL_FEATURES
)


def build_features(df: pd.DataFrame):
    frame = df.copy()
    frame["date"] = pd.to_datetime(frame["date"])

    frame["month"] = frame["date"].dt.month
    frame["day_of_month"] = frame["date"].dt.day

    return frame[FEATURE_COLUMNS]
