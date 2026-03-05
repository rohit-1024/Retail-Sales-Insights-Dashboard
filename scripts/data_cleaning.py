
'''                 NOTE : Data Cleaning                 '''

'''
NOTE | A complete data cleaning stage normally includes ...

1 Create a copy of the original dataset
2 Remove duplicate records
3 Handle missing values (drop / fill / impute)
4 Remove records with missing important identifiers (ex: CustomerID)
5 Remove records with missing critical text fields (ex: Description)
6 Handle invalid numerical values (negative / zero where not allowed)
7 Remove negative Quantity (returns) if not required for analysis
8 Remove records with zero / negative UnitPrice
9 Remove cancelled transactions (InvoiceNo starting with 'C')
10 Convert incorrect data types (ex: InvoiceDate to datetime)
11 Standardize text fields (strip spaces, lowercase if needed)
12 Remove unnecessary columns (if any)
13 Handle outliers (extremely high Quantity or UnitPrice)
14 Ensure categorical columns have valid values
15 Reset index after cleaning
16 Perform final validation checks to confirm dataset integrity

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


# 3) Make a Copy of Original DataFrame (Recommended before Cleaning)

df_clean = df.copy()

print("\n--------------------------------------------------------------------\n")
print("Created a copy of original dataframe for cleaning.")
print("\n--------------------------------------------------------------------\n")


# ------------------------------------------------------------------------------


# 4) Remove Duplicate Records from the DataFrame

duplicates = df_clean.duplicated().sum()
print(f"Duplicate Records Found: {duplicates}")

df_clean.drop_duplicates(inplace=True)

print(f"Remaining Records After Removing Duplicates: {df_clean.shape[0]}")
print("\n--------------------------------------------------------------------\n")


# ------------------------------------------------------------------------------


# 5) Convert 'InvoiceDate' Column to Datetime Format
#    This ensures proper time-based analysis later

print("Converting 'InvoiceDate' to datetime format...\n")

df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'], dayfirst=True)

print("Datatype After Conversion:")
print(df_clean['InvoiceDate'].dtype)

print("\n--------------------------------------------------------------------\n")


# ------------------------------------------------------------------------------


# 6) Remove Records where Quantity is Negative
#    Negative quantity usually represents product returns

neg_qty_records = df_clean[df_clean['Quantity'] < 0]

print(f"Records with Negative Quantity: {len(neg_qty_records)}")

df_clean = df_clean[df_clean['Quantity'] > 0]

print(f"Remaining Records After Removing Negative Quantity: {df_clean.shape[0]}")
print("\n--------------------------------------------------------------------\n")


# ------------------------------------------------------------------------------


# 7) Remove Records where UnitPrice is Zero or Negative

invalid_price_records = df_clean[df_clean['UnitPrice'] <= 0]

print(f"Records with Zero / Negative UnitPrice: {len(invalid_price_records)}")

df_clean = df_clean[df_clean['UnitPrice'] > 0]

print(f"Remaining Records After Removing Invalid UnitPrice: {df_clean.shape[0]}")
print("\n--------------------------------------------------------------------\n")


# ------------------------------------------------------------------------------


# 8) Remove Cancelled Orders
#    Cancelled invoices usually start with 'C'

cancelled_orders = df_clean[df_clean['InvoiceNo'].astype(str).str.startswith('C')]

print(f"Records Representing Cancelled Orders: {len(cancelled_orders)}")

df_clean = df_clean[~df_clean['InvoiceNo'].astype(str).str.startswith('C')]

print(f"Remaining Records After Removing Cancelled Orders: {df_clean.shape[0]}")
print("\n--------------------------------------------------------------------\n")


# ------------------------------------------------------------------------------


# 9) Remove Records with Missing Description

missing_description = df_clean['Description'].isnull().sum()

print(f"Records with Missing Description: {missing_description}")

df_clean = df_clean[df_clean['Description'].notnull()]

print(f"Remaining Records After Removing Missing Description: {df_clean.shape[0]}")
print("\n--------------------------------------------------------------------\n")


# ------------------------------------------------------------------------------


# 10) Remove Records with Missing CustomerID
#    Since CustomerID is important for customer analysis

missing_customer = df_clean['CustomerID'].isnull().sum()
print(f"Records with Missing CustomerID: {missing_customer}")

df_clean = df_clean[df_clean['CustomerID'].notnull()]

print(f"Remaining Records After Removing Missing CustomerID: {df_clean.shape[0]}")
print("\n--------------------------------------------------------------------\n")


# ------------------------------------------------------------------------------


# 11) Reset Index after Cleaning

df_clean.reset_index(drop=True, inplace=True)

print("Index has been reset after cleaning.")
print("\n--------------------------------------------------------------------\n")


# ------------------------------------------------------------------------------


# 12) Show Final Cleaned DataFrame Shape

print(f"Final Shape of Cleaned DataFrame (rows, columns): {df_clean.shape}")
print("\n--------------------------------------------------------------------\n")


# ------------------------------------------------------------------------------


# 13) Verify that No Invalid Records Remain

print("Final Validation Checks:\n")

print(f"Duplicate Records: {df_clean.duplicated().sum()}")
print(f"Negative Quantity Records: {(df_clean['Quantity'] < 0).sum()}")
print(f"Zero / Negative UnitPrice Records: {(df_clean['UnitPrice'] <= 0).sum()}")
print(f"Missing CustomerID Records: {df_clean['CustomerID'].isnull().sum()}")

print("\n--------------------------------------------------------------------\n")


# ------------------------------------------------------------------------------




'''                 NOTE : Store Cleaned Data                 '''

'''
NOTE | Storing cleaned data normally includes ...

1 Verify final cleaned dataframe
2 Define output file name and location
3 Save dataframe to CSV file
4 Disable index column while saving
5 Confirm successful data export

'''

# ------------------------------------------------------------------------------


# 1) Verify Final Cleaned DataFrame

print("\n--------------------------------------------------------------------\n")
print("Preview of Cleaned Data (First 5 Rows):\n")
print(df_clean.head())
print("\n--------------------------------------------------------------------\n")


# ------------------------------------------------------------------------------


# 2) Define Output File Path

output_file = "data/cleaned_data.csv"

print(f"Output File Path: {output_file}")
print("\n--------------------------------------------------------------------\n")


# ------------------------------------------------------------------------------


# 3) Save Cleaned DataFrame to CSV File

df_clean.to_csv(output_file, index=False)

print("Cleaned dataset has been successfully saved to CSV file.")
print("\n--------------------------------------------------------------------\n")


# ------------------------------------------------------------------------------


# 4) Confirm Export by Checking File Shape

print(f"Final Stored Dataset Shape (rows, columns): {df_clean.shape}")
print("\n--------------------------------------------------------------------\n")


# ------------------------------------------------------------------------------