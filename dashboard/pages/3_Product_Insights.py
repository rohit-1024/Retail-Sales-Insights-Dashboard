
import streamlit as st
import plotly.express as px
from utils.filters import render_filters
from utils.queries import run_query, apply_filters

st.title("Product Insights")

year, country, product = render_filters()

query = """
SELECT
    p.product_name,
    SUM(sf.revenue) AS revenue
FROM sales_fact sf
JOIN date_dimension d USING(date_id)
JOIN customer_dimension c USING(customer_id)
JOIN product_dimension p USING(product_id)
"""

query = apply_filters(query, year, country, product)

query += """
GROUP BY p.product_name
ORDER BY revenue DESC
LIMIT 10
"""

df = run_query(query)

fig = px.bar(
    df,
    x="product_name",
    y="revenue",
    title="Top Products"
)

st.plotly_chart(fig, use_container_width=True)