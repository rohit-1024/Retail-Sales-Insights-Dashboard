import streamlit as st
import plotly.express as px
from utils.queries import get_top_countries_by_revenue

st.title("🌍 Geographic Sales Insights")

st.markdown("""
This page analyzes **sales distribution across different countries**.

It helps businesses understand:
- Which regions generate the most revenue
- Geographic market opportunities
""")

st.markdown("---")

# Load Data
df = get_top_countries_by_revenue()

top_countries = df.head(10)

# Chart
fig = px.bar(
    top_countries,
    x="country",
    y="total_revenue",
    title="Top Countries by Revenue"
)

fig.update_layout(
    xaxis_title="Country",
    yaxis_title="Revenue",
    xaxis_tickangle=-45
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("📊 Geographic Sales Data")

st.dataframe(top_countries)