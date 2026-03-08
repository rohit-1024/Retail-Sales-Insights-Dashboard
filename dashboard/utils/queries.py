
import pandas as pd
from utils.db_connection import get_connection
import streamlit as st


@st.cache_data
def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    return df


# -------------------------------------------------
# a) KPI METRICS
# -------------------------------------------------

def get_total_revenue():

    query = """
    SELECT ROUND(SUM(revenue),2) AS total_revenue
    FROM sales_fact
    """
    return run_query(query)


def get_total_orders():

    query = """
    SELECT COUNT(*) AS total_orders
    FROM sales_fact
    """
    return run_query(query)


def get_total_items_sold():

    query = """
    SELECT SUM(quantity) AS total_items_sold
    FROM sales_fact
    """
    return run_query(query)


def get_unique_customers():

    query = """
    SELECT COUNT(DISTINCT customer_id) AS unique_customers
    FROM sales_fact
    """
    return run_query(query)


def get_unique_products():

    query = """
    SELECT COUNT(DISTINCT product_id) AS unique_products
    FROM sales_fact
    """
    return run_query(query)


# -------------------------------------------------
# b) TIME BASED ANALYTICS
# -------------------------------------------------

def get_monthly_revenue():

    query = """
    SELECT year, month, SUM(revenue) AS monthly_revenue
    FROM sales_fact
    JOIN date_dimension USING(date_id)
    GROUP BY year, month
    ORDER BY year, month
    """
    return run_query(query)


def get_monthly_quantity():

    query = """
    SELECT year, month, SUM(quantity) AS monthly_quantity
    FROM sales_fact
    JOIN date_dimension USING(date_id)
    GROUP BY year, month
    ORDER BY year, month
    """
    return run_query(query)


def get_daily_sales():

    query = """
    SELECT date, SUM(revenue) AS daily_sales
    FROM sales_fact
    JOIN date_dimension USING(date_id)
    GROUP BY date
    ORDER BY date
    """
    return run_query(query)


def get_yearly_revenue():

    query = """
    SELECT year, SUM(revenue) AS yearly_revenue
    FROM sales_fact
    JOIN date_dimension USING(date_id)
    GROUP BY year
    """
    return run_query(query)


def get_average_daily_revenue():

    query = """
    SELECT AVG(daily_revenue)
    FROM (
        SELECT date, SUM(revenue) AS daily_revenue
        FROM sales_fact
        JOIN date_dimension USING(date_id)
        GROUP BY date
    ) AS daily_sales
    """
    return run_query(query)


# -------------------------------------------------
# c) PRODUCT ANALYTICS
# -------------------------------------------------

def get_top_products_by_revenue():

    query = """
    SELECT product_name, SUM(revenue) AS total_revenue
    FROM sales_fact
    JOIN product_dimension USING(product_id)
    GROUP BY product_name
    ORDER BY total_revenue DESC
    LIMIT 10
    """
    return run_query(query)


def get_top_products_by_quantity():

    query = """
    SELECT product_name, SUM(quantity) AS total_quantity
    FROM sales_fact
    JOIN product_dimension USING(product_id)
    GROUP BY product_name
    ORDER BY total_quantity DESC
    LIMIT 10
    """
    return run_query(query)


def get_least_selling_products():

    query = """
    SELECT product_name, SUM(quantity) AS total_quantity
    FROM sales_fact
    JOIN product_dimension USING(product_id)
    GROUP BY product_name
    ORDER BY total_quantity ASC
    LIMIT 10
    """
    return run_query(query)


def get_avg_revenue_per_product():

    query = """
    SELECT product_name, AVG(revenue) AS avg_revenue
    FROM sales_fact
    JOIN product_dimension USING(product_id)
    GROUP BY product_name
    ORDER BY avg_revenue DESC
    LIMIT 10
    """
    return run_query(query)


def get_products_above_avg_revenue():

    query = """
    SELECT product_name, SUM(revenue) AS total_revenue
    FROM sales_fact
    JOIN product_dimension USING(product_id)
    GROUP BY product_name
    HAVING total_revenue > (
        SELECT AVG(revenue) FROM sales_fact
    )
    """
    return run_query(query)


# -------------------------------------------------
# d) CUSTOMER ANALYTICS
# -------------------------------------------------

