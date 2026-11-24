from pathlib import Path
import pandas as pd


# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data_cache"


# ==================================================
# HELPERS
# ==================================================

def normalize_state(selected_state):

    if selected_state == "All":
        return "ALL"

    return selected_state


def load_csv(path):

    return pd.read_csv(
        path
    )


def load_state_file(
    folder_name,
    selected_state="All"
):

    state = normalize_state(
        selected_state
    )

    path = (
        DATA_DIR
        / folder_name
        / f"{state}.csv"
    )

    if not path.exists():

        raise FileNotFoundError(
            f"Data file not found: {path}"
        )

    return load_csv(
        path
    )


def load_global_file(
    folder_name
):

    path = (
        DATA_DIR
        / folder_name
        / "ALL.csv"
    )

    if not path.exists():

        raise FileNotFoundError(
            f"Data file not found: {path}"
        )

    return load_csv(
        path
    )


# ==================================================
# STATES
# ==================================================

def get_states():

    path = (
        DATA_DIR
        / "states.csv"
    )

    return load_csv(
        path
    )


# ==================================================
# KPIs
# ==================================================

def get_kpi_row(
    selected_state="All"
):

    path = (
        DATA_DIR
        / "kpis.csv"
    )

    df = load_csv(
        path
    )

    row = df[
        df["state"]
        == selected_state
    ]

    if row.empty:

        raise ValueError(
            f"No KPI data found for state: "
            f"{selected_state}"
        )

    return row.iloc[0]


def get_total_revenue(
    selected_state="All"
):

    row = get_kpi_row(
        selected_state
    )

    return row[
        "total_revenue"
    ]


def get_total_orders(
    selected_state="All"
):

    row = get_kpi_row(
        selected_state
    )

    return row[
        "total_orders"
    ]


def get_average_order_value(
    selected_state="All"
):

    row = get_kpi_row(
        selected_state
    )

    return row[
        "average_order_value"
    ]


def get_late_delivery_rate(
    selected_state="All"
):

    row = get_kpi_row(
        selected_state
    )

    return row[
        "late_delivery_rate"
    ]


def get_average_review_score(
    selected_state="All"
):

    row = get_kpi_row(
        selected_state
    )

    return row[
        "average_review_score"
    ]


# ==================================================
# SALES
# ==================================================

def get_monthly_revenue(
    selected_state="All"
):

    return load_state_file(
        "monthly_revenue",
        selected_state
    )


def get_monthly_growth(
    selected_state="All"
):

    return load_state_file(
        "monthly_growth",
        selected_state
    )


# ==================================================
# STATE PERFORMANCE
# ==================================================

def get_revenue_by_state():

    return load_global_file(
        "revenue_by_state"
    )


def get_orders_by_state():

    return load_global_file(
        "orders_by_state"
    )


def get_aov_by_state():

    return load_global_file(
        "aov_by_state"
    )


def get_state_performance():

    return load_global_file(
        "state_performance"
    )


# ==================================================
# PRODUCTS
# ==================================================

def get_top_categories_by_revenue(
    selected_state="All"
):

    return load_state_file(
        "top_categories",
        selected_state
    )


def get_category_sales_vs_reviews(
    selected_state="All"
):

    return load_state_file(
        "category_sales_reviews",
        selected_state
    )


def get_low_rated_high_sales_products():

    return load_global_file(
        "low_rated_products"
    )


# ==================================================
# SELLERS
# ==================================================

def get_top_sellers(
    selected_state="All"
):

    return load_state_file(
        "top_sellers",
        selected_state
    )


def get_seller_state_revenue(
    selected_state="All"
):

    return load_state_file(
        "seller_state_revenue",
        selected_state
    )


# ==================================================
# MARKETPLACE GEOGRAPHY
# ==================================================

def get_marketplace_geography(
    selected_state="All"
):

    return load_state_file(
        "marketplace_geography",
        selected_state
    )


# ==================================================
# CUSTOMER RETENTION
# ==================================================

def get_repeat_purchase_summary(
    selected_state="All"
):

    return load_state_file(
        "repeat_purchase",
        selected_state
    )


def get_orders_per_customer(
    selected_state="All"
):

    return load_state_file(
        "orders_per_customer",
        selected_state
    )


# ==================================================
# RFM
# ==================================================

def get_rfm_segments(
    selected_state="All"
):

    return load_state_file(
        "rfm_segments",
        selected_state
    )


# ==================================================
# COHORT RETENTION
# ==================================================

def get_cohort_retention(
    selected_state="All"
):

    return load_state_file(
        "cohort_retention",
        selected_state
    )


# ==================================================
# DELIVERY STATUS
# ==================================================

def get_delivery_status(
    selected_state="All"
):

    return load_state_file(
        "delivery_status",
        selected_state
    )


def get_review_by_delivery_status(
    selected_state="All"
):

    return load_state_file(
        "review_delivery",
        selected_state
    )


# ==================================================
# LATE DELIVERY BY STATE
# ==================================================

def get_late_delivery_by_state():

    path = (
        DATA_DIR
        / "kpis.csv"
    )

    df = load_csv(
        path
    )

    df = df[
        df["state"] != "All"
    ].copy()

    df = df[
        [
            "state",
            "total_orders",
            "late_delivery_rate"
        ]
    ]

    df = df.rename(
        columns={
            "state": "customer_state",
            "total_orders": "orders"
        }
    )

    df = df.sort_values(
        "late_delivery_rate",
        ascending=False
    )

    return df.head(15)


# ==================================================
# DELIVERY DAYS BY STATE
# ==================================================

def get_delivery_days_by_state():

    return load_global_file(
        "delivery_days_by_state"
    )


# ==================================================
# FREIGHT BY STATE
# ==================================================

def get_freight_by_state():

    return load_global_file(
        "freight_by_state"
    )


# ==================================================
# DELAY SEVERITY
# ==================================================

def get_delay_severity_reviews(
    selected_state="All"
):

    return load_state_file(
        "delay_severity",
        selected_state
    )


# ==================================================
# DELIVERY TIME VS REVIEW
# ==================================================

def get_delivery_time_by_review(
    selected_state="All"
):

    return load_state_file(
        "delivery_time_review",
        selected_state
    )