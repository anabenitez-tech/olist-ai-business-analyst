import os
import time
import json

from dotenv import load_dotenv
from google import genai

from src.analytics import (
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


# ==================================================
# ENVIRONMENT
# ==================================================

load_dotenv()


# ==================================================
# GEMINI CLIENT
# ==================================================

def get_client():

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:

        raise ValueError(
            "GEMINI_API_KEY was not found. "
            "Check your .env file."
        )

    return genai.Client(
        api_key=api_key
    )


# ==================================================
# GEMINI REQUEST
# ==================================================

def generate_with_retry(
    prompt,
    max_attempts=2
):

    client = get_client()

    for attempt in range(
        max_attempts
    ):

        try:

            response = (
                client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )
            )

            return response.text

        except Exception as error:

            error_text = str(error)

            if (
                "503" in error_text
                and attempt
                < max_attempts - 1
            ):

                time.sleep(3)

                continue

            raise error

    raise RuntimeError(
        "Gemini is temporarily unavailable."
    )


# ==================================================
# ANALYSIS PLANNER
# ==================================================

def plan_analysis(question):

    prompt = f"""
You are the analysis router for an Olist
E-Commerce Business Intelligence application.

Your job is to understand the business question
and select ONE approved analysis.

AVAILABLE ANALYSES:

monthly_revenue
monthly_growth
revenue_by_state
orders_by_state
aov_by_state
state_performance
top_categories
category_sales_vs_reviews
low_rated_products
top_sellers
seller_state_revenue
marketplace_geography
repeat_purchase
orders_per_customer
rfm_segments
cohort_retention
delivery_status
review_vs_delivery
late_delivery_by_state
delivery_days_by_state
freight_by_state
delay_severity_reviews
delivery_time_by_review
none


AVAILABLE CHART TYPES:

bar
line
pie
scatter
none


ROUTING RULES:

Revenue trend or revenue over time:
monthly_revenue + line

Month-over-month growth:
monthly_growth + line

Revenue by customer state:
revenue_by_state + bar

Orders by customer state:
orders_by_state + bar

Average order value by state:
aov_by_state + bar

Revenue compared with delivery performance:
state_performance + scatter

Top product categories by revenue:
top_categories + bar

Categories combining sales and satisfaction:
category_sales_vs_reviews + scatter

Poorly rated high-selling products:
low_rated_products + bar

Best sellers:
top_sellers + bar

Seller geography or revenue by seller state:
seller_state_revenue + bar

Local vs cross-state marketplace:
marketplace_geography + pie

Repeat customers or repeat purchase:
repeat_purchase + pie

Number of orders per customer:
orders_per_customer + bar

RFM or customer segments:
rfm_segments + bar

Retention or cohorts:
cohort_retention + line

Late vs on-time order proportions:
delivery_status + pie

Impact of late delivery on reviews:
review_vs_delivery + bar

Worst states for late deliveries:
late_delivery_by_state + bar

Delivery time by state:
delivery_days_by_state + bar

Freight or shipping cost by state:
freight_by_state + bar

Review score by delay severity:
delay_severity_reviews + bar

Delivery time compared with review score:
delivery_time_by_review + line

If no approved analysis is relevant:
none + none


Return ONLY valid JSON.

Example:

{{
    "analysis": "cohort_retention",
    "chart_type": "line"
}}


USER QUESTION:

{question}
"""

    raw_result = generate_with_retry(
        prompt
    )

    raw_result = (
        raw_result
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:

        result = json.loads(
            raw_result
        )

    except json.JSONDecodeError:

        return {
            "analysis": "none",
            "chart_type": "none"
        }

    return {
        "analysis": result.get(
            "analysis",
            "none"
        ),
        "chart_type": result.get(
            "chart_type",
            "none"
        )
    }


# ==================================================
# GET DATA FOR AI ANALYSIS
# ==================================================

def get_analysis_data(
    analysis,
    selected_state="All"
):

    if analysis == "monthly_revenue":
        return get_monthly_revenue(
            selected_state
        )

    if analysis == "monthly_growth":
        return get_monthly_growth(
            selected_state
        )

    if analysis == "revenue_by_state":
        return get_revenue_by_state()

    if analysis == "orders_by_state":
        return get_orders_by_state()

    if analysis == "aov_by_state":
        return get_aov_by_state()

    if analysis == "state_performance":
        return get_state_performance()

    if analysis == "top_categories":
        return get_top_categories_by_revenue(
            selected_state
        )

    if analysis == "category_sales_vs_reviews":
        return get_category_sales_vs_reviews(
            selected_state
        )

    if analysis == "low_rated_products":
        return get_low_rated_high_sales_products()

    if analysis == "top_sellers":
        return get_top_sellers(
            selected_state
        )

    if analysis == "seller_state_revenue":
        return get_seller_state_revenue(
            selected_state
        )

    if analysis == "marketplace_geography":
        return get_marketplace_geography(
            selected_state
        )

    if analysis == "repeat_purchase":
        return get_repeat_purchase_summary(
            selected_state
        )

    if analysis == "orders_per_customer":
        return get_orders_per_customer(
            selected_state
        )

    if analysis == "rfm_segments":
        return get_rfm_segments(
            selected_state
        )

    if analysis == "cohort_retention":
        return get_cohort_retention(
            selected_state
        )

    if analysis == "delivery_status":
        return get_delivery_status(
            selected_state
        )

    if analysis == "review_vs_delivery":
        return get_review_by_delivery_status(
            selected_state
        )

    if analysis == "late_delivery_by_state":
        return get_late_delivery_by_state()

    if analysis == "delivery_days_by_state":
        return get_delivery_days_by_state()

    if analysis == "freight_by_state":
        return get_freight_by_state()

    if analysis == "delay_severity_reviews":
        return get_delay_severity_reviews(
            selected_state
        )

    if analysis == "delivery_time_by_review":
        return get_delivery_time_by_review(
            selected_state
        )

    return None


# ==================================================
# BUSINESS OVERVIEW
# ==================================================

def build_overview(
    selected_state="All"
):

    revenue = get_total_revenue(
        selected_state
    )

    orders = get_total_orders(
        selected_state
    )

    aov = get_average_order_value(
        selected_state
    )

    late_rate = get_late_delivery_rate(
        selected_state
    )

    review = get_average_review_score(
        selected_state
    )

    return f"""
CURRENT FILTER

State:
{selected_state}


CORE BUSINESS KPIs

Revenue:
{revenue:.2f} BRL

Orders:
{orders}

Average Order Value:
{aov:.2f} BRL

Late Delivery Rate:
{late_rate:.2%}

Average Review Score:
{review:.2f}
"""


# ==================================================
# COMPLETE AI ANALYSIS
# ==================================================

def analyze_question(
    question,
    selected_state="All"
):

    plan = plan_analysis(
        question
    )

    analysis = plan.get(
        "analysis",
        "none"
    )

    data = get_analysis_data(
        analysis,
        selected_state
    )

    overview = build_overview(
        selected_state
    )

    if data is not None:

        data_text = (
            data
            .head(120)
            .to_string(
                index=False
            )
        )

    else:

        data_text = (
            "No additional approved "
            "analysis was selected."
        )

    prompt = f"""
You are an AI Business Analyst specialized
in the Olist Brazilian E-Commerce dataset.

You are analyzing REAL SQL-derived business data.

RULES:

1. Use only the supplied data.

2. Never invent values.

3. Clearly distinguish facts from interpretation.

4. Include relevant numbers.

5. Explain why the result matters for the business.

6. Identify risks, opportunities or trade-offs
   when supported by the data.

7. Keep the response concise but analytical.

8. Do not claim causation unless the data proves it.

9. Finish with a short recommendation when useful.

10. Revenue values are BRL.

11. Percentages must be presented clearly.

12. The selected dashboard state filter must
    be respected when applicable.


BUSINESS OVERVIEW:

{overview}


SELECTED ANALYSIS:

{analysis}


ANALYSIS DATA:

{data_text}


USER QUESTION:

{question}
"""

    answer = generate_with_retry(
        prompt
    )

    return {
        "answer": answer,
        "plan": plan,
        "data": data
    }


# ==================================================
# COMPATIBILITY FUNCTION
# ==================================================

def ask_analyst(
    question,
    selected_state="All"
):

    result = analyze_question(
        question,
        selected_state
    )

    return result["answer"]