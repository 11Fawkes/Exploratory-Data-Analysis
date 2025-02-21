

from line_profiler import profile
from matplotlib import pyplot as plt
import streamlit as st
st.set_page_config(layout="wide")
from streamlit_folium import st_folium
import folium
import pandas as pd
from unit_value_vis import top_lan_names_by_pollutant
from add_values import geo_zip_updated
from climate_data import image_dict
from image_arrays import image_to_data_uri
from bounds import bounds
import plotly.express as px
import seaborn as sns
from noise_data import processed_dataframes, selected_dataframes


st.title('Climate Monitoring ')

st.markdown("""
<style>
.main {
    background-color:#f0f2f6;
}
/* Change the default text color */
body {
    color: black;
}

/* Change the header color */
h1,h2,h3,h4,h5,h6 {
    color: green;
}
/* Targeting all subheaders */
.css-1s0hp0w {
    font-size: 10px; /* Adjust the size as needed */
}
/* Change font throughout the app */
body {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}
/* Custom styles for the radio buttons */
div.row-widget.stRadio > div {
    display: flex;
    flex-direction: row;
}

/* Style each radio item (optional) */
div.row-widget.stRadio > div > label {
    background-color: #efefef;  /* Light grey background */
    padding: 3px 5px;          /* Padding around text */
    border-radius: 10px;        /* Rounded corners */
    margin-right: 3px;          /* Space between items */
}

/* Style for checked radio item (optional) */
div.row-widget.stRadio > div > label[data-baseweb="radio"] > div:first-child > div {
    background-color: blue !important; /* Blue background for selected item */
}
</style>
""", unsafe_allow_html=True)

# POLLUTANT DATA

pollutant_name_mapping = {
    'Carbon Monoxide (CO)': 'CO_value',
    'Nitrogen Dioxide (NO2)': 'NO2_value',
    'Formaldehyde (HCHO)': 'HCHO_value',
    'Ozone (O3)': 'O3_value',
    'Sulfur Dioxide (SO2)': 'SO2_value',
    'Methane (CH4)': 'CH4_value',
    'Aerosol (AER)': 'AER_value'
}
selected_pollutant_name = st.radio(
    "Pollutants:",
    list(pollutant_name_mapping.keys())
)

@profile
def get_image_data(pollutant):
    """
    Get the data URI of the image corresponding to the specified pollutant.
    """
    if pollutant in image_dict:
        image_info = image_dict[pollutant]
        if 'image' in image_info:
            image_path = image_info['image']  # Assuming this is the path to the image
            return image_to_data_uri(image_path)
    return None

if selected_pollutant_name:
    selected_pollutant_column = pollutant_name_mapping[selected_pollutant_name]
    image_path = get_image_data(selected_pollutant_column)
    image_bounds=bounds
def create_map( pollutant, image_uri, bounds):
    # Center and bounds of Germany
    center_lat, center_lon = 51.1657, 10.4515

    # Initialize the map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

    # Add the image overlay
    if image_path:
        folium.raster_layers.ImageOverlay(
            image=image_path,
            bounds=bounds,
            opacity=0.6,  # Adjust as necessary
            interactive=True,
            cross_origin=False,
            zindex=1,
        ).add_to(m)

    return m



# Using the function to get the top lan_names
top_lan_names_df = top_lan_names_by_pollutant(geo_zip_updated, selected_pollutant_column)

# Create a histogram
fig = px.bar(
    top_lan_names_df,
    x=selected_pollutant_column,
    y=top_lan_names_df.index,
    labels={'x': f'Average {selected_pollutant_name}', 'y': 'Lan Name'},
    color=selected_pollutant_column,  # Color bars based on value
    template='plotly_dark',    # Use a modern template like 'plotly_dark'
)

# Update layout for a more polished look
fig.update_layout(
    xaxis_title=f'Average {selected_pollutant_name} mol/m2',
    yaxis_title=None,
    font=dict(family="Arial, sans-serif", size=12, color="white"),
    hovermode='closest',
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)', # Transparent background
    margin=dict(l=0, r=0, t=0, b=0)
)

# Update tooltips
fig.update_traces(
    hovertemplate=(
        "District: %{y}<br>" +
        f"Average {selected_pollutant_name}: " + "%{x}"
    )
)

col1, col2 = st.columns(2)

# Place the map in the first column
with col1:
    # Assuming 'map' is a Folium map object
    st_folium(create_map( selected_pollutant_column, image_path, image_bounds), width=700, height=500 )

# Place the plot in the second column
with col2:
    st.subheader(f'Average {selected_pollutant_name}')
    # Assuming 'plot' is a Plotly figure object
    st.plotly_chart(fig, use_container_width=True)


# NOISE DATA
# Set the style of the plot
sns.set(style="whitegrid")

noise_name={'Roads':'Aggl_Road_Data1',
            'Railway':'Aggl_Rail_Data',
            'Airports':'Aggl_Air_Data',
            'Major Airports':'MAir_Data',
            'Industry':'Aggl_Ind_Data'}
# Function to create and display a multi-colored line plot for each sheet
@st.cache_data
def create_line_plot(sheet_name, title):
    df = processed_dataframes[sheet_name]
    noise_columns = [col for col in df.columns if col.startswith('#noise')]
    melted_df = pd.melt(df, id_vars=['Region'], value_vars=noise_columns)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='Region', y='value', hue='variable', data=melted_df, marker='o', palette='viridis', ax=ax)

    ax.set_xlabel('Region')
    ax.set_ylabel('Population')
    ax.set_title(title)
    ax.legend(title='Noise Categories', bbox_to_anchor=(1.05, 1), loc='upper left')
    #plt.xticks(rotation=45, ha='right')

    st.pyplot(fig)

# Streamlit UI
sheet_names = list(noise_name.keys())
selected_sheet_name = st.radio("Noise sources:", sheet_names)

if selected_sheet_name:
    selected_sheet = noise_name[selected_sheet_name]
    create_line_plot(selected_sheet, f"Number of people affected by noise ({selected_sheet_name})")


st.write("Dashboard created by [Dhruv Rajesh and Anisha ]")
