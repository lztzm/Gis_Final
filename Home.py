import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import geopandas as gpd
import numpy as np
import geopandas as gpd
import plotly.express as px
import requests

st.set_page_config(layout="wide")

# Customize the sidebar

st.sidebar.title("About")
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Customize page title
st.title("東京的旅遊景點以及鐵路視覺化")


st.header("簡介")

markdown = """
日本是台灣的熱門旅遊聖地，東京更是當中的佼佼者，我們希望能夠在這個Steamlit裡面視覺化東京的熱門旅遊景點以及相關旅遊配套！

"""

st.markdown(markdown)

color_map = {
        "Japna": [255, 0, 0]               # Default color if route not found
    }

data_urls_dict = {
    "Camino_Frances": "https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E8%A7%80%E5%85%89%E5%AE%A2%E5%9C%8B%E7%B1%8D.csv"
}


def show_map(csv_url, color):
    chart_data = pd.read_csv(csv_url)

   # Load the GeoJSON data from the URL
    geojson_url = "https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/tourism_comefrom.geojson"
    geojson_data = requests.get(geojson_url).json()

    # Filter the GeoJSON features based on the route_name
    filtered_geojson = {
        "type": "FeatureCollection",
        "features": [
            feature for feature in geojson_data["features"]
            if feature["properties"].get("route") == route_name
        ]
    }



    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v10",
            initial_view_state=pdk.ViewState(
                latitude=40.0,  # Center near Spain for better view
                longitude=0.0,
                zoom=1,
                pitch=45,
            ),
            layers=[
                pdk.Layer(
                    "ColumnLayer",
                    data=chart_data,
                    get_position="[Y, X]",  # Note: Longitude is X, Latitude is Y
                    get_elevation="Number / 10",  # Set the elevation (height of the column) proportional to 'Number'
                    elevation_scale=800,  # Scale factor for elevation 誇張程度
                    get_fill_color=f"[{color[0]}, {color[1]}, {color[2]}, 210]",  # Color of the columns RGBA
                    radius=80000,  # Radius of the columns
                    pickable=True,
                ),
                pdk.Layer(
                    "GeoJsonLayer",  # Add GeoJSON layer
                    filtered_geojson,  # Use the filtered GeoJSON
                    get_fill_color=[255, 0, 0, 255],  # Color for the route line (red)
                    get_line_color=[255, 0, 0],  # Line color for the route (red)
                    line_width=4,  # Line width for the route
                    pickable=True,
                )
            ],
        )
    )
    # Show the table of chart_data
    st.table(chart_data)  # Display the chart data as a table

    route_name = "Japna"
    data_url = data_urls_dict.get(route_name, data_urls_dict["default"])
    color = color_map.get(route_name, color_map["default"])
    show_map(data_url, color)

st.markdown("<br><br><br>", unsafe_allow_html=True)  # Adds three line breaks
