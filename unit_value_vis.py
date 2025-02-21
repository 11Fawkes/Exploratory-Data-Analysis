
import streamlit as st
import pandas as pd


def top_lan_names_by_pollutant(df, pollutant, top_n=5):
    """
    Returns the top 'lan_name's with the highest average value for a given pollutant.

    :param df: pandas DataFrame containing the data
    :param pollutant: String, name of the pollutant column
    :param top_n: Integer, number of top 'lan_name's to return
    :return: pandas DataFrame with top 'lan_name's and their mean pollutant values
    """
    if pollutant not in df.columns:
        raise ValueError(f"Pollutant '{pollutant}' not found in DataFrame")

    grouped_df = df.groupby('lan_name')[pollutant].mean()
    return grouped_df
