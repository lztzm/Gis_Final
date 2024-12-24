import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import requests
import random
import matplotlib.colors as mcolors
import folium

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
station = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E6%9D%B1%E4%BA%AC%E8%B7%AF%E7%B7%9A%E5%9C%96.csv")
railway_url = "https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E6%9D%B1%E4%BA%AC%E9%90%B5%E8%B7%AF.geojson"
region_url = "https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E6%9D%B1%E4%BA%AC%E8%A1%8C%E6%94%BF%E5%8D%80%E5%88%86%E7%95%8C.geojson"

# 從 URL 加載 GeoJSON 文件
response = requests.get(region_url)
geojson_data = response.json()

response_railway = requests.get(railway_url)
geojson_data_rail = response_railway.json()

# 提取唯一的 `name:en` 屬性
unique_names = set(
    feature["properties"].get("name:en", "Unknown")
    for feature in geojson_data_rail["features"]
)

# 自動生成顏色表
color_palette = list(mcolors.CSS4_COLORS.keys())  # 使用 Matplotlib 的顏色表
random.shuffle(color_palette)  # 隨機排序
color_map = {name: color_palette[i % len(color_palette)] for i, name in enumerate(unique_names)}

# 自定義樣式函數
def style_function(feature):
    name = feature["properties"].get("name:en", "Unknown")
    return {
        "color": color_map.get(name, "#000000"),  # 根據 name:en 屬性設置顏色
        "weight": max(2, 5),  # 動態寬度，最小為 2
        "opacity": 0.8,
    }

# 創建地圖
m = leafmap.Map()

# 車站圖層
station_layer = m.add_points_from_xy(
    station,
    x="lat",
    y="lon",
    spin=True,
    add_legend=True,
    layer_name = "Station",
)

# 添加鐵路路線圖層，根據 name:en 顯示不同顏色
m.add_geojson(
    geojson_data_rail,
    layer_name="鐵路路線",
    style_function=style_function,
)

# 提供選擇行政區的功能
districts = ['全部區域'] + list(set([feature["properties"].get("laa", "Unknown") for feature in geojson_data["features"]]))
selected_district = st.selectbox('選擇行政區', districts)

# 根據選擇的行政區過濾 GeoJSON 數據
if selected_district != '全部區域':
    filtered_geojson = {
        "type": "FeatureCollection",
        "features": [feature for feature in geojson_data["features"] if feature["properties"].get("laa", "") == selected_district]
    }
else:
    filtered_geojson = geojson_data  # 如果選擇 "全部區域"，顯示全部區域

# 添加篩選後的 GeoJSON 圖層
m.add_geojson(
    filtered_geojson,  # 使用篩選後的 GeoJSON 數據
    layer_name="行政區域",
    style={
        "color": "blue",  # 邊界顏色
        "weight": 2,      # 邊界寬度
        "fillColor": "cyan",  # 填充顏色
        "fillOpacity": 0.2,   # 填充透明度
    },
)

# 自定義 HTML 來顯示可滾動的圖例
legend_html = """
<div style="max-height: 200px; overflow-y: scroll; padding: 10px;">
    <ul style="list-style: none; padding: 0;">
"""
for name in unique_names:
    legend_html += f'<li style="color: {color_map[name]};">{name}</li>'
legend_html += "</ul></div>"

# 使用 Streamlit 的 HTML 顯示自定義圖例
st.markdown(legend_html, unsafe_allow_html=True)

# 添加定位功能
folium.plugins.LocateControl().add_to(m)

# 新增圖層控制
m.add_layer_control()

# 顯示地圖
m.to_streamlit(height=700)

