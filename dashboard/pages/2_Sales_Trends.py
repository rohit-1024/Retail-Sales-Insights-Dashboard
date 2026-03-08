import streamlit as st
import plotly.express as px
from utils.filters import render_filters
from utils.queries import run_query, apply_filters

st.title("Sales Trends")

year, country, product = render_filters()

query = """
SELECT
    d.year,
    d.month,
    SUM(sf.revenue) AS revenue
FROM sales_fact sf
JOIN date_dimension d USING(date_id)
JOIN customer_dimension c USING(customer_id)
JOIN product_dimension p USING(product_id)
"""

query = apply_filters(query, year, country, product)

query += " GROUP BY d.year, d.month ORDER BY d.year, d.month"

df = run_query(query)

fig = px.line(
    df,
    x="month",
    y="revenue",
    color="year",
    title="Monthly Revenue Trend"
)

st.plotly_chart(fig, use_container_width=True)
