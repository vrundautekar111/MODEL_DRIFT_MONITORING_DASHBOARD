
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

CHART_TEMPLATE = "plotly_dark"


def sales_trend(df):
    daily = (
        df.groupby("date", as_index=False)["units_sold"]
        .sum()
    )

    fig = px.line(
        daily,
        x="date",
        y="units_sold",
        title="Daily units sold",
        template=CHART_TEMPLATE,
    )

    fig.update_traces(line=dict(width=2.5))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=55, b=10),
    )

    return fig


def category_chart(df):
    grouped = (
        df.groupby("category", as_index=False)["units_sold"]
        .sum()
        .sort_values("units_sold", ascending=True)
    )

    fig = px.bar(
        grouped,
        x="units_sold",
        y="category",
        orientation="h",
        title="Sales by category",
        template=CHART_TEMPLATE,
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=55, b=10),
    )

    return fig


def drift_chart(drift):
    if not drift:
        return go.Figure()

    df = pd.DataFrame(drift)
    df["score_numeric"] = pd.to_numeric(
        df["score"], errors="coerce"
    )

    fig = px.bar(
        df,
        x="feature",
        y="score_numeric",
        color="status",
        title="Feature drift scores",
        template=CHART_TEMPLATE,
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=55, b=10),
    )

    return fig
