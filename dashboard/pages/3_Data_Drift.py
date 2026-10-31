
import streamlit as st

from dashboard.services.api_client import get, post
from dashboard.components.charts import drift_chart

st.title("Data drift")
st.write(
    "Compare the current sales feature distribution "
    "with the model's training reference."
)

if st.button("Run drift analysis", type="primary"):
    try:
        st.session_state["drift_result"] = post(
            "/monitoring/run"
        )
    except Exception as exc:
        st.error(str(exc))

result = st.session_state.get("drift_result")

if result is None:
    try:
        history = get("/monitoring/history")

        if history:
            result = history[0]["result"]
    except Exception:
        result = None

if result:
    a, b = st.columns(2)

    a.metric(
        "Drifted features",
        result.get("drifted_features", 0),
    )

    b.metric(
        "Warning features",
        result.get("warning_features", 0),
    )

    st.plotly_chart(
        drift_chart(result.get("drift", [])),
        use_container_width=True,
    )

    st.dataframe(
        result.get("drift", []),
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("Start the API and run a monitoring check.")
