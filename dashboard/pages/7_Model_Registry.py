
import streamlit as st

from dashboard.services.api_client import get

st.title("Model registry")
st.caption("Inspect active model metadata and registered versions.")

try:
    model = get("/models")

    st.metric(
        "Active model",
        model.get("active_model", "unknown"),
    )

    st.markdown("### Evaluation metrics")
    st.json(model.get("metrics", {}))

    st.markdown("### Registered versions")
    st.dataframe(
        model.get("versions", []),
        use_container_width=True,
        hide_index=True,
    )

except Exception as exc:
    st.error(f"API unavailable: {exc}")
