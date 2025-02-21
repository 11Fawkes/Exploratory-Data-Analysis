import os
import pandas as pd
import openpyxl
import xlrd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


file_path="C:/Users/dk103/Documents/output_file_Jupy_frZero3.xlsx"
excel_file = pd.ExcelFile(file_path)

# Assuming you have defined processed_dataframes as an empty dictionary
processed_dataframes = {}

# Your loop
for sheet_name in excel_file.sheet_names:
    df = excel_file.parse(sheet_name)

    # Convert numeric columns to numeric type
    numeric_columns = df.select_dtypes(include=np.number).columns
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors="coerce")

    # Replace negative values and invalid values with zero
    df[numeric_columns] = np.where(df[numeric_columns] < 0, 0, df[numeric_columns])
    df[numeric_columns] = np.where(~np.isfinite(df[numeric_columns]), 0, df[numeric_columns])

    # Store the processed DataFrame
    processed_dataframes[sheet_name] = df

# Assuming 'processed_dataframes' is a dictionary containing processed DataFrames
output_excel_file = 'C:/Users/dk103/Documents/output_file_Jupy_frZero4.xlsx'  # Specify the desired output Excel file name

# Create an ExcelWriter object
with pd.ExcelWriter(output_excel_file) as writer:
    # Iterate through processed DataFrames and write each to the Excel file
    for sheet_name, df in processed_dataframes.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

data_to_keep=["Aggl_Road_Data1","Aggl_Rail_Data","Aggl_Air_Data","Aggl_Ind_Data", "MAir_Data"]
selected_dataframes = {key: processed_dataframes[key] for key in data_to_keep if key in processed_dataframes}
