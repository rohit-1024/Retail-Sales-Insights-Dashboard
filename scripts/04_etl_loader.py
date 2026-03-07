from dotenv import load_dotenv
import os


# ------------------------------------------------------------------------------
# Load Environment Variables from .env file

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


'''
                NOTE : ETL Loader
Load Transformed Data into Data Warehouse (MySQL Database)
'''

'''
NOTE | A complete ETL loading stage normally includes ...

1 Import required libraries
2 Load transformed dataset
3 Establish connection to MySQL database
4 Insert records into Dimension Tables
5 Create lookup mappings for dimension keys
6 Insert records into Fact Table using batch inserts
7 Commit transactions
8 Close database connection
'''

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# 1) Import Required Libraries

import pandas as pd
import mysql.connector

# ------------------------------------------------------------------------------

# 2) Load Transformed Dataset

print("\n--------------------------------------------------------------------\n")
print("Loading transformed dataset...\n")

df = pd.read_csv("data/transformed_data.csv")

print("Dataset Loaded Successfully.")
print(f"Dataset Shape (rows, columns): {df.shape}")

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------

# 3) Establish Connection to MySQL Data Warehouse

print("Connecting to MySQL Data Warehouse...\n")

connection = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

cursor = connection.cursor()

print("Connection Established Successfully.")

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------

# 4) Load Product Dimension Table (Batch Insert)

print("Loading Product Dimension Table...\n")

product_data = df[['StockCode', 'Description']].drop_duplicates()

product_insert_query = """
INSERT IGNORE INTO product_dimension (stock_code, product_name)
VALUES (%s, %s)
"""

product_values = product_data.values.tolist()

cursor.executemany(product_insert_query, product_values)

print(f"Inserted {len(product_values)} records into product_dimension.")

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------

# 5) Load Customer Dimension Table (Batch Insert)

print("Loading Customer Dimension Table...\n")

customer_data = df[['CustomerID', 'Country']].drop_duplicates()

customer_insert_query = """
INSERT IGNORE INTO customer_dimension (customer_id, country)
VALUES (%s, %s)
"""

customer_values = customer_data.values.tolist()

cursor.executemany(customer_insert_query, customer_values)

print(f"Inserted {len(customer_values)} records into customer_dimension.")

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------

# 6) Load Date Dimension Table (Batch Insert)

print("Loading Date Dimension Table...\n")

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

date_data = pd.DataFrame()
date_data['date'] = df['InvoiceDate'].dt.date
date_data['day'] = df['InvoiceDate'].dt.day
date_data['month'] = df['InvoiceDate'].dt.month
date_data['year'] = df['InvoiceDate'].dt.year

date_data = date_data.drop_duplicates()

date_insert_query = """
INSERT IGNORE INTO date_dimension (date, day, month, year)
VALUES (%s, %s, %s, %s)
"""

date_values = date_data.values.tolist()

cursor.executemany(date_insert_query, date_values)

print(f"Inserted {len(date_values)} records into date_dimension.")

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------

# 7) Commit Dimension Tables Before Fact Load

connection.commit()

# ------------------------------------------------------------------------------

# 8) Create Lookup Dictionaries for Dimension Keys

print("Creating dimension lookup mappings...\n")

cursor.execute("SELECT product_id, stock_code FROM product_dimension")
product_lookup = {stock: pid for pid, stock in cursor.fetchall()}

cursor.execute("SELECT customer_id FROM customer_dimension")
customer_lookup = {cid: cid for (cid,) in cursor.fetchall()}

cursor.execute("SELECT date_id, date FROM date_dimension")
date_lookup = {d: did for did, d in cursor.fetchall()}

print("Lookup mappings created.")

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------

# 9) Prepare Fact Table Records

print("Preparing Sales Fact Records...\n")

fact_values = []

for _, row in df.iterrows():

    product_id = product_lookup.get(row['StockCode'])
    customer_id = row['CustomerID']
    date_id = date_lookup.get(pd.to_datetime(row['InvoiceDate']).date())

    quantity = row['Quantity']
    revenue = row['Revenue']

    fact_values.append((product_id, customer_id, date_id, quantity, revenue))

print(f"Prepared {len(fact_values)} fact records.")

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------

# 10) Insert Sales Fact Table (Batch Insert)

print("Loading Sales Fact Table...\n")

fact_insert_query = """
INSERT INTO sales_fact (product_id, customer_id, date_id, quantity, revenue)
VALUES (%s, %s, %s, %s, %s)
"""

cursor.executemany(fact_insert_query, fact_values)

print(f"Inserted {len(fact_values)} records into sales_fact.")

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------

# 11) Commit Transactions

connection.commit()

print("All records committed successfully to the Data Warehouse.")

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------

# 12) Close Database Connection

cursor.close()
connection.close()

print("MySQL Connection Closed.")

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------