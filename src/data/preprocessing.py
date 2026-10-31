
import pandas as pd


def prepare_sales_frame(df: pd.DataFrame):
    frame = df.copy()

    frame["date"] = pd.to_datetime(
        frame["date"], errors="coerce"
    )

    frame = frame.dropna(
        subset=["date", "units_sold"]
    )

    numeric_columns = [
        "price",
        "discount_pct",
        "marketing_spend",
        "stock_available",
        "day_of_week",
        "is_weekend",
        "is_promotion",
        "units_sold",
    ]

    for column in numeric_columns:
        frame[column] = pd.to_numeric(
            frame[column], errors="coerce"
        )

    frame = frame.dropna(
        subset=["price", "units_sold"]
    )

    frame = frame.drop_duplicates(
        ["date", "product_id", "store_id"]
    )

    return frame.sort_values(
        "date"
    ).reset_index(drop=True)
