from pathlib import Path
import pandas as pd

from src.analytics import (
    get_states,
    get_total_revenue,
    get_total_orders,
    get_average_order_value,
    get_late_delivery_rate,
    get_average_review_score,
    get_monthly_revenue,
    get_monthly_growth,
    get_revenue_by_state,
    get_orders_by_state,
    get_aov_by_state,
    get_state_performance,
    get_top_categories_by_revenue,
    get_category_sales_vs_reviews,
    get_low_rated_high_sales_products,
    get_top_sellers,
    get_seller_state_revenue,
    get_marketplace_geography,
    get_repeat_purchase_summary,
    get_orders_per_customer,
    get_rfm_segments,
    get_cohort_retention,
    get_delivery_status,
    get_review_by_delivery_status,
    get_late_delivery_by_state,
    get_delivery_days_by_state,
    get_freight_by_state,
    get_delay_severity_reviews,
    get_delivery_time_by_review
)


BASE_DIR = Path("data_cache")

BASE_DIR.mkdir(
    exist_ok=True
)


def save_df(
    name,
    dataframe,
    state=None
):

    folder = BASE_DIR / name

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = (
        "ALL.csv"
        if state is None
        else f"{state}.csv"
    )

    path = folder / filename

    dataframe.to_csv(
        path,
        index=False
    )

    print(
        f"Saved: {path}"
    )


# ==================================================
# STATES
# ==================================================

states_df = get_states()

states = [
    "All"
] + states_df[
    "customer_state"
].tolist()


states_df.to_csv(
    BASE_DIR / "states.csv",
    index=False
)


# ==================================================
# KPI EXPORT
# ==================================================

kpi_rows = []


for state in states:

    print(
        f"\nExporting KPIs: {state}"
    )

    kpi_rows.append(
        {
            "state": state,

            "total_revenue":
                get_total_revenue(
                    state
                ),

            "total_orders":
                get_total_orders(
                    state
                ),

            "average_order_value":
                get_average_order_value(
                    state
                ),

            "late_delivery_rate":
                get_late_delivery_rate(
                    state
                ),

            "average_review_score":
                get_average_review_score(
                    state
                )
        }
    )


pd.DataFrame(
    kpi_rows
).to_csv(
    BASE_DIR / "kpis.csv",
    index=False
)


# ==================================================
# ANALYSES THAT USE STATE FILTER
# ==================================================

state_functions = {
    "monthly_revenue":
        get_monthly_revenue,

    "monthly_growth":
        get_monthly_growth,

    "top_categories":
        get_top_categories_by_revenue,

    "category_sales_reviews":
        get_category_sales_vs_reviews,

    "top_sellers":
        get_top_sellers,

    "seller_state_revenue":
        get_seller_state_revenue,

    "marketplace_geography":
        get_marketplace_geography,

    "repeat_purchase":
        get_repeat_purchase_summary,

    "orders_per_customer":
        get_orders_per_customer,

    "rfm_segments":
        get_rfm_segments,

    "cohort_retention":
        get_cohort_retention,

    "delivery_status":
        get_delivery_status,

    "review_delivery":
        get_review_by_delivery_status,

    "delay_severity":
        get_delay_severity_reviews,

    "delivery_time_review":
        get_delivery_time_by_review
}


for state in states:

    file_state = (
        "ALL"
        if state == "All"
        else state
    )

    print(
        f"\nEXPORTING STATE: {state}"
    )

    for name, function in (
        state_functions.items()
    ):

        try:

            df = function(
                state
            )

            save_df(
                name,
                df,
                file_state
            )

        except Exception as error:

            print(
                f"ERROR "
                f"{name} - "
                f"{state}: "
                f"{error}"
            )


# ==================================================
# GLOBAL ANALYSES
# ==================================================

global_functions = {
    "revenue_by_state":
        get_revenue_by_state,

    "orders_by_state":
        get_orders_by_state,

    "aov_by_state":
        get_aov_by_state,

    "state_performance":
        get_state_performance,

    "low_rated_products":
        get_low_rated_high_sales_products,

    "late_delivery_by_state":
        get_late_delivery_by_state,

    "delivery_days_by_state":
        get_delivery_days_by_state,

    "freight_by_state":
        get_freight_by_state
}


for name, function in (
    global_functions.items()
):

    print(
        f"\nExporting global: {name}"
    )

    try:

        df = function()

        save_df(
            name,
            df
        )

    except Exception as error:

        print(
            f"ERROR "
            f"{name}: "
            f"{error}"
        )


print(
    "\n============================"
)

print(
    "EXPORT FINISHED"
)

print(
    "============================"
)