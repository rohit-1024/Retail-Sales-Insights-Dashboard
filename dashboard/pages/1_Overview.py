
import streamlit as st
from utils.filters import render_filters
from utils.queries import run_query, apply_filters
import pandas as pd

st.title("Sales Overview")

year, country, product = render_filters()

query = """
SELECT
    SUM(revenue) AS revenue,
    COUNT(*) AS orders
FROM sales_fact sf
JOIN date_dimension d USING(date_id)
JOIN customer_dimension c USING(customer_id)
JOIN product_dimension p USING(product_id)
"""

query = apply_filters(query, year, country, product)

df = run_query(query)

col1, col2 = st.columns(2)

revenue = df.iloc[0]['revenue'] if not df.empty else 0

if revenue is None:
    revenue = 0

col1.metric("Total Revenue", f"${revenue:,.2f}")

orders = df.iloc[0]['orders'] if not df.empty else 0

if orders is None or pd.isna(orders):
    orders = 0

col2.metric("Total Orders", f"{int(orders):,}")