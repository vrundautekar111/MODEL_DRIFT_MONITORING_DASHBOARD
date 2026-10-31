
import pandas as pd

REQUIRED_COLUMNS = [
    "date",
    "product_id",
    "category",
    "store_id",
    "price",
    "discount_pct",
    "marketing_spend",
    "stock_available",
    "day_of_week",
    "is_weekend",
    "is_promotion",
    "units_sold",
]


def validate_sales_frame(df: pd.DataFrame):
    issues = []

    missing_columns = sorted(
        set(REQUIRED_COLUMNS) - set(df.columns)
    )

    if missing_columns:
        issues.append({
            "severity": "critical",
            "issue": "missing_columns",
            "details": ", ".join(missing_columns),
        })

        return {
            "ok": False,
            "row_count": int(len(df)),
            "issues": issues,
        }

    if df.empty:
        issues.append({
            "severity": "critical",
            "issue": "empty_batch",
            "details": "No rows received",
        })

    null_count = int(
        df[REQUIRED_COLUMNS].isna().sum().sum()
    )

    if null_count:
        issues.append({
            "severity": "warning",
            "issue": "missing_values",
            "details": f"{null_count} null cells",
        })

    duplicates = int(
        df.duplicated(
            ["date", "product_id", "store_id"]
        ).sum()
    )

    if duplicates:
        issues.append({
            "severity": "warning",
            "issue": "duplicate_records",
            "details": (
                f"{duplicates} duplicate product/date/store rows"
            ),
        })

    numeric_columns = [
        "price",
        "discount_pct",
        "marketing_spend",
        "stock_available",
        "units_sold",
    ]

    for column in numeric_columns:
        values = pd.to_numeric(
            df[column], errors="coerce"
        )

        if values.isna().any():
            issues.append({
                "severity": "critical",
                "issue": "invalid_numeric_values",
                "details": f"Invalid numeric values in {column}",
            })

        if (values.dropna() < 0).any():
            issues.append({
                "severity": "critical",
                "issue": "negative_values",
                "details": f"Negative values in {column}",
            })

    dates = pd.to_datetime(df["date"], errors="coerce")

    if dates.isna().any():
        issues.append({
            "severity": "critical",
            "issue": "invalid_dates",
            "details": "Unparseable dates found",
        })

    critical = any(
        issue["severity"] == "critical"
        for issue in issues
    )

    return {
        "ok": not critical,
        "row_count": int(len(df)),
        "issues": issues,
    }
