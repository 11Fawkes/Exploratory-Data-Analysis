
import streamlit as st
from scipy.spatial import KDTree
import pandas as pd
from admin_unit import geo_zip_updated
from color_values import color_value_tables
import streamlit as st
from add_values import add_value_to_unit_vectorized  # Update this line
from scipy.spatial import KDTree
from color_values import color_value_tables

# Function to create KD-tree for a given color value table
@st.cache_data
def create_tree_for_color_value_table(color_value_table):
    color_points = list(color_value_table.keys())  # Get the RGB color points
    return KDTree(color_points)

# Creating KD-trees for each pollutant's color value table
trees = {pollutant: create_tree_for_color_value_table(color_value_table)
         for pollutant, color_value_table in color_value_tables.items()}

@st.cache_data
def get_value_from_color_optimized(rgb_color, tree, value_table):
    # Query the KD-tree to find the nearest RGB color
    distance, index = tree.query(rgb_color)
    nearest_color = tree.data[index]

    # Convert the nearest_color to a tuple of integers
    nearest_color_tuple = tuple(nearest_color.astype(int))

    # Retrieve the corresponding value from the value table
    value = value_table.get(nearest_color_tuple, None)

    return value

def vectorized_value_conversion(df, pollutant, tree, value_table):
    # Extract the RGB columns for the pollutant
    rgb_values = df[f"{pollutant}_rgb"].apply(pd.Series)

    # Vectorized query of KD-tree
    distances, indices = tree.query(rgb_values)

    # Convert indices to nearest colors and then to values
    nearest_colors = tree.data[indices].astype(int)
    values = [value_table.get(tuple(color), None) for color in nearest_colors]

    return values

def add_value_to_unit_vectorized(df, trees, color_value_tables):
    for pollutant in color_value_tables.keys():
        value_column = f"{pollutant}_value"
        tree = trees[pollutant]
        value_table = color_value_tables[pollutant]

        # Apply the vectorized conversion for each pollutant
        df[value_column] = vectorized_value_conversion(df, pollutant, tree, value_table)

    return df


geo_zip_updated = add_value_to_unit_vectorized(geo_zip_updated, trees, color_value_tables)
geo_zip_updated = geo_zip_updated.drop(columns=["CO_rgb", "NO2_rgb", "HCHO_rgb", "O3_rgb", "SO2_rgb", "AER_rgb", "CH4_rgb", "geometry"])

