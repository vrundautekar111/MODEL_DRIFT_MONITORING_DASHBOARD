
from pathlib import Path
import sys

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.monitoring.data_quality import assess_data_quality

st.title("Data quality")
st.caption("Validate the dataset before trusting its predictions.")

df = pd.read_csv(ROOT / "data/sample/sales_sample.csv")
result = assess_data_quality(df)

a, b, c = st.columns(3)

a.metric("Rows checked", f"{result['row_count']:,}")
b.metric("Missing cell rate", f"{result['missing_rate']:.2%}")
c.metric("Duplicate rows", result["duplicate_rows"])

if result["ok"]:
    st.success("No critical data-quality failures.")
else:
    st.error("Critical data-quality issues detected.")

st.markdown("### Validation issues")
st.json(result["issues"])

missing = (
    df.isna()
    .sum()
    .rename("missing_count")
    .reset_index()
    .rename(columns={"index": "column"})
)

st.markdown("### Missing values by column")
st.dataframe(missing, use_container_width=True, hide_index=True)
