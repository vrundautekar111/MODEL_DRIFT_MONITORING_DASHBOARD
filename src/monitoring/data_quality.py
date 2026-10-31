
from src.data.validation import validate_sales_frame


def assess_data_quality(df):
    validation = validate_sales_frame(df)

    missing_rate = (
        float(df.isna().mean().mean())
        if len(df.columns)
        else 0.0
    )

    return {
        "ok": validation["ok"],
        "row_count": validation["row_count"],
        "missing_rate": missing_rate,
        "duplicate_rows": int(df.duplicated().sum()),
        "issues": validation["issues"],
    }
