
'''                 NOTE : Explore (Analyze) Data                '''

'''
NOTE | A complete exploration stage normally includes ...

1 Load data
2 Inspect rows (head, tail)
3 Shape of dataset
4 Column names
5 Data types
6 Dataset info
7 Summary statistics
8 Missing values
9 Duplicate records
10 Invalid values (negative / zero)
11 Cancelled transactions
12 Unique values
13 Category distributions
14 Numerical distributions
15 Date range
16 Memory usage

'''
# ------------------------------------------------------------------------------


# 1) Import Libraries
# Syntax :  import module as alias

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------------------------------


# 2) Load Dataset (csv) into pandas dataframe

df = pd.read_csv("data/retail_sales.csv", encoding="ISO-8859-1")

# ------------------------------------------------------------------------------


# 3) show the dataframe

print("\n--------------------------------------------------------------------\n")
print("Dataframe : \n")
print(df)
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 4) show the first 'n' [default: 5] rows from dataframe

print("First 5 rows: \n")
print(df.head())
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 5) show the last 'n' [default: 5] rows from dataframe

print("Last 5 rows: \n")
print(df.tail())
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 6) print the size(shape) of the dataframe --->  (rows, columns)

print(f"Size / Shape (rows, columns): {df.shape}")
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 7) print all the column (attribute) names in the dataframe

print("Columns: \n")
for name in df.columns:
    print(name, end = "  ")
print()
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 8) print the datatypes of all the columns (attributes) in the dataframe

print("Datatypes of Columns: \n")
print(df.dtypes)
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 9) print the info (information) of the dataframe columns (attributes)
#    such as: Column Name, Non-Null values Count, Dtype, etc.,
#    also it shows the total columns of each Dtype
#    also shows the total memory usage of the DataFrame

print("DataFrame Information: \n")
df.info()
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 10) Print the basic Statistics for Numerical columns (attributes)

print("Basic Statistics: \n")
print(df.describe())
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 11) Print the Missing Value's (Null's) Count for each column (attribute) in the dataframe

print("Count of Null Values: \n")
print(df.isnull().sum())

print("\nPercentage of Null Values: \n")
print((df.isnull().sum() / len(df)) * 100)
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 12) Print the Total No. of duplicate records in the dataframe

print(f"Total No. of Duplicate Records: {df.duplicated().sum()}")
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 13) Print the Total No. of records in the dataframe where, Quantity is Negative

neg_qty = df[df['Quantity'] < 0]
print(f"Total no. of records with negative 'Quantity': {len(neg_qty)}")
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 14) Print the Total No. of records in the dataframe where, UnitPrice <= 0

invalid_price = df[df['UnitPrice'] <= 0]
print(f"Total no. of records with Zero / Negative 'UnitPrice': {len(invalid_price)}")
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 15) Print the Total No. of records in the dataframe which represents the canceled orders
#     Cancelled Orders : InvoiceNo starting with C

canceled_orders = df[df['InvoiceNo'].str.contains('C', na=False)]
print(f"Total no. of records representing Cancelled Orders: {len(canceled_orders)}")
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 16) Print the Total No. of Unique (Distinct) Values in each column in the DataFrame

print(f"No. of Unique Invoices: {df['InvoiceNo'].nunique()}")
print(f"No. of Unique Products: {df['StockCode'].nunique()}")
print(f"No. of Unique Customers: {df['CustomerID'].nunique()}")
print(f"No. of Unique Countries: {df['Country'].nunique()}")
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 17) Check DataFrame Memory Usage

print(f"DataFrame Memory Usage: {df.memory_usage(deep=True).sum() / (1024**2):.2f} MB")
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 18) Check Range of Dates

print("Earliest Invoice Date:", df['InvoiceDate'].min())
print("Latest Invoice Date:", df['InvoiceDate'].max())
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------