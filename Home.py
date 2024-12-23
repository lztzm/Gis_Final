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


# 準備數據
data = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E8%A7%80%E5%85%89%E5%AE%A2%E5%9C%8B%E7%B1%8D.csv")

geojson_url = "https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/tourism_comefrom.geojson"
    geojson_data = requests.get(geojson_url).json()

# 定義 Pydeck Layer
layer = pdk.Layer(
    'PathLayer',
    data,
    get_psition="[Y,X]",  # 使用 x, y, z
    get_elevation="Number/5",
    elevation_scale=800,
    get_fill_color=f"[{color[0]}, {color[1]}, {color[2]}, 210]",
        radius=80000,  # Radius of the columns
        pickable=True
)

# Pydeck 視圖配置
view_state = pdk.ViewState(
    latitude=40,
    longitude=0,
    zoom=1,
    pitch=50
)

# 繪製
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{x}, {y}, {z}"}
))



