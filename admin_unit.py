import geopandas as gpd
from line_profiler import profile
import pandas as pd
import streamlit as st
from climate_data import image_arrays, image_shapes
from bounds import bottom_right_coords, top_left_coords


file_path = "C:/Users/dk103/Documents/APP/geo_zip_simple.geojson"
@st.cache_data
def load_geojson(file_path):
    """
    Load a GeoJSON file into a GeoDataFrame.

    :param file_path: Path to the GeoJSON file.
    :return: GeoDataFrame containing the data from the GeoJSON file.
    """
    return gpd.read_file(file_path)

@profile
def add_rgb_values_to_units(geo_zip_simple, image_array, image_shape, top_left_coords, bottom_right_coords, column_name):
    def extract_rgb_values(x, y, image_shape, image_array):
        if 0 <= x < image_shape[1] and 0 <= y < image_shape[0]:
            return image_array[y, x, :3].tolist()  # Extract RGB values
        return None  # Return None if coordinates are out of bounds

    # Vectorized approach for coordinate conversion

    centroids =geo_zip_simple['geometry'].centroid
    lat_rel = (top_left_coords[0] - centroids.y) / (top_left_coords[0] - bottom_right_coords[0])
    lon_rel = (centroids.x - top_left_coords[1]) / (bottom_right_coords[1] - top_left_coords[1])

    x_coords = (lon_rel * image_shape[1]).astype(int)
    y_coords = (lat_rel * image_shape[0]).astype(int)

    # Vectorized approach for RGB value assignment
    rgb_values = [extract_rgb_values(x, y, image_shape, image_array) for x, y in zip(x_coords, y_coords)]
    geo_zip_simple[column_name] = rgb_values

    return geo_zip_simple

# Dictionary to store updated GeoDataFrames for each pollutant
geo_zip_updated = load_geojson(file_path).copy()

for pollutant, image_array in image_arrays.items():
    image_shape = image_shapes[pollutant]

    # Add a new column for each pollutant's RGB values
    geo_zip_updated = add_rgb_values_to_units(
        geo_zip_updated,
        image_array,
        image_shape,
        top_left_coords,
        bottom_right_coords,
        f"{pollutant}_rgb"
    )