import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import geopandas as gpd
import json
import folium
from folium.plugins import LocateControl
import requests
import json

# 移動 set_page_config 到最前面
st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("Marker Cluster with GeoJSON Filtering and Location")

# 讀取景點和熱區數據
Hotel = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E9%85%92%E5%BA%97%E5%90%8D%E5%96%AE.csv")
heat_data = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E5%90%84%E5%8D%80%E6%99%AF%E9%BB%9E%E6%95%B8%E9%87%8F.csv")

m = leafmap.Map(center=map_center, zoom=12)
# 添加篩選後的點標記
m.add_points_from_xy(
 Hotel,  # 使用篩選後的資料
 x="經度",
 y="緯度",
 spin=True,
 add_legend=True,
)
# 添加篩選後的熱區地圖
m.add_heatmap(
 heat_data,  # 使用篩選後的資料
 latitude="緯度",
 longitude="經度",
 value="景點數量",
 name="Heat map",
 radius=30,
)

    # 添加定位功能
folium.plugins.LocateControl().add_to(m)

    # 新增圖層控制
m.add_layer_control()

    # 顯示地圖
m.to_streamlit(height=700)

    ########################################################
# 根據選擇的行政區顯示表格
st.subheader(f"景點資料 - {selected_district}")
st.dataframe(Hotel, height=400)  # 設置高度並讓表格可滾動
