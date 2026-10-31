
import pandas as pd

from src.data.validation import validate_sales_frame


def test_validation_accepts_valid_sales_row():
    df = pd.DataFrame([{
        "date": "2026-01-01",
        "product_id": "P1",
        "category": "Home",
        "store_id": "S1",
        "price": 10,
        "discount_pct": 0,
        "marketing_spend": 0,
        "stock_available": 10,
        "day_of_week": 3,
        "is_weekend": 0,
        "is_promotion": 0,
        "units_sold": 2,
    }])

    assert validate_sales_frame(df)["ok"]


def test_validation_flags_missing_columns():
    result = validate_sales_frame(
        pd.DataFrame({"date": ["2026-01-01"]})
    )

    assert not result["ok"]
