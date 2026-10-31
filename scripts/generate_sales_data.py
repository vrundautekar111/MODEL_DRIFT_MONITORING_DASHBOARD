
from pathlib import Path

from src.data.generate_sales_data import generate_sales_data


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    output_path = root / "data/sample/sales_sample.csv"

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = generate_sales_data()
    df.to_csv(output_path, index=False)

    print(f"Saved {len(df):,} sales records")
    print(f"Output: {output_path}")
