
from pathlib import Path

import numpy as np
import pandas as pd


PRODUCTS = [
    {
        "product_id": "P1001",
        "category": "Electronics",
        "base_price": 25000,
        "base_demand": 18,
    },
    {
        "product_id": "P1002",
        "category": "Electronics",
        "base_price": 15000,
        "base_demand": 25,
    },
    {
        "product_id": "P2001",
        "category": "Clothing",
        "base_price": 900,
        "base_demand": 55,
    },
    {
        "product_id": "P3001",
        "category": "Home",
        "base_price": 1800,
        "base_demand": 32,
    },
    {
        "product_id": "P4001",
        "category": "Accessories",
        "base_price": 650,
        "base_demand": 45,
    },
]


def generate_sales_data(
    start="2024-01-01",
    end="2026-10-28",
    seed=42,
):
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start, end, freq="D")

    rows = []

    for product in PRODUCTS:
        for store_id in ["S01", "S02"]:
            previous_sales = product["base_demand"]

            for date in dates:
                weekend = int(date.dayofweek >= 5)

                promotion_probability = (
                    0.22
                    if date >= pd.Timestamp("2026-04-01")
                    else 0.15
                )

                promotion = int(
                    rng.random() < promotion_probability
                )

                discount = (
                    float(rng.uniform(10, 30))
                    if promotion
                    else float(rng.uniform(0, 5))
                )

                seasonality = (
                    1 + 0.20 * np.sin(
                        2 * np.pi * date.month / 12
                    )
                )

                # Simulated business demand shift.
                demand_shift = (
                    1.35
                    if date >= pd.Timestamp("2026-04-01")
                    else 1.0
                )

                price = product["base_price"] * (
                    1 - discount / 100
                )

                marketing_spend = (
                    float(rng.uniform(1000, 8000))
                    if promotion
                    else float(rng.uniform(200, 2000))
                )

                expected_demand = (
                    product["base_demand"]
                    * seasonality
                    * demand_shift
                    * (1 + 0.20 * weekend)
                    * (1 + 0.60 * promotion)
                )

                # Simple demand momentum.
                expected_demand = (
                    0.85 * expected_demand
                    + 0.15 * previous_sales
                )

                stock_available = int(
                    max(0, rng.normal(100, 20))
                )

                units_sold = int(
                    min(
                        stock_available,
                        rng.poisson(max(expected_demand, 0.1)),
                    )
                )

                rows.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "product_id": product["product_id"],
                    "category": product["category"],
                    "store_id": store_id,
                    "price": round(float(price), 2),
                    "discount_pct": round(discount, 2),
                    "marketing_spend": round(
                        marketing_spend, 2
                    ),
                    "stock_available": stock_available,
                    "day_of_week": int(date.dayofweek),
                    "is_weekend": weekend,
                    "is_promotion": promotion,
                    "units_sold": units_sold,
                })

                previous_sales = units_sold

    return pd.DataFrame(rows)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]

    output_path = root / "data/sample/sales_sample.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = generate_sales_data()
    df.to_csv(output_path, index=False)

    print(f"Created: {output_path}")
    print(f"Rows: {len(df):,}")
