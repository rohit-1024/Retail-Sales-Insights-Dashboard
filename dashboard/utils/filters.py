import streamlit as st
from utils.queries import run_query


def get_filter_values():

    years_query = """
    SELECT DISTINCT year FROM date_dimension ORDER BY year
    """

    countries_query = """
    SELECT DISTINCT country FROM customer_dimension ORDER BY country
    """

    products_query = """
    SELECT DISTINCT product_name FROM product_dimension ORDER BY product_name
    """

    years = run_query(years_query)
    countries = run_query(countries_query)
    products = run_query(products_query)

    return years, countries, products


def render_filters():

    st.sidebar.header("Global Filters")

    years, countries, products = get_filter_values()

    selected_year = st.sidebar.selectbox(
        "Select Year",
        ["All"] + years["year"].astype(str).tolist()
    )

    selected_country = st.sidebar.selectbox(
        "Select Country",
        ["All"] + countries["country"].tolist()
    )

    selected_product = st.sidebar.selectbox(
        "Select Product",
        ["All"] + products["product_name"].tolist()
    )

    return selected_year, selected_country, selected_product