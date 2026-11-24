# Olist AI Business Analyst

An interactive **AI-powered business analytics application** built with **Python, Streamlit, Plotly, SQL-derived datasets and Google Gemini**.

The project transforms the Olist Brazilian E-Commerce dataset into an interactive analytical product where users can explore business performance, customer behavior, delivery operations and marketplace dynamics, while also asking business questions in natural language.

🔗 **Live App:** https://olist-analytics-gemini.streamlit.app/

---

## Project Overview

The goal of this project is to analyze the performance of the Olist marketplace and identify business opportunities across several areas:

- Revenue and sales performance
- Customer retention and repeat purchasing
- Product and category performance
- Seller performance
- Marketplace geography
- Delivery operations
- Customer satisfaction
- AI-assisted business analysis

The project started with data preparation and analysis in **SQL Server** and was later transformed into an interactive **Streamlit analytics application**.

---

## Business Questions

The analysis focuses on questions such as:

- How is revenue evolving over time?
- Which Brazilian states generate the most revenue?
- Which product categories combine strong sales with weak customer satisfaction?
- How important are repeat customers to the business?
- Which customer segments are most valuable?
- How strong is customer retention?
- How does late delivery affect review scores?
- Which states experience the highest late-delivery rates?
- Is the marketplace mainly local or cross-state?
- Which sellers and seller regions generate the most revenue?

---

## Key Metrics

The complete Olist analysis produced the following headline metrics:

| Metric | Result |
|---|---:|
| Total Revenue | 13.22M BRL |
| Delivered Orders | 96,470 |
| Average Order Value | 137.04 BRL |
| Late Delivery Rate | 6.77% |
| Average Review Score | ~4.16 / 5 |
| On-Time Delivery Review | 4.29 / 5 |
| Late Delivery Review | 2.27 / 5 |
| Repeat Purchase Rate | ~3% |

---

## Key Business Insights

### 1. Customer retention is a major challenge

The marketplace is highly dependent on one-time buyers.

Approximately:

- **90,557 customers** made only one purchase.
- Only around **2,801 customers** returned for additional purchases.
- The overall repeat-purchase rate is approximately **3%**.

Cohort analysis also shows very weak retention after the first purchase, with most cohorts retaining less than 1% of customers in following months.

This suggests that customer acquisition is much stronger than customer retention.

---

### 2. Delivery performance strongly affects customer satisfaction

Delivery delays have a significant impact on customer reviews.

Average review score:

- **On-time deliveries:** 4.29 / 5
- **Late deliveries:** 2.27 / 5

The relationship becomes even clearer when analyzing the severity of delays: longer delivery delays are associated with increasingly poor customer satisfaction.

This indicates that logistics performance is not only an operational issue but also a major customer-experience driver.

---

### 3. Olist operates as a highly interconnected marketplace

A large share of transactions occur between customers and sellers located in different Brazilian states.

Approximately:

- **68.73% of revenue** comes from cross-state transactions.
- **31.27% of revenue** comes from same-state transactions.

This highlights the importance of national logistics and fulfillment capabilities.

---

### 4. Product performance should not be evaluated using revenue alone

Some product categories generate strong revenue while receiving weaker customer reviews.

Combining:

- Revenue
- Units sold
- Review score
- Number of reviews

helps identify categories that may represent opportunities for product-quality, seller-quality or fulfillment improvements.

---

### 5. Geographic performance varies considerably

Customer states differ significantly in:

- Revenue
- Order volume
- Average order value
- Freight cost
- Delivery time
- Late-delivery rate

This means that geographic segmentation can help identify operational bottlenecks and market opportunities.

---

## AI Business Analyst

The application includes a natural-language AI assistant powered by **Google Gemini**.

Instead of allowing the AI model to execute unrestricted queries, the application uses a controlled analytical architecture.

The AI first identifies the most appropriate analysis for the user's question and then selects from a predefined set of approved business analyses.

Examples include:

- Monthly revenue
- Revenue growth
- Revenue by state
- State performance
- Top product categories
- Category sales vs reviews
- Seller performance
- Customer repeat purchasing
- RFM segmentation
- Cohort retention
- Delivery performance
- Review score vs delivery status
- Freight analysis
- Delay severity

This approach makes the application more predictable, secure and explainable.

---

## Example Questions

Users can ask questions such as:

> Why is customer retention a concern for Olist?

> Which categories combine high revenue with weak customer satisfaction?

> Which customer states have the highest late delivery rates?

> How does delivery delay affect customer satisfaction?

> Is Olist mainly a local marketplace?

> Which sellers generate the most revenue?

The AI assistant selects the relevant analysis, interprets the results and can generate a supporting visualization.

---

## Dashboard Features

The Streamlit application includes:

### Business Performance

- Total revenue
- Delivered orders
- Average order value
- Late-delivery rate
- Average review score
- Monthly revenue trends

### Product Intelligence

- Category revenue
- Units sold
- Customer satisfaction
- Category performance comparison

### Customer Intelligence

- Repeat purchase analysis
- Customer purchase behavior
- RFM segmentation
- Cohort retention

### Delivery & Customer Experience

- On-time vs late delivery performance
- Delay severity
- Review score impact
- Late-delivery rates by state

### Interactive Filtering

Users can filter the dashboard by Brazilian customer state.

The application's KPIs, charts and AI analysis adapt to the selected market.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| SQL Server | Data cleaning, transformation and business analysis |
| SQL | Analytical queries and dataset preparation |
| Python | Application and analytics logic |
| Pandas | Data manipulation |
| Streamlit | Interactive web application |
| Plotly | Interactive visualizations |
| Google Gemini | AI business analyst |
| Git | Version control |
| GitHub | Source-code hosting |
| Streamlit Community Cloud | Application deployment |

