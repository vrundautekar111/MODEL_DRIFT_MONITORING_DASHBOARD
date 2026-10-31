
import streamlit as st

from dashboard.services.api_client import get

st.title("Model performance")
st.caption(
    "Holdout evaluation and live forecast error after actual "
    "sales labels become available."
)

try:
    model = get("/models")
    performance = get("/sales/performance")

    holdout = model.get("metrics", {})

    a, b, c = st.columns(3)

    a.metric("Holdout MAE", holdout.get("mae", "n/a"))

    b.metric("Labeled predictions", performance.get("rows", 0))

    live_mae = performance.get("mae")

    c.metric(
        "Live MAE",
        round(live_mae, 3)
        if live_mae is not None
        else "Waiting for actuals",
    )

    st.markdown("### Holdout metrics")
    st.json(holdout)

    st.markdown("### Live performance")
    st.json(performance)

except Exception as exc:
    st.error(f"API unavailable: {exc}")
