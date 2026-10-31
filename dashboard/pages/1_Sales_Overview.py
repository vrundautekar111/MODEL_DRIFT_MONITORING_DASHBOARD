
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]

st.title("Sales overview")
st.caption("Explore sales performance by date and product.")

df = pd.read_csv(
    ROOT / "data/sample/sales_sample.csv",
    parse_dates=["date"],
)

date_range = st.date_input(
    "Sales date range",
    value=(df["date"].min().date(), df["date"].max().date()),
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = date_range

    view = df[
        (df["date"].dt.date >= start)
        & (df["date"].dt.date <= end)
    ]
else:
    view = df

a, b, c = st.columns(3)

a.metric("Units sold", f"{view['units_sold'].sum():,.0f}")

b.metric(
    "Revenue proxy",
    f"₹{(view['price'] * view['units_sold']).sum():,.0f}",
)

c.metric("Records", f"{len(view):,}")

daily = (
    view.groupby("date", as_index=False)["units_sold"]
    .sum()
)

fig = px.line(
    daily,
    x="date",
    y="units_sold",
    title="Daily demand",
    template="plotly_dark",
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(
    view.tail(100),
    use_container_width=True,
    hide_index=True,
)