---

## Project Architecture

```text
SQL Server
    │
    ▼
Analytical SQL Queries
    │
    ▼
Aggregated Business Datasets
    │
    ▼
CSV Data Cache
    │
    ▼
Python / Pandas Analytics Layer
    │
    ├──────────────► Plotly Visualizations
    │
    └──────────────► Gemini AI Analyst
                         │
                         ▼
                  Business Insights
    │
    ▼
Streamlit Application
    │
    ▼
Streamlit Community Cloud
```

---

## Project Structure

```text
olist-ai-business-analyst/
│
├── app.py
│
├── assets/
│   └── olist_logo.png
│
├── data_cache/
│   ├── states.csv
│   ├── kpis.csv
│   ├── monthly_revenue/
│   ├── monthly_growth/
│   ├── top_categories/
│   ├── category_sales_reviews/
│   ├── repeat_purchase/
│   ├── rfm_segments/
│   ├── cohort_retention/
│   ├── delivery_status/
│   └── ...
│
├── src/
│   ├── analytics.py
│   └── ai_assistant.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Data Pipeline

The original analytical workflow was developed using SQL Server.

For public deployment, the architecture was adapted so the Streamlit application does not require access to a local SQL Server instance.

The deployment pipeline is:

```text
SQL Server
→ Data aggregation
→ CSV export
→ data_cache
→ Pandas
→ Streamlit
```

This allows the public application to run entirely on Streamlit Community Cloud while preserving the analytical results generated from SQL.

---

## SQL Analysis

The original SQL project included dedicated analyses for:

- Database setup
- Data-quality checks
- Sales analysis
- Customer analysis
- Product analysis
- Delivery analysis
- Power BI datasets
- Product-level analytical datasets

The SQL layer was responsible for transforming the raw Olist data into business-ready analytical datasets.

---

## Customer Segmentation

The project includes **RFM analysis** based on:

- **Recency** — how recently the customer purchased
- **Frequency** — how often the customer purchased
- **Monetary Value** — how much revenue the customer generated

This allows customers to be grouped into behavioral segments and provides a stronger view of customer value than simple order counts.

---

## Cohort Retention Analysis

Customers are grouped according to their first purchase month.

The application then analyzes whether those customers return in subsequent months.

The results show that customer retention is extremely limited across most acquisition cohorts.

This reinforces repeat purchasing as one of the main strategic opportunities identified in the project.

---

## Delivery Analysis

Delivery performance is analyzed through several dimensions:

- Delivery status
- Average delivery time
- Late-delivery rate
- Delivery delay severity
- Geographic delivery performance
- Customer reviews
- Freight value

One of the strongest findings is the relationship between delivery delays and customer satisfaction.

---

## AI Architecture

The AI component follows a controlled workflow:

```text
User Question
     │
     ▼
Gemini Analysis Planner
     │
     ▼
Approved Analysis Selection
     │
     ▼
Python Analytics Function
     │
     ▼
Business Data
     │
     ├────────► AI Interpretation
     │
     └────────► Dynamic Plotly Chart
```

The model does not receive unrestricted access to the database.

Instead, it selects from approved analytical functions, improving reliability and making the system easier to explain and maintain.

---

## Running the Project Locally

Clone the repository:

```bash
git clone https://github.com/anabenitez-tech/olist-ai-business-analyst.git
```

Open the project directory:

```bash
cd olist-ai-business-analyst
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
GEMINI_API_KEY=your_api_key
```

Then start the application:

```bash
streamlit run app.py
```

---

## Environment Variables

The Gemini API key is stored securely and is not included in the repository.

Local development uses:

```text
.env
```

Production deployment uses Streamlit Secrets.

Example:

```toml
GEMINI_API_KEY = "your_api_key"
```

The `.env` file is excluded through `.gitignore`.

---

## Deployment

The application is publicly deployed using **Streamlit Community Cloud**.

🔗 **Live Application:**  
https://olist-analytics-gemini.streamlit.app/

The deployment is connected directly to the GitHub repository, so new commits to the main branch can automatically update the live application.

---

## Skills Demonstrated

This project demonstrates practical experience with:

- SQL analytics
- Data cleaning
- Data validation
- Business intelligence
- Exploratory data analysis
- KPI development
- Customer segmentation
- Cohort analysis
- RFM analysis
- E-commerce analytics
- Python
- Pandas
- Interactive data visualization
- Streamlit development
- API integration
- Generative AI
- Prompt design
- Git and GitHub
- Cloud deployment
- Business storytelling

---

## Project Positioning

This project is primarily positioned as a:

**Data Analytics / Business Intelligence project with Applied AI**

It combines traditional business analytics with an AI-powered analytical interface.

The project is particularly relevant for roles such as:

- Data Analyst
- Business Intelligence Analyst
- Junior Analytics Engineer
- Product Analyst
- E-commerce Analyst
- AI-enabled Data Analyst

---

## Dataset

The project uses the public **Brazilian E-Commerce Public Dataset by Olist**, containing marketplace data about:

- Customers
- Orders
- Products
- Sellers
- Payments
- Reviews
- Geographic locations
- Delivery performance

The dataset is commonly used for educational and portfolio analytics projects.

---

## Future Improvements

Potential future extensions include:

- Predictive customer churn modeling
- Customer lifetime value estimation
- Delivery-delay prediction
- Product recommendation models
- Automated anomaly detection
- Advanced geographic visualizations
- Additional AI analysis capabilities

---

## Author

**Ana Benitez**

Data Analytics | Business Intelligence | Python | SQL | Applied AI

GitHub:  
https://github.com/anabenitez-tech

---

## Live Demo

**Try the application here:**

https://olist-analytics-gemini.streamlit.app/