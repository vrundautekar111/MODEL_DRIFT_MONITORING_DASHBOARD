
import streamlit as st


def metric_card(
    label,
    value,
    delta=None,
    help_text=None,
):
    delta_html = (
        f'<div class="metric-delta">{delta}</div>'
        if delta else ""
    )

    help_html = (
        f'<div class="metric-help">{help_text}</div>'
        if help_text else ""
    )

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
            {help_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