def get_top_customers_by_revenue():

    query = """
    SELECT customer_id, SUM(revenue) AS total_spent
    FROM sales_fact
    GROUP BY customer_id
    ORDER BY total_spent DESC
    LIMIT 10
    """
    return run_query(query)


def get_average_customer_spending():

    query = """
    SELECT AVG(customer_spending)
    FROM (
        SELECT customer_id, SUM(revenue) AS customer_spending
        FROM sales_fact
        GROUP BY customer_id
    ) AS customer_totals
    """
    return run_query(query)


def get_customers_highest_quantity():

    query = """
    SELECT customer_id, SUM(quantity) AS total_items
    FROM sales_fact
    GROUP BY customer_id
    ORDER BY total_items DESC
    LIMIT 10
    """
    return run_query(query)


def get_customers_more_than_50_orders():

    query = """
    SELECT customer_id, COUNT(*) AS purchase_count
    FROM sales_fact
    GROUP BY customer_id
    HAVING purchase_count > 50
    """
    return run_query(query)


def get_customer_revenue_distribution():

    query = """
    SELECT customer_id, SUM(revenue) AS total_spent
    FROM sales_fact
    GROUP BY customer_id
    ORDER BY total_spent DESC
    """
    return run_query(query)


# -------------------------------------------------
# e) GEOGRAPHIC ANALYTICS
# -------------------------------------------------

def get_revenue_by_country():

    query = """
    SELECT country, SUM(revenue) AS total_revenue
    FROM sales_fact
    JOIN customer_dimension USING(customer_id)
    GROUP BY country
    ORDER BY total_revenue DESC
    """
    return run_query(query)


def get_quantity_by_country():

    query = """
    SELECT country, SUM(quantity) AS total_quantity
    FROM sales_fact
    JOIN customer_dimension USING(customer_id)
    GROUP BY country
    ORDER BY total_quantity DESC
    """
    return run_query(query)


def get_top_countries_by_revenue():

    query = """
    SELECT country, SUM(revenue) AS total_revenue
    FROM sales_fact
    JOIN customer_dimension USING(customer_id)
    GROUP BY country
    ORDER BY total_revenue DESC
    LIMIT 10
    """
    return run_query(query)


def get_countries_with_most_customers():

    query = """
    SELECT country, COUNT(DISTINCT customer_id) AS customer_count
    FROM customer_dimension
    GROUP BY country
    ORDER BY customer_count DESC
    """
    return run_query(query)


# -------------------------------------------------
# f) SALES BEHAVIOR ANALYTICS
# -------------------------------------------------

def get_average_order_value():

    query = """
    SELECT AVG(revenue) AS avg_order_value
    FROM sales_fact
    """
    return run_query(query)


def get_highest_transaction():

    query = """
    SELECT MAX(revenue) AS highest_transaction
    FROM sales_fact
    """
    return run_query(query)


def get_lowest_transaction():

    query = """
    SELECT MIN(revenue) AS lowest_transaction
    FROM sales_fact
    """
    return run_query(query)


def get_transactions_per_customer():

    query = """
    SELECT customer_id, COUNT(*) AS transactions
    FROM sales_fact
    GROUP BY customer_id
    ORDER BY transactions DESC
    """
    return run_query(query)


# -------------------------------------------------
# g) WAREHOUSE VALIDATION
# -------------------------------------------------

def get_fact_table_size():

    query = """
    SELECT COUNT(*) AS fact_table_size
    FROM sales_fact
    """
    return run_query(query)


def get_dimension_table_sizes():

    query = """
    SELECT
        (SELECT COUNT(*) FROM product_dimension) AS products,
        (SELECT COUNT(*) FROM customer_dimension) AS customers,
        (SELECT COUNT(*) FROM date_dimension) AS dates
    """
    return run_query(query)



# ---------------------------------
# Code for Filtering ...
# ---------------------------------

def apply_filters(base_query, year, country, product):

    conditions = []

    if year != "All":
        conditions.append(f"d.year = {year}")

    if country != "All":
        conditions.append(f"c.country = '{country}'")

    if product != "All":
        conditions.append(f"p.product_name = '{product}'")

    if conditions:

        base_query += " WHERE " + " AND ".join(conditions)

    return base_query