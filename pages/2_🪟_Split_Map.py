import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd

st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("Split-panel Map")

# 讀取數據
heat_data = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E5%90%84%E5%8D%80%E6%99%AF%E9%BB%9E%E6%95%B8%E9%87%8F.csv")
hotel = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E9%85%92%E5%BA%97%E5%90%8D%E5%96%AE.csv")
station = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E8%BB%8A%E7%AB%99%E9%BB%9E%E4%BD%8D.csv")

# 創建地圖
m = leafmap.Map()

# 熱區圖層
heatmap_layer = leafmap.folium.FeatureGroup(name="熱區地圖")
m.add_heatmap(
    heat_data,
    latitude="緯度",
    longitude="經度",
    value="景點數量",
    name="Heat map",
    radius=20,
)

# 酒店圖層
hotel_layer = m.add_points_from_xy(
    hotel,
    x="經度",
    y="緯度",
    spin=True,
    add_legend=True,
)

# 車站圖層
station_layer = m.add_points_from_xy(
    station,
    x="經度",
    y="緯度",
    spin=True,
    add_legend=True,
)

# 使用 split_map 顯示兩個圖層
m.split_map(
    left_layer="OpenStreetMap",
    right_layer=hotel_layer
)

# 顯示地圖
m.to_streamlit(height=700)
