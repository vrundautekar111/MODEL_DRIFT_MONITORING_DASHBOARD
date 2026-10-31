
import pandas as pd

from src.data.validation import validate_sales_frame


def load_sales_csv(path):
    df = pd.read_csv(path)
    validation = validate_sales_frame(df)

    if not validation["ok"]:
        raise ValueError(
            f"Sales data failed validation: "
            f"{validation['issues']}"
        )

    return df, validation
