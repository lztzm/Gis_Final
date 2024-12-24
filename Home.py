import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import geopandas as gpd
import numpy as np
import geopandas as gpd
import plotly.express as px
import requests
import pydeck as pdk
import plotly.express as px


st.set_page_config(layout="wide")

# Customize the sidebar

st.sidebar.title("About")
logo = "data:image/png;base64,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"
st.sidebar.image(logo)

# Customize page title
st.title("東京觀光地圖")


st.header("簡介")

markdown = """
日本是旅遊大國，世界各地的人都慕名前來體驗日本文化，可以說是旅遊聖地。而當中身為首都的東京更是當中的佼佼者，我們希望能夠在這個Steamlit裡面視覺化東京的熱門旅遊景點以及相關旅遊配套！可以給來東京的觀光客提供一個方便的地圖，我們所設計的WebApp裡面包含了交通、景點、飯店等資訊。

👈🏻按這邊有更多內容哦！

"""

st.markdown(markdown)

# 準備數據
data = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E8%A7%80%E5%85%89%E5%AE%A2%E5%9C%8B%E7%B1%8D.csv")

geojson_url = "https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/tourism_comefrom.geojson"
geojson_data = requests.get(geojson_url).json()

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
                data,
                get_position="[X, Y]",  # Note: Longitude is X, Latitude is Y
                get_elevation="Number / 10",  # Set the elevation (height of the column) proportional to 'Number'
                elevation_scale=8000,  # Scale factor for elevation 誇張程度
                get_color=[0, 0, 255],  # Color of the columns RGBA
                radius=80000,  # Radius of the columns
                pickable=True,
            ),
            pdk.Layer(
                "GeoJsonLayer",  # Add GeoJSON layer
                geojson_data,  # Use the filtered GeoJSON
                get_fill_color=[255, 0, 0, 255],  # Color for the route line (red)
                get_line_color=[255, 0, 0],  # Line color for the route (red)
                line_width=4,  # Line width for the route
                pickable=True,
            )
        ],
    )
)
#########################################
pie = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E8%A7%80%E5%85%89%E5%AE%A2%E5%85%A5%E5%9C%8B%E6%A9%9F%E5%A0%B4%20%E6%A9%AB%E5%BC%8F.csv")
# 繪製圓餅圖
fig = px.pie(
    pie,
    names="國家/入境機場",
    values="全體",
    title="入境機場圓餅圖",
    hole=0,  # 中心空洞比例（甜甜圈圖效果）
)

st.plotly_chart(fig)
#########################################
chart_data = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E8%A7%80%E5%85%89%E5%AE%A2%E5%85%A5%E5%9C%8B%E6%A9%9F%E5%A0%B4_%E7%99%BE%E5%88%86%E6%AF%94.csv")
# Show the table of chart_data
st.table(chart_data)  # Display the chart data as a table



