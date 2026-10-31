
import streamlit as st

from dashboard.services.api_client import post

st.title("Retraining center")

st.warning(
    "This operation trains and evaluates a candidate model. "
    "It does not replace the active model."
)

st.write(
    "Review data quality, drift, training data freshness, "
    "and labeled forecast errors before retraining."
)

if st.button("Train and evaluate candidate", type="primary"):
    with st.spinner("Training candidate model..."):
        try:
            result = post(
                "/retraining/evaluate",
                {},
                timeout=300,
            )

            st.session_state["candidate_result"] = result

        except Exception as exc:
            st.error(f"Retraining failed: {exc}")

if "candidate_result" in st.session_state:
    st.markdown("### Candidate evaluation result")
    st.json(st.session_state["candidate_result"])
