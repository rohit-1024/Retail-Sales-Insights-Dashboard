
'''                 NOTE : Data Transformation                 '''

'''
NOTE | A complete data transformation stage normally includes ...

1 Load cleaned dataset
2 Create a working copy of dataset
3 Generate derived numerical fields (ex: revenue)
4 Extract useful components from datetime fields (ex: day, month, year)
5 Standardize column formats if required
6 Validate newly created fields
7 Perform final transformation checks
8 Reset index if necessary
9 Prepare dataset for Data Warehouse loading
10 Export transformed dataset for further processing

'''

# ------------------------------------------------------------------------------


# 1) Import Libraries
# Syntax : import module as alias

import pandas as pd
import numpy as np

# ------------------------------------------------------------------------------


# 2) Load Cleaned Dataset into Pandas DataFrame

df = pd.read_csv("data/cleaned_data.csv")

print("\n--------------------------------------------------------------------\n")
print("Cleaned dataset successfully loaded.")
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 3) Create a Copy of DataFrame for Transformation

df_transformed = df.copy()

print("Created a copy of cleaned dataset for transformation.")
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 4) Convert 'InvoiceDate' to Datetime Format
#    Ensures correct extraction of date components

print("Converting 'InvoiceDate' to datetime format...\n")

df_transformed['InvoiceDate'] = pd.to_datetime(df_transformed['InvoiceDate'])

print("Datatype After Conversion:")
print(df_transformed['InvoiceDate'].dtype)

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 5) Create Derived Field : Revenue
#    Revenue = Quantity x UnitPrice

print("Creating derived field 'Revenue'...\n")

df_transformed['Revenue'] = df_transformed['Quantity'] * df_transformed['UnitPrice']

print("Sample Revenue Values:")
print(df_transformed[['Quantity', 'UnitPrice', 'Revenue']].head())

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 6) Extract Day from InvoiceDate

print("Extracting 'Day' from InvoiceDate...\n")

df_transformed['Day'] = df_transformed['InvoiceDate'].dt.day

print("Day column created successfully.")

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 7) Extract Month from InvoiceDate

print("Extracting 'Month' from InvoiceDate...\n")

df_transformed['Month'] = df_transformed['InvoiceDate'].dt.month

print("Month column created successfully.")

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 8) Extract Year from InvoiceDate

print("Extracting 'Year' from InvoiceDate...\n")

df_transformed['Year'] = df_transformed['InvoiceDate'].dt.year

print("Year column created successfully.")

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 9) Verify Newly Created Derived Fields

print("Preview of Derived Fields:\n")

print(df_transformed[['InvoiceDate', 'Day', 'Month', 'Year', 'Revenue']].head())

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 10) Reset Index after Transformation

df_transformed.reset_index(drop=True, inplace=True)

print("Index has been reset after transformation.")

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 11) Show Final Transformed DataFrame Shape

print(f"Final Shape of Transformed DataFrame (rows, columns): {df_transformed.shape}")

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------




'''                 NOTE : Store Transformed Data                 '''

'''
NOTE | Storing transformed data normally includes ...

1 Verify transformed dataframe
2 Define output file path
3 Export dataframe to CSV
4 Disable index column during export
5 Confirm successful data storage

'''

# ------------------------------------------------------------------------------


# 1) Preview Transformed Dataset

print("\n--------------------------------------------------------------------\n")
print("Preview of Transformed Data (First 5 Rows):\n")
print(df_transformed.head())
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 2) Define Output File Path

output_file = "data/transformed_data.csv"

print(f"Output File Path: {output_file}")
print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 3) Save Transformed DataFrame to CSV File

df_transformed.to_csv(output_file, index=False)

print("Transformed dataset has been successfully saved to CSV file.")

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------


# 4) Confirm Export by Checking File Shape

print(f"Final Stored Dataset Shape (rows, columns): {df_transformed.shape}")

print("\n--------------------------------------------------------------------\n")

# ------------------------------------------------------------------------------