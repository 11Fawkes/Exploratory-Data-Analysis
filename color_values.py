from line_profiler import profile
import numpy as np
import pandas as pd
from climate_data import image_dict



@profile
def create_legend(minVal, maxVal):
    def hex_to_rgb(hex_color):
        """
        Converts a hex color to an RGB tuple.

        Args:
        hex_color (str): Hex color string.

        Returns:
        tuple: Corresponding RGB tuple.
        """
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    """
    Creates a DataFrame representing a CO legend with levels and colors.

    Args:
    minVal (float): Minimum value of the range.
    maxVal (float): Maximum value of the range.

    Returns:
    DataFrame: CO levels with corresponding colors.
    """
    diff = maxVal - minVal
    colors = ['0x00007f', '0x0000ff', '0x00ffff', '0xffff00', '0xff0000', '0x7f0000']

    levels = np.array([minVal,
                       minVal + 0.125 * diff,
                       minVal + 0.375 * diff,
                       minVal + 0.625 * diff,
                       minVal + 0.875 * diff,
                       maxVal])

    levels = np.round(levels, 4)
    legend_df = pd.DataFrame({'Level': levels, 'Color': colors})
    legend_df['Color'] = legend_df['Color'].apply(lambda x: f"#{x[2:]}")
    legend_df['RGB'] = legend_df['Color'].apply(hex_to_rgb)
    return legend_df
@profile
def create_color_value_table(legend_df):
        """
        Creates a dictionary mapping RGB colors to CO levels.
        Args:
        legend_df (DataFrame): DataFrame with CO levels and colors.
        Returns:
        dict: Mapping of RGB colors to CO levels.
        """
        return {rgb: level for rgb, level in zip(legend_df['RGB'], legend_df['Level'])}


def get_value_from_color_optimized(rgb_color, tree, value_table):
    # Query the KD-tree for the nearest neighbor
    distance, index = tree.query(rgb_color)
    nearest_color = tree.data[index]

    # Convert the numpy array back to a tuple to use as a dictionary key
    nearest_color_tuple = tuple(nearest_color.astype(int))

    return value_table[nearest_color_tuple]

legend_dfs= {key: create_legend(value.get('minVal'), value.get('maxVal')) for key, value in image_dict.items()}
color_value_tables = {key: create_color_value_table(legend_df) for key, legend_df in legend_dfs.items()}
