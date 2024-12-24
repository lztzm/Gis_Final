import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import requests
import random
import matplotlib.colors as mcolors

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
station = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E6%9D%B1%E4%BA%AC%E8%B7%AF%E7%B7%9A%E5%9C%96.csv")
railway_url = "https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E6%9D%B1%E4%BA%AC%E9%90%B5%E8%B7%AF.geojson"

# 從 URL 加載 GeoJSON 文件
response = requests.get(railway_url)
geojson_data = response.json()

# 提取唯一的 `name:en` 屬性
unique_names = set(
    feature["properties"].get("name:en", "Unknown")
    for feature in geojson_data["features"]
)

# 自動生成顏色表
color_palette = list(mcolors.CSS4_COLORS.keys())  # 使用 Matplotlib 的顏色表
random.shuffle(color_palette)  # 隨機排序
color_map = {name: color_palette[i % len(color_palette)] for i, name in enumerate(unique_names)}

# 自定義樣式函數
def style_function(feature):
    name = feature["properties"].get("name:en", "Unknown")
    length = feature["properties"].get("length", 1000)  # 假設 GeoJSON 有 `length` 屬性
    return {
        "color": color_map.get(name, "#000000"),  # 自動顏色
        "weight": max(2, length / 1000),  # 動態寬度，最小為 2
        "opacity": 0.8,
    }
    
# 創建地圖
m = leafmap.Map()
# 酒店圖層
hotel_layer = m.add_points_from_xy(
    hotel,
    x="經度",
    y="緯度",
    spin=True,
    add_legend=True,
    layer_name = "Hotel",
)

# 車站圖層
station_layer = m.add_points_from_xy(
    station,
    x="lat",
    y="lon",
    spin=True,
    add_legend=True,
    layer_name = "Station",
)

m.add_geojson(
    geojson_data,
    layer_name="鐵路路線",
    style_function=style_function,
)


# 添加顏色圖例到地圖
legend_dict = {name: color_map[name] for name in unique_names}
m.add_legend(title="鐵路名稱 (name:en)", legend_dict=legend_dict)


# 顯示地圖
m.to_streamlit(height=700)
