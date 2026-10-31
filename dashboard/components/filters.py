
import streamlit as st


def sidebar_filters(df):
    st.sidebar.markdown("### Workspace filters")

    categories = sorted(
        df["category"].dropna().unique().tolist()
    )

    products = sorted(
        df["product_id"].dropna().unique().tolist()
    )

    selected_categories = st.sidebar.multiselect(
        "Category",
        categories,
        default=categories,
    )

    selected_products = st.sidebar.multiselect(
        "Product",
        products,
        default=products,
    )

    return df[
        df["category"].isin(selected_categories)
        & df["product_id"].isin(selected_products)
    ]
