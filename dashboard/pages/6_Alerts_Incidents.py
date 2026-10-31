
import streamlit as st

from dashboard.services.api_client import get, post

st.title("Alerts & incidents")

try:
    alerts = get("/alerts")

    if not alerts:
        st.success("No alerts recorded yet.")

    for alert in alerts:
        title = (
            f"#{alert['id']} · "
            f"{alert['severity'].upper()} · "
            f"{alert['title']} · {alert['status']}"
        )

        with st.expander(title):
            st.write(alert.get("details", ""))

            if alert["status"] == "open":
                if st.button(
                    "Resolve alert",
                    key=f"resolve-{alert['id']}",
                ):
                    try:
                        post(
                            f"/alerts/{alert['id']}/resolve",
                            {},
                        )

                        st.success("Alert resolved.")
                    except Exception as exc:
                        st.error(str(exc))

except Exception as exc:
    st.error(f"API unavailable: {exc}")
