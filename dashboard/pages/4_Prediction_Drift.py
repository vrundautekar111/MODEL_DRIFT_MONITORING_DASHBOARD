
import streamlit as st

from dashboard.services.api_client import get

st.title("Prediction drift")
st.write(
    "Inspect changes in the model's predicted-demand distribution."
)

try:
    history = get("/monitoring/history")

    if history:
        result = history[0]["result"]
        summary = result.get("prediction_distribution", {})

        st.json(summary)

        st.info(
            "Compare stored prediction distributions across "
            "separate monitoring windows for reliable trend analysis."
        )
    else:
        st.info("No monitoring run is stored yet.")

except Exception as exc:
    st.error(f"API unavailable: {exc}")
