import streamlit as st
import plotly.express as px
import pandas as pd

from src.ai_assistant import analyze_question

from src.analytics import (
    get_states,
    get_total_revenue,
    get_total_orders,
    get_average_order_value,
    get_late_delivery_rate,
    get_average_review_score,
    get_monthly_revenue,
    get_category_sales_vs_reviews,
    get_repeat_purchase_summary,
    get_rfm_segments,
    get_delay_severity_reviews,
    get_late_delivery_by_state
)


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Olist AI Business Analyst",
    page_icon="📊",
    layout="wide"
)


# ==================================================
# DESIGN SYSTEM
# ==================================================

BG = "#0B1220"

CARD = "#111827"
CARD_2 = "#172033"

BORDER = "#273449"

WHITE = "#F8FAFC"
TEXT = "#CBD5E1"
MUTED = "#7C8AA5"

BLUE = "#5B8CFF"
TEAL = "#31D0AA"
AMBER = "#F4B860"
RED = "#FF6B6B"

SLATE = "#94A3B8"

GRID = "rgba(148,163,184,0.12)"


# ==================================================
# FRIENDLY PLOT LABELS
# ==================================================

PLOT_LABELS = {
    "revenue": "Revenue",
    "orders": "Orders",
    "average_order_value": "Average Order Value",
    "late_delivery_rate": "Late Delivery Rate",
    "average_review_score": "Average Review Score",
    "average_delivery_days": "Average Delivery Days",
    "average_freight_value": "Average Freight Value",
    "customer_state": "Customer State",
    "seller_state": "Seller State",
    "seller_id": "Seller",
    "seller": "Seller",
    "product_category": "Product Category",
    "product_id": "Product",
    "product": "Product",
    "items_sold": "Items Sold",
    "total_reviews": "Total Reviews",
    "customers": "Customers",
    "customer_type": "Customer Type",
    "customer_segment": "Customer Segment",
    "avg_recency": "Average Recency",
    "avg_frequency": "Average Frequency",
    "avg_monetary": "Average Monetary Value",
    "delivery_status": "Delivery Status",
    "delay_group": "Delay Severity",
    "review_score": "Review Score",
    "month": "Month",
    "mom_growth_pct": "Monthly Growth",
    "order_bucket": "Orders per Customer",
    "state_relationship": "Marketplace Geography",
    "retention_rate": "Retention Rate",
    "cohort_index": "Months Since First Purchase",
    "cohort": "Cohort",
    "cohort_month": "Cohort Month",
    "cohort_size": "Cohort Size"
}


# ==================================================
# CSS
# ==================================================

st.markdown(
    f"""
<style>

.stApp {{
    background:
        radial-gradient(
            circle at top right,
            rgba(91,140,255,0.08),
            transparent 28%
        ),
        {BG};
}}

.block-container {{
    max-width: 1450px;
    padding-top: 1.2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    padding-bottom: 4rem;
}}

h1, h2, h3, h4, h5, h6 {{
    color: {WHITE} !important;
}}

p, label {{
    color: {TEXT};
}}


/* KPI CARDS */

.kpi-card {{
    background:
        linear-gradient(
            145deg,
            {CARD},
            {CARD_2}
        );

    border:
        1px solid {BORDER};

    border-radius:
        14px;

    padding:
        17px 18px;

    min-height:
        105px;
}}

.kpi-label {{
    color:
        {MUTED};

    font-size:
        12px;

    font-weight:
        600;

    letter-spacing:
        0.3px;
}}

.kpi-value {{
    color:
        {WHITE};

    font-size:
        27px;

    font-weight:
        800;

    margin-top:
        8px;
}}

.kpi-accent {{
    height:
        3px;

    width:
        32px;

    border-radius:
        5px;

    margin-bottom:
        12px;
}}


/* SECTION TITLES */

.section-title {{
    color:
        {WHITE};

    font-size:
        20px;

    font-weight:
        800;

    margin-top:
        4px;
}}

.section-subtitle {{
    color:
        {MUTED};

    font-size:
        12px;

    margin-top:
        4px;

    margin-bottom:
        12px;
}}


/* SELECTBOX */

div[data-baseweb="select"] > div {{
    background:
        {CARD};

    border:
        1px solid {BORDER};

    border-radius:
        9px;
}}


/* TEXT INPUT */

.stTextInput input {{
    background:
        {CARD};

    color:
        {WHITE};

    border:
        1px solid {BORDER};

    border-radius:
        10px;

    height:
        48px;
}}

.stTextInput input:focus {{
    border-color:
        {BLUE};

    box-shadow:
        0 0 0 1px {BLUE};
}}


/* AI MARKDOWN */

[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
[data-testid="stMarkdownContainer"] h5,
[data-testid="stMarkdownContainer"] h6 {{
    color:
        {WHITE} !important;
}}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {{
    color:
        {TEXT} !important;
}}

[data-testid="stMarkdownContainer"] strong {{
    color:
        {WHITE} !important;
}}


/* CLEAN STREAMLIT */

#MainMenu {{
    visibility:
        hidden;
}}

footer {{
    visibility:
        hidden;
}}

</style>
""",
    unsafe_allow_html=True
)


# ==================================================
# CHART STYLE
# ==================================================

def style_chart(fig):

    fig.update_layout(
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,

        font=dict(
            color=TEXT,
            size=10
        ),

        title=dict(
            font=dict(
                color=WHITE,
                size=15
            ),
            x=0.03
        ),

        margin=dict(
            l=35,
            r=20,
            t=55,
            b=40
        ),

        hoverlabel=dict(
            bgcolor=CARD_2,
            font_color=WHITE,
            bordercolor=BORDER
        )
    )

    fig.update_xaxes(
        gridcolor=GRID,
        linecolor=BORDER,
        zeroline=False
    )

    fig.update_yaxes(
        gridcolor=GRID,
        linecolor=BORDER,
        zeroline=False
    )

    return fig


