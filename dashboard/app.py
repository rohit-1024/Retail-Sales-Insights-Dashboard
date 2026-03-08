# dashboard/app.py
import streamlit as st
import plotly.express as px
from datetime import datetime

from utils.filters import render_filters
from utils.queries import run_query, apply_filters
from components.kpi_cards import kpi_card

# -------------------------------------------------------------------------
# Page configuration
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="Retail Sales Data Warehouse & Business Analytics Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------------
# Top of page: Title + short description
# -------------------------------------------------------------------------
col_title, col_space, col_logo = st.columns([6, 1, 1])
with col_title:
    st.title("📦 Retail Sales Data Warehouse & Business Analytics Dashboard")
    st.markdown(
        """
        **Interactive Business Intelligence dashboard** built on a production-style
        **MySQL Star Schema data warehouse**.
        
        Use the global filters in the sidebar to slice and drill into the analytics below.
        """
    )

with col_logo:
    st.caption("")  # leave small right-aligned space for a logo if needed

st.markdown("---")

# -------------------------------------------------------------------------
# Sidebar: About, Filters, Contact
# -------------------------------------------------------------------------
with st.sidebar:
    st.header("Filters & Info")

    st.markdown("**Global filters** apply across all KPIs and charts below.")
    st.markdown("---")

    # render_filters returns selected (year, country, product)
    year, country, product = render_filters()

    st.markdown("---")
    st.subheader("About this Dashboard")
    st.markdown(
        """
        **What:** Sales analytics built from transactional data transformed into a
        star-schema data warehouse (fact + dimension tables).

        **Pipeline:** Raw → Cleaning → Transformation → ETL → Warehouse → Dashboard
        """
    )

    st.markdown("---")
    st.subheader("Developer")
    st.markdown(
        """
        **Rohit Raut**
        Python & SQL Developer
        Email: rohit.it4368@gmail.com
        """
    )

    st.markdown("---")
    st.caption("© 2026 Rohit Raut. All Rights Reserved.")
    st.caption(f"Last updated: {datetime(2026,3,8).strftime('%B %d, %Y')}")

# -------------------------------------------------------------------------
# Helper: safe run_query with friendly error message
# -------------------------------------------------------------------------
def safe_query(q):
    try:
        return run_query(q)
    except Exception as e:
        st.error("Failed to execute query — check DB connection and queries.")
        st.exception(e)
        return None

# -------------------------------------------------------------------------
# KPI Query - apply filters
# -------------------------------------------------------------------------
kpi_query = """
SELECT
    COALESCE(SUM(sf.revenue),0) AS revenue,
    COUNT(*) AS orders,
    COUNT(DISTINCT sf.customer_id) AS customers,
    COUNT(DISTINCT sf.product_id) AS products
FROM sales_fact sf
JOIN date_dimension d USING(date_id)
JOIN customer_dimension c USING(customer_id)
JOIN product_dimension p USING(product_id)
"""

kpi_query = apply_filters(kpi_query, year, country, product)
kpi_df = safe_query(kpi_query)

# Present KPIs in four compact cards
st.markdown("## Executive Summary")
if kpi_df is not None and not kpi_df.empty:
    rev = float(kpi_df.iloc[0]["revenue"] or 0)
    orders = int(kpi_df.iloc[0]["orders"] or 0)
    customers = int(kpi_df.iloc[0]["customers"] or 0)
    products = int(kpi_df.iloc[0]["products"] or 0)

    c1, c2, c3, c4 = st.columns([1.5, 1.5, 1.5, 1.5])
    with c1:
        kpi_card("Total Revenue", f"${rev:,.0f}", delta=None, up=True)
    with c2:
        kpi_card("Total Orders", f"{orders:,}", delta=None, up=True)
    with c3:
        kpi_card("Customers", f"{customers:,}", delta=None, up=True)
    with c4:
        kpi_card("Products Sold", f"{products:,}", delta=None, up=True)
else:
    st.info("KPIs will appear here once the connection and queries succeed.")

st.divider()

# -------------------------------------------------------------------------
# Monthly Revenue Trend (time series)
# -------------------------------------------------------------------------
st.subheader("Monthly Revenue Trend")
st.markdown("Trend shows month-by-month revenue. Use filters to slice by year, country or product.")

trend_query = """
SELECT
    d.year,
    d.month,
    SUM(sf.revenue) AS revenue
FROM sales_fact sf
JOIN date_dimension d USING(date_id)
JOIN customer_dimension c USING(customer_id)
JOIN product_dimension p USING(product_id)
"""

trend_query = apply_filters(trend_query, year, country, product)

trend_query += """
GROUP BY d.year, d.month
ORDER BY d.year, d.month
"""

trend_df = safe_query(trend_query)

