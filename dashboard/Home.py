
from pathlib import Path
import sys

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dashboard.services.api_client import get, post
from dashboard.components.metric_cards import metric_card
from dashboard.components.charts import (
    sales_trend,
    category_chart,
    drift_chart,
)
from dashboard.components.filters import sidebar_filters


st.set_page_config(
    page_title="SalesGuard AI | Model Observability",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

css_path = ROOT / "dashboard/assets/style.css"

st.markdown(
    f"<style>{css_path.read_text(encoding='utf-8')}</style>",
    unsafe_allow_html=True,
)

data_path = ROOT / "data/sample/sales_sample.csv"

if not data_path.exists():
    st.error(
        "Sales data is missing. Run "
        "python scripts/generate_sales_data.py"
    )
    st.stop()

df = pd.read_csv(data_path, parse_dates=["date"])
filtered = sidebar_filters(df)

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">
            SALES INTELLIGENCE / MODEL OBSERVABILITY
        </div>
        <div class="hero-title">
            SalesGuard <span style="color:#68d7ff">AI</span>
        </div>
        <div class="hero-sub">
            Monitor product demand, detect distribution shifts,
            and protect forecast quality.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

units = filtered["units_sold"].sum()
products = filtered["product_id"].nunique()
daily_units = (
    filtered.groupby("date")["units_sold"]
    .sum()
    .mean()
)

cols = st.columns(5)

with cols[0]:
    metric_card("UNITS SOLD", f"{units:,.0f}")

with cols[1]:
    metric_card("PRODUCTS", f"{products:,}")

with cols[2]:
    metric_card(
        "AVG. DAILY UNITS",
        f"{daily_units:,.1f}",
    )

with cols[3]:
    try:
        model = get("/models")
        metrics = model.get("metrics", {})
        metric_card(
            "HOLDOUT MAE",
            f"{metrics.get('mae', 0):.2f}",
        )
    except Exception:
        metric_card("HOLDOUT MAE", "Unavailable")

with cols[4]:
    if st.button(
        "▶ Run monitoring",
        type="primary",
        use_container_width=True,
    ):
        with st.spinner(
            "Checking data quality and model drift..."
        ):
            try:
                result = post("/monitoring/run")
                st.session_state["latest_monitoring"] = result
                st.success(
                    f"Monitoring complete: "
                    f"{result['status'].upper()}"
                )
            except Exception as exc:
                st.error(f"Monitoring failed: {exc}")

try:
    model = get("/models")
    metrics = model.get("metrics", {})

    st.caption(
        f"Model: {model.get('active_model', 'unknown')} · "
        f"MAE: {metrics.get('mae', 'n/a')} · "
        f"RMSE: {metrics.get('rmse', 'n/a')}"
    )
except Exception:
    st.warning(
        "API unavailable. Start it using "
        "uvicorn app.main:app --reload"
    )

st.markdown("### Business performance")

left, right = st.columns([1.55, 1])

with left:
    st.plotly_chart(
        sales_trend(filtered),
        use_container_width=True,
    )

with right:
    st.plotly_chart(
        category_chart(filtered),
        use_container_width=True,
    )

st.markdown("### Model health & monitoring")

latest = st.session_state.get("latest_monitoring")

if latest is None:
    try:
        history = get("/monitoring/history")

        if history:
            latest = history[0]["result"]

    except Exception:
        latest = None

health_col, drift_col = st.columns([0.75, 1.25])

with health_col:
    if latest:
        status = latest.get("status", "unknown").upper()

        if status == "HEALTHY":
            st.success(f"System status: {status}")
        elif status == "WARNING":
            st.warning(f"System status: {status}")
        else:
            st.error(f"System status: {status}")

        st.metric(
            "Drifted features",
            latest.get("drifted_features", 0),
        )

        st.metric(
            "Warning features",
            latest.get("warning_features", 0),
        )

        st.write(latest.get("recommendation", ""))

        if latest.get("retraining", {}).get("recommended"):
            st.warning(
                "Retraining evaluation recommended. "
                "Review the candidate before deployment."
            )
    else:
        st.info(
            "Run monitoring to populate model health metrics."
        )

with drift_col:
    if latest:
        st.plotly_chart(
            drift_chart(latest.get("drift", [])),
            use_container_width=True,
        )
    else:
        st.info(
            "Feature-level drift scores will appear "
            "after the first monitoring run."
        )

st.markdown("### Latest product records")

st.dataframe(
    filtered.sort_values("date", ascending=False).head(15),
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "Synthetic demonstration data. Drift thresholds "
    "should be calibrated using historical company sales."
)