# ==================================================
# PIE CHART STYLE
# ==================================================

def style_pie_chart(
    fig,
    height=340
):

    fig.update_layout(
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,

        font=dict(
            color=TEXT,
            size=10
        ),

        title=dict(
            font=dict(
                color=WHITE,
                size=15
            ),
            x=0.03
        ),

        legend=dict(
            font=dict(
                color=TEXT,
                size=10
            )
        ),

        margin=dict(
            l=20,
            r=20,
            t=55,
            b=35
        ),

        height=height,

        hoverlabel=dict(
            bgcolor=CARD_2,
            font_color=WHITE,
            bordercolor=BORDER
        )
    )

    return fig


# ==================================================
# SAFE NUMERIC CONVERSION
# ==================================================

def convert_numeric_columns(
    dataframe,
    columns
):

    df = dataframe.copy()

    for column in columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


# ==================================================
# AI DYNAMIC CHART
# ==================================================

def create_dynamic_chart(
    plan,
    data
):

    if data is None:
        return None

    if data.empty:
        return None

    analysis = plan.get(
        "analysis",
        "none"
    )


    # ==================================================
    # MONTHLY REVENUE
    # ==================================================

    if analysis == "monthly_revenue":

        data = convert_numeric_columns(
            data,
            [
                "revenue"
            ]
        )

        data = data.dropna(
            subset=[
                "revenue"
            ]
        )

        if data.empty:
            return None

        fig = px.line(
            data,

            x="month",
            y="revenue",

            markers=True,

            title="Monthly Revenue",

            labels=PLOT_LABELS
        )

        fig.update_traces(
            line=dict(
                color=BLUE,
                width=3
            ),

            marker=dict(
                size=5,
                color=TEAL
            ),

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Revenue: %{y:,.0f} BRL"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            height=330,
            xaxis_title=None,
            yaxis_title="Revenue"
        )

        style_chart(fig)

        return fig


    # ==================================================
    # MONTHLY GROWTH
    # ==================================================

    if analysis == "monthly_growth":

        data = convert_numeric_columns(
            data,
            [
                "mom_growth_pct"
            ]
        )

        data = data.dropna(
            subset=[
                "mom_growth_pct"
            ]
        )

        if data.empty:
            return None

        fig = px.line(
            data,

            x="month",
            y="mom_growth_pct",

            markers=True,

            title="Month-over-Month Revenue Growth",

            labels=PLOT_LABELS
        )

        fig.update_traces(
            line=dict(
                color=TEAL,
                width=3
            )
        )

        fig.update_layout(
            height=330,
            xaxis_title=None,
            yaxis_title="Growth %"
        )

        style_chart(fig)

        return fig


    # ==================================================
    # REVENUE BY STATE
    # ==================================================

    if analysis == "revenue_by_state":

        data = convert_numeric_columns(
            data,
            [
                "revenue"
            ]
        )

        data = data.dropna(
            subset=[
                "revenue"
            ]
        )

        df = data.head(15)

        if df.empty:
            return None

        fig = px.bar(
            df,

            x="revenue",
            y="customer_state",

            orientation="h",

            title="Revenue by Customer State",

            labels=PLOT_LABELS
        )

        fig.update_traces(
            marker_color=BLUE,

            hovertemplate=(
                "<b>%{y}</b><br>"
                "Revenue: %{x:,.0f} BRL"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            yaxis=dict(
                autorange="reversed"
            ),

            height=360,

            xaxis_title="Revenue",
            yaxis_title=None
        )

        style_chart(fig)

        return fig


    # ==================================================
    # ORDERS BY STATE
    # ==================================================

    if analysis == "orders_by_state":

        data = convert_numeric_columns(
            data,
            [
                "orders"
            ]
        )

        data = data.dropna(
            subset=[
                "orders"
            ]
        )

        df = data.head(15)

        if df.empty:
            return None

        fig = px.bar(
            df,

            x="orders",
            y="customer_state",

            orientation="h",

            title="Orders by Customer State",

            labels=PLOT_LABELS
        )

        fig.update_traces(
            marker_color=TEAL,

            hovertemplate=(
                "<b>%{y}</b><br>"
                "Orders: %{x:,.0f}"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            yaxis=dict(
                autorange="reversed"
            ),

            height=360,

            xaxis_title="Orders",
            yaxis_title=None
        )

        style_chart(fig)

        return fig


    # ==================================================
    # AOV BY STATE
    # ==================================================

    if analysis == "aov_by_state":

        data = convert_numeric_columns(
            data,
            [
                "average_order_value"
            ]
        )

        data = data.dropna(
            subset=[
                "average_order_value"
            ]
        )

        df = data.head(15)

        if df.empty:
            return None

        fig = px.bar(
            df,

            x="average_order_value",
            y="customer_state",

            orientation="h",

            title="Average Order Value by State",

            labels=PLOT_LABELS
        )

        fig.update_traces(
            marker_color=AMBER,

            hovertemplate=(
                "<b>%{y}</b><br>"
                "Average Order Value: %{x:,.2f} BRL"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            yaxis=dict(
                autorange="reversed"
            ),

            height=360,

            xaxis_title="Average Order Value",
            yaxis_title=None
        )

        style_chart(fig)

        return fig


    # ==================================================
    # STATE PERFORMANCE
    # ==================================================

    if analysis == "state_performance":

        data = convert_numeric_columns(
            data,
            [
                "revenue",
                "late_delivery_rate",
                "orders",
                "average_review_score",
                "average_delivery_days"
            ]
        )

        data = data.dropna(
            subset=[
                "revenue",
                "late_delivery_rate",
                "orders"
            ]
        )

        if data.empty:
            return None

        fig = px.scatter(
            data,

            x="revenue",
            y="late_delivery_rate",

            size="orders",

            hover_name="customer_state",

            hover_data={
                "average_review_score": ":.2f",
                "average_delivery_days": ":.2f",
                "orders": ":,.0f",
                "revenue": ":,.0f",
                "late_delivery_rate": ":.1%"
            },

            title=(
                "Revenue vs Late Delivery Rate "
                "by State"
            ),

            labels=PLOT_LABELS
        )

        fig.update_traces(
            marker=dict(
                color=BLUE,
                opacity=0.78,

                line=dict(
                    width=1,
                    color=WHITE
                )
            )
        )

        fig.update_yaxes(
            tickformat=".0%"
        )

        fig.update_layout(
            height=380,

            xaxis_title="Revenue",
            yaxis_title="Late Delivery Rate"
        )

        style_chart(fig)

        return fig


    # ==================================================
    # TOP CATEGORIES
    # ==================================================

    if analysis == "top_categories":

        data = convert_numeric_columns(
            data,
            [
                "revenue"
            ]
        )

        data = data.dropna(
            subset=[
                "revenue"
            ]
        )

        if data.empty:
            return None

        fig = px.bar(
            data,

            x="revenue",
            y="product_category",

            orientation="h",

            title="Top Categories by Revenue",

            labels=PLOT_LABELS
        )

        fig.update_traces(
            marker_color=BLUE,

            hovertemplate=(
                "<b>%{y}</b><br>"
                "Revenue: %{x:,.0f} BRL"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            yaxis=dict(
                autorange="reversed"
            ),

            height=360,

            xaxis_title="Revenue",
            yaxis_title=None
        )

        style_chart(fig)

        return fig


    # ==================================================
    # CATEGORY SALES VS REVIEWS
    # ==================================================

    if analysis == "category_sales_vs_reviews":

        data = convert_numeric_columns(
            data,
            [
                "revenue",
                "average_review_score",
                "items_sold",
                "total_reviews"
            ]
        )

        data = data.dropna(
            subset=[
                "revenue",
                "average_review_score",
                "items_sold"
            ]
        )

        data = data[
            data["items_sold"] > 0
        ]

        if data.empty:
            return None

        fig = px.scatter(
            data,

            x="revenue",
            y="average_review_score",

            size="items_sold",

            hover_name="product_category",

            hover_data={
                "revenue": ":,.0f",
                "average_review_score": ":.2f",
                "items_sold": ":,.0f",
                "total_reviews": ":,.0f"
            },

            title=(
                "Category Revenue vs "
                "Customer Satisfaction"
            ),

            labels=PLOT_LABELS
        )

        fig.update_traces(
            marker=dict(
                color=TEAL,
                opacity=0.75,

                line=dict(
                    color=WHITE,
                    width=1
                )
            )
        )

        fig.update_layout(
            height=380,

            yaxis_range=[
                0,
                5
            ],

            xaxis_title="Revenue",

            yaxis_title=(
                "Average Review Score"
            )
        )

        style_chart(fig)

        return fig


    # ==================================================
    # LOW RATED PRODUCTS
    # ==================================================

    if analysis == "low_rated_products":

        data = convert_numeric_columns(
            data,
            [
                "average_review_score",
                "items_sold",
                "revenue",
                "total_reviews"
            ]
        )

        data = data.dropna(
            subset=[
                "average_review_score"
            ]
        )

        if data.empty:
            return None

        df = data.copy()

        df["product"] = (
            df["product_id"]
            .astype(str)
            .str[:10]
        )

        fig = px.bar(
            df,

            x="average_review_score",
            y="product",

            orientation="h",

            hover_data={
                "product_category": True,
                "items_sold": ":,.0f",
                "revenue": ":,.0f",
                "total_reviews": ":,.0f"
            },

            title=(
                "High-Sales Products "
                "with Weak Reviews"
            ),

            labels=PLOT_LABELS
        )

        fig.update_traces(
            marker_color=RED
        )

        fig.update_layout(
            yaxis=dict(
                autorange="reversed"
            ),

            xaxis_range=[
                0,
                5
            ],

            height=420,

            xaxis_title="Average Review",
            yaxis_title=None
        )

        style_chart(fig)

        return fig


    # ==================================================
    # TOP SELLERS
    # ==================================================

    if analysis == "top_sellers":

        data = convert_numeric_columns(
            data,
            [
                "revenue",
                "orders"
            ]
        )

        data = data.dropna(
            subset=[
                "revenue"
            ]
        )

        if data.empty:
            return None

        df = data.copy()

        df["seller"] = (
            df["seller_id"]
            .astype(str)
            .str[:9]
        )

        fig = px.bar(
            df,

            x="revenue",
            y="seller",

            orientation="h",

            hover_data={
                "seller_state": True,
                "orders": ":,.0f",
                "revenue": ":,.0f"
            },

            title="Top Sellers by Revenue",

            labels=PLOT_LABELS
        )

        fig.update_traces(
            marker_color=BLUE
        )

        fig.update_layout(
            yaxis=dict(
                autorange="reversed"
            ),

            height=360,

            xaxis_title="Revenue",
            yaxis_title=None
        )

        style_chart(fig)

        return fig


    # ==================================================
    # SELLER STATE
    # ==================================================

    if analysis == "seller_state_revenue":

        data = convert_numeric_columns(
            data,
            [
                "revenue"
            ]
        )

        data = data.dropna(
            subset=[
                "revenue"
            ]
        )

        df = data.head(15)

        if df.empty:
            return None

        fig = px.bar(
            df,

            x="revenue",
            y="seller_state",

            orientation="h",

            title="Revenue by Seller State",

            labels=PLOT_LABELS
        )

        fig.update_traces(
            marker_color=TEAL,

            hovertemplate=(
                "<b>%{y}</b><br>"
                "Revenue: %{x:,.0f} BRL"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            yaxis=dict(
                autorange="reversed"
            ),

            height=360,

            xaxis_title="Revenue",
            yaxis_title=None
        )

        style_chart(fig)

        return fig


    # ==================================================
    # MARKETPLACE GEOGRAPHY
    # ==================================================

    if analysis == "marketplace_geography":

        data = convert_numeric_columns(
            data,
            [
                "revenue"
            ]
        )

        data = data.dropna(
            subset=[
                "revenue"
            ]
        )

        if data.empty:
            return None

        fig = px.pie(
            data,

            names="state_relationship",
            values="revenue",

            hole=0.60,

            title=(
                "Same-State vs "
                "Cross-State Revenue"
            ),

            color="state_relationship",

            color_discrete_map={
                "Same State": TEAL,
                "Different State": BLUE
            },

            labels=PLOT_LABELS
        )

        fig.update_traces(
            textinfo="percent+label",

            textfont=dict(
                color=WHITE
            ),

            hovertemplate=(
                "<b>%{label}</b><br>"
                "Revenue: %{value:,.0f} BRL<br>"
                "Share: %{percent}"
                "<extra></extra>"
            )
        )

        style_pie_chart(
            fig,
            height=340
        )

        return fig


    # ==================================================
    # REPEAT PURCHASE
    # ==================================================

    if analysis == "repeat_purchase":

        data = convert_numeric_columns(
            data,
            [
                "customers"
            ]
        )

        data = data.dropna(
            subset=[
                "customers"
            ]
        )

        if data.empty:
            return None

        fig = px.pie(
            data,

            names="customer_type",
            values="customers",

            hole=0.62,

            title=(
                "Customer Repeat Purchase Mix"
            ),

            color="customer_type",

            color_discrete_map={
                "Repeat Customer": TEAL,
                "One-Time Customer": SLATE
            },

            labels=PLOT_LABELS
        )

        fig.update_traces(
            textinfo="percent+label",

            textfont=dict(
                color=WHITE
            ),

            hovertemplate=(
                "<b>%{label}</b><br>"
                "Customers: %{value:,.0f}<br>"
                "Share: %{percent}"
                "<extra></extra>"
            )
        )

        style_pie_chart(
            fig,
            height=340
        )

        return fig


    # ==================================================
    # ORDERS PER CUSTOMER
    # ==================================================

    if analysis == "orders_per_customer":

        data = convert_numeric_columns(
            data,
            [
                "customers"
            ]
        )

        data = data.dropna(
            subset=[
                "customers"
            ]
        )

        if data.empty:
            return None

        fig = px.bar(
            data,

            x="order_bucket",
            y="customers",

            title="Orders per Customer",

            labels=PLOT_LABELS
        )

        fig.update_traces(
            marker_color=BLUE
        )

        fig.update_layout(
            height=330,

            xaxis_title="Orders per Customer",
            yaxis_title="Customers"
        )

        style_chart(fig)

        return fig


    # ==================================================
    # RFM SEGMENTS
    # ==================================================

    if analysis == "rfm_segments":

        data = convert_numeric_columns(
            data,
            [
                "customers",
                "avg_recency",
                "avg_frequency",
                "avg_monetary"
            ]
        )

        data = data.dropna(
            subset=[
                "customers"
            ]
        )

        if data.empty:
            return None

        fig = px.bar(
            data,

            x="customers",
            y="customer_segment",

            orientation="h",

            hover_data={
                "avg_recency": ":.1f",
                "avg_frequency": ":.2f",
                "avg_monetary": ":,.2f"
            },

            title="RFM Customer Segments",

            labels=PLOT_LABELS
        )

        fig.update_traces(
            marker_color=TEAL
        )

        fig.update_layout(
            yaxis=dict(
                autorange="reversed"
            ),

            height=360,

            xaxis_title="Customers",
            yaxis_title=None
        )

        style_chart(fig)

        return fig


    # ==================================================
    # COHORT RETENTION
    # ==================================================

    if analysis == "cohort_retention":

        data = convert_numeric_columns(
            data,
            [
                "cohort_index",
                "retention_rate",
                "cohort_size"
            ]
        )

        data = data.dropna(
            subset=[
                "cohort_index",
                "retention_rate"
            ]
        )

        if data.empty:
            return None

        df = data.copy()

        cohort_sizes = (
            df[
                [
                    "cohort_month",
                    "cohort_size"
                ]
            ]
            .drop_duplicates()
            .sort_values(
                "cohort_size",
                ascending=False
            )
            .head(6)
        )

        selected_cohorts = (
            cohort_sizes[
                "cohort_month"
            ]
            .tolist()
        )

        df = df[
            df["cohort_month"].isin(
                selected_cohorts
            )
        ]

        df = df[
            (
                df["cohort_index"] > 0
            )
            &
            (
                df["cohort_index"] <= 6
            )
        ]

        if df.empty:
            return None

        df["cohort"] = (
            df["cohort_month"]
            .astype(str)
            .str[:7]
        )

        fig = px.line(
            df,

            x="cohort_index",
            y="retention_rate",

            color="cohort",

            markers=True,

            title=(
                "Customer Cohort Retention "
                "After Acquisition"
            ),

            labels=PLOT_LABELS
        )

        fig.update_layout(
            height=380,

            xaxis_title=(
                "Months Since First Purchase"
            ),

            yaxis_title="Retention Rate"
        )

        style_chart(fig)

        return fig


    # ==================================================
    # DELIVERY STATUS
    # ==================================================

    if analysis == "delivery_status":

        data = convert_numeric_columns(
            data,
            [
                "orders"
            ]
        )

        data = data.dropna(
            subset=[
                "orders"
            ]
        )

        if data.empty:
            return None

        fig = px.pie(
            data,

            names="delivery_status",
            values="orders",

            hole=0.62,

            title="Delivery Status",

            color="delivery_status",

            color_discrete_map={
                "On Time": TEAL,
                "Late": RED
            },

            labels=PLOT_LABELS
        )

        fig.update_traces(
            textinfo="percent+label",

            textfont=dict(
                color=WHITE
            ),

            hovertemplate=(
                "<b>%{label}</b><br>"
                "Orders: %{value:,.0f}<br>"
                "Share: %{percent}"
                "<extra></extra>"
            )
        )

        style_pie_chart(
            fig,
            height=340
        )

        return fig


    # ==================================================
    # REVIEW VS DELIVERY
    # ==================================================

    if analysis == "review_vs_delivery":

        data = convert_numeric_columns(
            data,
            [
                "average_review_score"
            ]
        )

        data = data.dropna(
            subset=[
                "average_review_score"
            ]
        )

        if data.empty:
            return None

        colors = []

        for status in data["delivery_status"]:

            if status == "Late":

                colors.append(
                    RED
                )

            else:

                colors.append(
                    TEAL
                )

        fig = px.bar(
            data,

            x="delivery_status",
            y="average_review_score",

            text_auto=".2f",

            title=(
                "Review Score: "
                "On-Time vs Late"
            ),

            labels=PLOT_LABELS
        )

        fig.update_traces(
            marker_color=colors,

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Average Review Score: %{y:.2f}"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            yaxis_range=[
                0,
                5
            ],

            height=330,

            xaxis_title=None,

            yaxis_title=(
                "Average Review Score"
            )
        )

        style_chart(fig)

        return fig


    # ==================================================
    # LATE DELIVERY BY STATE
    # ==================================================

    if analysis == "late_delivery_by_state":

        data = convert_numeric_columns(
            data,
            [
                "late_delivery_rate"
            ]
        )

        data = data.dropna(
            subset=[
                "late_delivery_rate"
            ]
        )

        if data.empty:
            return None

        fig = px.bar(
            data,

            x="late_delivery_rate",
            y="customer_state",

            orientation="h",

            title=(
                "Late Delivery Rate by State"
            ),

            labels=PLOT_LABELS
        )

        fig.update_traces(
            marker_color=RED,

            hovertemplate=(
                "<b>%{y}</b><br>"
                "Late Delivery Rate: %{x:.1%}"
                "<extra></extra>"
            )
        )

        fig.update_xaxes(
            tickformat=".0%"
        )

        fig.update_layout(
            yaxis=dict(
                autorange="reversed"
            ),

            height=390,

            xaxis_title=(
                "Late Delivery Rate"
            ),

            yaxis_title=None
        )

        style_chart(fig)

        return fig


    # ==================================================
    # DELIVERY DAYS BY STATE
    # ==================================================

    if analysis == "delivery_days_by_state":

        data = convert_numeric_columns(
            data,
            [
                "average_delivery_days"
            ]
        )

        data = data.dropna(
            subset=[
                "average_delivery_days"
            ]
        )

        df = data.head(15)

        if df.empty:
            return None

        fig = px.bar(
            df,

            x="average_delivery_days",
            y="customer_state",

            orientation="h",

            title=(
                "Average Delivery Time by State"
            ),

            labels=PLOT_LABELS
        )

        fig.update_traces(
            marker_color=AMBER,

            hovertemplate=(
                "<b>%{y}</b><br>"
                "Average Delivery Days: %{x:.1f}"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            yaxis=dict(
                autorange="reversed"
            ),

            height=380,

            xaxis_title=(
                "Average Delivery Days"
            ),

            yaxis_title=None
        )

        style_chart(fig)

        return fig


    # ==================================================
    # FREIGHT BY STATE
    # ==================================================

    if analysis == "freight_by_state":

        data = convert_numeric_columns(
            data,
            [
                "average_freight_value"
            ]
        )

        data = data.dropna(
            subset=[
                "average_freight_value"
            ]
        )

        df = data.head(15)

        if df.empty:
            return None

        fig = px.bar(
            df,

            x="average_freight_value",
            y="customer_state",

            orientation="h",

            title=(
                "Average Freight Value by State"
            ),

            labels=PLOT_LABELS
        )

        fig.update_traces(
            marker_color=AMBER,

            hovertemplate=(
                "<b>%{y}</b><br>"
                "Average Freight Value: %{x:,.2f} BRL"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            yaxis=dict(
                autorange="reversed"
            ),

            height=380,

            xaxis_title=(
                "Average Freight Value"
            ),

            yaxis_title=None
        )

        style_chart(fig)

        return fig


    # ==================================================
    # DELAY SEVERITY
    # ==================================================

    if analysis == "delay_severity_reviews":

        data = convert_numeric_columns(
            data,
            [
                "average_review_score"
            ]
        )

        data = data.dropna(
            subset=[
                "average_review_score"
            ]
        )

        if data.empty:
            return None

        order = [
            "On Time",
            "1-3 Days Late",
            "4-7 Days Late",
            "8-14 Days Late",
            "15+ Days Late"
        ]

        color_map = {
            "On Time": TEAL,
            "1-3 Days Late": AMBER,
            "4-7 Days Late": AMBER,
            "8-14 Days Late": RED,
            "15+ Days Late": RED
        }

        colors = [
            color_map.get(
                group,
                SLATE
            )

            for group
            in data["delay_group"]
        ]

        fig = px.bar(
            data,

            x="delay_group",
            y="average_review_score",

            text_auto=".2f",

            category_orders={
                "delay_group": order
            },

            title=(
                "Review Score by "
                "Delivery Delay Severity"
            ),

            labels=PLOT_LABELS
        )

        fig.update_traces(
            marker_color=colors,

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Average Review Score: %{y:.2f}"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            height=340,

            yaxis_range=[
                0,
                5
            ],

            xaxis_title=None,

            yaxis_title=(
                "Average Review Score"
            )
        )

        style_chart(fig)

        return fig


    # ==================================================
    # DELIVERY TIME VS REVIEW
    # ==================================================

    if analysis == "delivery_time_by_review":

        data = convert_numeric_columns(
            data,
            [
                "review_score",
                "average_delivery_days"
            ]
        )

        data = data.dropna(
            subset=[
                "review_score",
                "average_delivery_days"
            ]
        )

        if data.empty:
            return None

        fig = px.line(
            data,

            x="review_score",
            y="average_delivery_days",

            markers=True,

            title=(
                "Delivery Time by "
                "Review Score"
            ),

            labels=PLOT_LABELS
        )

        fig.update_traces(
            line=dict(
                color=RED,
                width=3
            ),

            marker=dict(
                size=8
            ),

            hovertemplate=(
                "Review Score: %{x}<br>"
                "Average Delivery Days: %{y:.1f}"
                "<extra></extra>"
            )
        )

        fig.update_layout(
            height=330,

            xaxis_title="Review Score",

            yaxis_title=(
                "Average Delivery Days"
            )
        )

        style_chart(fig)

        return fig


    return None


# ==================================================
# HEADER
# ==================================================

header_left, header_center, header_right = st.columns(
    [1, 3, 1]
)

with header_center:

    logo_left, logo_col, logo_right = st.columns(
        [1.2, 1.6, 1.2]
    )

    with logo_col:

        st.image(
            "assets/olist_logo.png",
            use_container_width=True
        )

    st.markdown(
        "<h1 style='"
        "text-align:center;"
        "color:#F8FAFC;"
        "font-size:40px;"
        "font-weight:800;"
        "line-height:1.1;"
        "margin-top:-8px;"
        "margin-bottom:5px;"
        "'>"
        "Olist AI Business Analyst"
        "</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='"
        "text-align:center;"
        "color:#7C8AA5;"
        "font-size:15px;"
        "margin-top:0px;"
        "margin-bottom:20px;"
        "'>"
        "Data exploration powered by SQL, Python and Gemini"
        "</p>",
        unsafe_allow_html=True
    )


# ==================================================
# FILTER
# ==================================================

states_df = get_states()

state_options = (
    ["All"]
    + states_df[
        "customer_state"
    ].tolist()
)

filter_left, filter_col = st.columns(
    [5, 1.3]
)

with filter_col:

    selected_state = st.selectbox(
        "CUSTOMER STATE",
        state_options
    )


# ==================================================
# KPI DATA
# ==================================================

total_revenue = get_total_revenue(
    selected_state
)

total_orders = get_total_orders(
    selected_state
)

average_order_value = (
    get_average_order_value(
        selected_state
    )
)

late_delivery_rate = (
    get_late_delivery_rate(
        selected_state
    )
)

average_review_score = (
    get_average_review_score(
        selected_state
    )
)


# ==================================================
# KPI CARDS
# ==================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

k1, k2, k3, k4, k5 = st.columns(5)


def show_kpi(
    container,
    label,
    value,
    color
):

    html = (
        f'<div class="kpi-card">'
        f'<div class="kpi-accent" '
        f'style="background:{color};"></div>'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'</div>'
    )

    with container:

        st.markdown(
            html,
            unsafe_allow_html=True
        )


show_kpi(
    k1,
    "Total Revenue",
    f"{total_revenue / 1_000_000:.2f}M BRL",
    BLUE
)

show_kpi(
    k2,
    "Delivered Orders",
    f"{total_orders / 1_000:.1f}K",
    BLUE
)

show_kpi(
    k3,
    "Average Order Value",
    f"{average_order_value:.2f} BRL",
    TEAL
)

show_kpi(
    k4,
    "Late Delivery Rate",
    f"{late_delivery_rate:.2%}",
    RED
)

show_kpi(
    k5,
    "Average Review",
    f"{average_review_score:.2f} / 5",
    AMBER
)


# ==================================================
# BUSINESS PERFORMANCE
# ==================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">'
    'Business Performance'
    '</div>'
    '<div class="section-subtitle">'
    'Sales momentum and product performance'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# MONTHLY REVENUE
# ==================================================

monthly = get_monthly_revenue(
    selected_state
)

monthly = convert_numeric_columns(
    monthly,
    [
        "revenue"
    ]
)

monthly = monthly.dropna(
    subset=[
        "revenue"
    ]
)

if monthly.empty:

    st.info(
        "Not enough monthly revenue data "
        f"is available for {selected_state}."
    )

else:

    fig_monthly = px.line(
        monthly,

        x="month",
        y="revenue",

        markers=True,

        title="Monthly Revenue Trend",

        labels=PLOT_LABELS
    )

    fig_monthly.update_traces(
        line=dict(
            color=BLUE,
            width=3
        ),

        marker=dict(
            size=5,
            color=TEAL
        ),

        hovertemplate=(
            "<b>%{x}</b><br>"
            "Revenue: %{y:,.0f} BRL"
            "<extra></extra>"
        )
    )

    fig_monthly.update_layout(
        height=280,

        xaxis_title=None,

        yaxis_title="Revenue",

        hovermode="x unified"
    )

    style_chart(
        fig_monthly
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )


# ==================================================
# PRODUCT + CUSTOMER INTELLIGENCE
# ==================================================

left_col, right_col = st.columns(
    [1.25, 0.75]
)


# ==================================================
# CATEGORY PERFORMANCE
# ==================================================

with left_col:

    category_data = (
        get_category_sales_vs_reviews(
            selected_state
        )
    )

    category_data = (
        convert_numeric_columns(
            category_data,

            [
                "revenue",
                "average_review_score",
                "items_sold",
                "total_reviews"
            ]
        )
    )

    category_data = (
        category_data.dropna(
            subset=[
                "revenue",
                "average_review_score",
                "items_sold"
            ]
        )
    )

    category_data = category_data[
        category_data[
            "items_sold"
        ] > 0
    ]


    if category_data.empty:

        st.info(
            "Not enough category data is available "
            f"for the selected state ({selected_state})."
        )

    else:

        fig_category = px.scatter(
            category_data,

            x="revenue",

            y="average_review_score",

            size="items_sold",

            hover_name="product_category",

            hover_data={
                "revenue": ":,.0f",
                "average_review_score": ":.2f",
                "items_sold": ":,.0f",
                "total_reviews": ":,.0f"
            },

            title=(
                "Category Revenue vs "
                "Customer Satisfaction"
            ),

            labels=PLOT_LABELS
        )

        fig_category.update_traces(
            marker=dict(
                color=BLUE,
                opacity=0.75,

                line=dict(
                    color=WHITE,
                    width=1
                )
            )
        )

        fig_category.update_layout(
            height=350,

            yaxis_range=[
                0,
                5
            ],

            xaxis_title="Revenue",

            yaxis_title=(
                "Average Review Score"
            )
        )

        style_chart(
            fig_category
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )


# ==================================================
# REPEAT PURCHASE
# ==================================================

with right_col:

    repeat_data = (
        get_repeat_purchase_summary(
            selected_state
        )
    )

    repeat_data = convert_numeric_columns(
        repeat_data,
        [
            "customers"
        ]
    )

    repeat_data = repeat_data.dropna(
        subset=[
            "customers"
        ]
    )


    if repeat_data.empty:

        st.info(
            "Not enough repeat-purchase data is "
            f"available for {selected_state}."
        )

    else:

        fig_repeat = px.pie(
            repeat_data,

            names="customer_type",

            values="customers",

            hole=0.65,

            title=(
                "Customer Purchase Behavior"
            ),

            color="customer_type",

            color_discrete_map={
                "Repeat Customer": TEAL,
                "One-Time Customer": SLATE
            },

            labels=PLOT_LABELS
        )

        fig_repeat.update_traces(
            textinfo="percent",

            textfont=dict(
                color=WHITE
            ),

            hovertemplate=(
                "<b>%{label}</b><br>"
                "Customers: %{value:,.0f}<br>"
                "Share: %{percent}"
                "<extra></extra>"
            )
        )

        style_pie_chart(
            fig_repeat,
            height=350
        )

        st.plotly_chart(
            fig_repeat,
            use_container_width=True
        )


# ==================================================
# CUSTOMER INTELLIGENCE
# ==================================================

st.markdown(
    '<div class="section-title">'
    'Customer & Retention Intelligence'
    '</div>'
    '<div class="section-subtitle">'
    'Engagement, lifecycle and repeat behavior'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# RFM
# ==================================================

rfm_data = get_rfm_segments(
    selected_state
)

rfm_data = convert_numeric_columns(
    rfm_data,

    [
        "customers",
        "avg_recency",
        "avg_frequency",
        "avg_monetary"
    ]
)

rfm_data = rfm_data.dropna(
    subset=[
        "customers"
    ]
)


if rfm_data.empty:

    st.info(
        "Not enough RFM data is available "
        f"for {selected_state}."
    )

else:

    fig_rfm = px.bar(
        rfm_data,

        x="customers",
        y="customer_segment",

        orientation="h",

        hover_data={
            "customers": ":,.0f",
            "avg_recency": ":.1f",
            "avg_frequency": ":.2f",
            "avg_monetary": ":,.2f"
        },

        title="RFM Customer Segments",

        labels=PLOT_LABELS
    )

    fig_rfm.update_traces(
        marker_color=TEAL
    )

    fig_rfm.update_layout(
        yaxis=dict(
            autorange="reversed"
        ),

        height=310,

        xaxis_title="Customers",

        yaxis_title=None
    )

    style_chart(
        fig_rfm
    )

    st.plotly_chart(
        fig_rfm,
        use_container_width=True
    )


# ==================================================
# DELIVERY EXPERIENCE
# ==================================================

st.markdown(
    '<div class="section-title">'
    'Delivery & Customer Experience'
    '</div>'
    '<div class="section-subtitle">'
    'Operational performance and customer satisfaction'
    '</div>',
    unsafe_allow_html=True
)

delivery_left, delivery_right = st.columns(2)


# ==================================================
# DELAY SEVERITY
# ==================================================

with delivery_left:

    delay_data = (
        get_delay_severity_reviews(
            selected_state
        )
    )

    delay_data = convert_numeric_columns(
        delay_data,
        [
            "average_review_score"
        ]
    )

    delay_data = delay_data.dropna(
        subset=[
            "average_review_score"
        ]
    )


    if delay_data.empty:

        st.info(
            "Not enough delivery-delay data is "
            f"available for {selected_state}."
        )

    else:

        delay_order = [
            "On Time",
            "1-3 Days Late",
            "4-7 Days Late",
            "8-14 Days Late",
            "15+ Days Late"
        ]

        delay_color_map = {
            "On Time": TEAL,
            "1-3 Days Late": AMBER,
            "4-7 Days Late": AMBER,
            "8-14 Days Late": RED,
            "15+ Days Late": RED
        }

        delay_colors = [
            delay_color_map.get(
                group,
                SLATE
            )

            for group
            in delay_data[
                "delay_group"
            ]
        ]

        fig_delay = px.bar(
            delay_data,

            x="delay_group",

            y="average_review_score",

            text_auto=".2f",

            category_orders={
                "delay_group": delay_order
            },

            title=(
                "Review Score by "
                "Delay Severity"
            ),

            labels=PLOT_LABELS
        )

        fig_delay.update_traces(
            marker_color=delay_colors,

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Average Review Score: %{y:.2f}"
                "<extra></extra>"
            )
        )

        fig_delay.update_layout(
            height=310,

            yaxis_range=[
                0,
                5
            ],

            xaxis_title=None,

            yaxis_title=(
                "Average Review Score"
            )
        )

        style_chart(
            fig_delay
        )

        st.plotly_chart(
            fig_delay,
            use_container_width=True
        )


# ==================================================
# LATE DELIVERY BY STATE
# ==================================================

with delivery_right:

    late_state = (
        get_late_delivery_by_state()
    )

    late_state = convert_numeric_columns(
        late_state,
        [
            "late_delivery_rate"
        ]
    )

    late_state = late_state.dropna(
        subset=[
            "late_delivery_rate"
        ]
    )


    if late_state.empty:

        st.info(
            "Late-delivery state data "
            "is not available."
        )

    else:

        fig_state = px.bar(
            late_state.head(10),

            x="late_delivery_rate",

            y="customer_state",

            orientation="h",

            title=(
                "States with Highest "
                "Late Delivery Rates"
            ),

            labels=PLOT_LABELS
        )

        fig_state.update_traces(
            marker_color=RED,

            hovertemplate=(
                "<b>Customer State: %{y}</b><br>"
                "Late Delivery Rate: %{x:.1%}"
                "<extra></extra>"
            )
        )

        fig_state.update_xaxes(
            tickformat=".0%"
        )

        fig_state.update_layout(
            yaxis=dict(
                autorange="reversed"
            ),

            height=310,

            xaxis_title=(
                "Late Delivery Rate"
            ),

            yaxis_title=None
        )

        style_chart(
            fig_state
        )

        st.plotly_chart(
            fig_state,
            use_container_width=True
        )


# ==================================================
# AI ANALYST PANEL
# ==================================================

ai_html = (
    f'<div style="'
    f'margin-top:18px;'
    f'padding:22px 24px;'
    f'border-radius:16px;'
    f'border:1px solid {BORDER};'
    f'background:linear-gradient('
    f'135deg,'
    f'rgba(91,140,255,0.10),'
    f'rgba(49,208,170,0.06)'
    f');'
    f'">'

    f'<div style="'
    f'color:{WHITE};'
    f'font-size:23px;'
    f'font-weight:800;'
    f'">'

    f'Ask the AI Business Analyst'

    f'</div>'

    f'<div style="'
    f'color:{TEXT};'
    f'font-size:13px;'
    f'margin-top:7px;'
    f'">'

    f'Explore sales, customers, retention, products, sellers, '
    f'geography and delivery performance using natural language.'

    f'</div>'

    f'</div>'
)

st.markdown(
    ai_html,
    unsafe_allow_html=True
)


# ==================================================
# SUGGESTED QUESTIONS
# ==================================================

st.markdown(
    f'<div style="'
    f'color:{MUTED};'
    f'margin-top:14px;'
    f'margin-bottom:7px;'
    f'font-size:12px;'
    f'">'
    f'Try questions such as:'
    f'</div>',
    unsafe_allow_html=True
)

st.caption(
    "• Why is customer retention a concern for Olist?  "
    "• Which categories combine high revenue with weak reviews?  "
    "• Is Olist mainly a local marketplace?  "
    "• How does delay severity affect customer satisfaction?"
)


# ==================================================
# USER QUESTION
# ==================================================

user_question = st.text_input(
    "Business question",

    placeholder=(
        "Example: Which categories combine "
        "high revenue with low customer satisfaction?"
    )
)


# ==================================================
# RUN AI ANALYSIS
# ==================================================

if user_question:

    with st.spinner(
        "Analyzing Olist business data..."
    ):

        try:

            result = analyze_question(
                user_question,
                selected_state
            )

            answer = result[
                "answer"
            ]

            plan = result[
                "plan"
            ]

            analysis_data = result[
                "data"
            ]


            # ==========================================
            # RESPONSE
            # ==========================================

            st.markdown(
                "### AI Business Insight"
            )

            st.markdown(
                answer
            )


            # ==========================================
            # SELECTED ANALYSIS
            # ==========================================

            analysis_name = (
                plan
                .get(
                    "analysis",
                    "none"
                )
                .replace(
                    "_",
                    " "
                )
                .title()
            )

            if analysis_name != "None":

                st.caption(
                    f"Selected analysis: "
                    f"{analysis_name}"
                )


            # ==========================================
            # DYNAMIC VISUALIZATION
            # ==========================================

            dynamic_fig = (
                create_dynamic_chart(
                    plan,
                    analysis_data
                )
            )

            if dynamic_fig is not None:

                st.markdown(
                    "#### AI-Generated Visualization"
                )

                st.plotly_chart(
                    dynamic_fig,
                    use_container_width=True
                )

                st.caption(
                    "Visualization generated from "
                    "approved SQL-derived Olist data."
                )

            else:

                st.caption(
                    "No additional visualization "
                    "is available for this analysis."
                )


        except Exception as error:

            st.error(
                f"AI assistant error: {error}"
            )