if trend_df is not None and not trend_df.empty:
    # create a display-friendly x-axis label
    trend_df["month_str"] = trend_df["month"].astype(str).str.zfill(2)
    trend_df["period"] = trend_df["year"].astype(str) + "-" + trend_df["month_str"]

    fig = px.line(
        trend_df,
        x="period",
        y="revenue",
        color="year",
        markers=True,
        title="Monthly Revenue Trend"
    )
    fig.update_layout(xaxis_title="Period (YYYY-MM)", yaxis_title="Revenue", title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No trend data found for the selected filters.")

st.divider()

# -------------------------------------------------------------------------
# Top Products & Geographic Snapshot
# -------------------------------------------------------------------------
left_col, right_col = st.columns((2, 1))

with left_col:
    st.subheader("Top Products by Revenue")
    prod_query = """
    SELECT
        p.product_name,
        SUM(sf.revenue) AS revenue
    FROM sales_fact sf
    JOIN date_dimension d USING(date_id)
    JOIN customer_dimension c USING(customer_id)
    JOIN product_dimension p USING(product_id)
    """
    prod_query = apply_filters(prod_query, year, country, product)
    prod_query += """
    GROUP BY p.product_name
    ORDER BY revenue DESC
    LIMIT 10
    """
    prod_df = safe_query(prod_query)
    if prod_df is not None and not prod_df.empty:
        prod_df.index = prod_df.index + 1
        fig2 = px.bar(
            prod_df,
            x="product_name",
            y="revenue",
            title="Top 10 Products by Revenue"
        )
        fig2.update_layout(xaxis_tickangle=-40, title_x=0.5, yaxis_title="Revenue")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("**Top products (table)**")
        st.dataframe(prod_df, height=300)
    else:
        st.info("No product data found for the selected filters.")

with right_col:
    st.subheader("Geographic Snapshot")
    geo_query = """
    SELECT country, SUM(sf.revenue) AS revenue
    FROM sales_fact sf
    JOIN customer_dimension c USING(customer_id)
    JOIN date_dimension d USING(date_id)
    JOIN product_dimension p USING(product_id)
    """
    geo_query = apply_filters(geo_query, year, country, product)
    geo_query += """
    GROUP BY country
    ORDER BY revenue DESC
    LIMIT 10
    """
    geo_df = safe_query(geo_query)
    if geo_df is not None and not geo_df.empty:
        geo_df.index = geo_df.index + 1
        fig3 = px.pie(geo_df, names="country", values="revenue", title="Top Countries by Revenue")
        fig3.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("**Top countries (table)**")
        st.dataframe(geo_df, height=300)
    else:
        st.info("No geographic data found for the selected filters.")

st.divider()

# -------------------------------------------------------------------------
# Quick Navigation Cards to other pages
# -------------------------------------------------------------------------
st.subheader("Explore Dashboard Pages")
nav_col1, nav_col2, nav_col3 = st.columns(3)

if nav_col1.button("🔎 Sales Trends"):
    st.switch_page("pages/2_Sales_Trends.py")

if nav_col2.button("🛍 Product Insights"):
    st.switch_page("pages/3_Product_Insights.py")

if nav_col3.button("👥 Customer Insights"):
    st.switch_page("pages/4_Customer_Insights.py")


st.divider()

# -------------------------------------------------------------------------
# Dataset & Pipeline info (collapsible)
# -------------------------------------------------------------------------

with st.expander("🔧 Data Pipeline (Click to expand)", expanded=False):

    st.markdown("""
    <style>
    .pipeline {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 12px;
        margin-top: 20px;
    }

    .step {
        background-color: #111827;
        border: 1px solid #374151;
        border-radius: 8px;
        padding: 12px 20px;
        font-size: 16px;
        text-align: center;
        width: 380px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.4);
    }

    .arrow {
        font-size: 22px;
        color: #9CA3AF;
    }

    .code {
        color: #22c55e;
        font-family: monospace;
    }
    </style>

    <div class="pipeline">

    <div class="step">
    Raw Data (<span class="code">kaggle.com</span>)
    </div>

    <div class="arrow">↓</div>

    <div class="step">
    Data Exploration (<span class="code">01_exploratory_data_analysis_eda.py</span>)
    </div>

    <div class="arrow">↓</div>

    <div class="step">
    Data Cleaning (<span class="code">02_data_cleaning.py</span>)
    </div>

    <div class="arrow">↓</div>

    <div class="step">
    Feature Engineering (<span class="code">03_data_transformation.py</span>)
    </div>

    <div class="arrow">↓</div>

    <div class="step">
    ETL Loader (<span class="code">04_etl_loader.py</span>)
    </div>

    <div class="arrow">↓</div>

    <div class="step">
    MySQL Data Warehouse (<span class="code">Star Schema</span>)
    </div>

    <div class="arrow">↓</div>

    <div class="step">
    Streamlit Dashboard
    </div>

    </div>
    """, unsafe_allow_html=True)

with st.expander("🗄 Data Warehouse Table Structure (Click to expand)", expanded=False):

    st.markdown("### Fact Table")

    st.markdown("""
| sales_fact |
|------------|
| sale_id (PK) |
| product_id (FK) |
| customer_id (FK) |
| date_id (FK) |
| quantity |
| revenue |
""")

    st.markdown("---")

    st.markdown("### Dimension Tables")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**product_dimension**")
        st.markdown("""
| Column |
|-------|
| product_id (PK) |
| stock_code |
| product_name |
""")

    with col2:
        st.markdown("**customer_dimension**")
        st.markdown("""
| Column |
|-------|
| customer_id (PK) |
| country |
""")

    with col3:
        st.markdown("**date_dimension**")
        st.markdown("""
| Column |
|-------|
| date_id (PK) |
| date |
| day |
| month |
| year |
""")

# -------------------------------------------------------------------------
# Footer: contact, copyright, version
# -------------------------------------------------------------------------
st.markdown("---")
footer_col1, footer_col2 = st.columns([3, 1])
with footer_col1:
    st.markdown("**Contact:** rohit.it4368@gmail.com")
    st.markdown("**Repository:** https://github.com/rohit-1024/Retail-Sales-Insights-Dashboard.git")
with footer_col2:
    st.caption("© 2026 Rohit Raut")
    st.caption("Version: 1.0.0")

# End of dashboard homepage