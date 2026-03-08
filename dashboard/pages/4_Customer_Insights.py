import streamlit as st
import plotly.express as px
from utils.queries import run_query

st.title("👥 Customer Spending Insights")

st.markdown("""
This page highlights **top customers based on total spending**.

Understanding customer spending helps businesses:
- Identify high-value customers
- Develop targeted marketing strategies
- Improve customer retention
""")

st.markdown("---")

query = """
SELECT customer_id, SUM(revenue) AS total_spent
FROM sales_fact
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10
"""

df = run_query(query)

# Chart
fig = px.bar(
    df,
    x="customer_id",
    y="total_spent",
    title="Top 10 Customers by Revenue"
)

fig.update_layout(
    xaxis_title="Customer ID",
    yaxis_title="Total Spending"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("📊 Customer Data")

st.dataframe(df)