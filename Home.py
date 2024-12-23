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
        "Camino_Frances": [255, 0, 0],           # Vibrant red
        "Camino_Ingles": [0, 0, 255],           # Strong blue
        "Camino_Portugues_central": [255, 165, 0],  # Bright orange
        "Camino_Primitivo": [0, 255, 0],        # Fresh green
        "Camino_del_Norte": [128, 0, 128],      # Deep purple
        "Portugues_Coastal": [255, 255, 0],     # Sunny yellow
        "Via_de_la_Plata": [139, 69, 19],       # Earthy brown
        "default": [0, 0, 0],                   # Default color if route not found
    }

data_urls_dict = {
    "Camino_Frances": "https://raw.githubusercontent.com/chinchillaZ/streamlit-hw/main/Camino/1_Frances_travelers.csv",
    "Camino_Ingles": "https://raw.githubusercontent.com/chinchillaZ/streamlit-hw/main/Camino/6_Ingles_travelers.csv",
    "Camino_Portugues_central": "https://raw.githubusercontent.com/chinchillaZ/streamlit-hw/main/Camino/2_Portugues_travelers.csv",
    "Camino_Primitivo": "https://raw.githubusercontent.com/chinchillaZ/streamlit-hw/main/Camino/4_Primitivo_travelers.csv",
    "Camino_del_Norte": "https://raw.githubusercontent.com/chinchillaZ/streamlit-hw/main/Camino/3_Norte_travelers.csv",
    "Portugues_Coastal": "https://raw.githubusercontent.com/chinchillaZ/streamlit-hw/main/Camino/7_Muxia_travelers.csv",
    "Via_de_la_Plata": "https://raw.githubusercontent.com/chinchillaZ/streamlit-hw/main/Camino/5_Plata_travelers.csv",
    "default": ""  # Default key if route is not found
}


def show_map(csv_url, color):
    chart_data = pd.read_csv(csv_url)
    chart_data = chart_data[chart_data["year"] == 2024]

   # Load the GeoJSON data from the URL
    geojson_url = "https://chinchillaz.github.io/streamlit-hw/all_Camino_route.geojson"
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

