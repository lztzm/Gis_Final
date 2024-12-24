import streamlit as st
import folium
import requests
import matplotlib.colors as mcolors
import random

st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("Map with Collapsible Legend")

# 讀取數據
railway_url = "https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E6%9D%B1%E4%BA%AC%E9%90%B5%E8%B7%AF.geojson"
region_url = "https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E6%9D%B1%E4%BA%AC%E8%A1%8C%E6%94%BF%E5%8D%80%E5%88%86%E7%95%8C.geojson"

# 從 URL 加載 GeoJSON 文件
response = requests.get(railway_url)
geojson_data_rail = response.json()

# 提取唯一的 `name:en` 屬性
unique_names = set(
    feature["properties"].get("name:en", "Unknown")
    for feature in geojson_data_rail["features"]
)

# 自動生成顏色表
color_palette = list(mcolors.CSS4_COLORS.keys())  # 使用 Matplotlib 的顏色表
random.shuffle(color_palette)  # 隨機排序
color_map = {name: color_palette[i % len(color_palette)] for i, name in enumerate(unique_names)}

# 創建地圖
m = folium.Map(location=[35.68, 139.76], zoom_start=12)

# 自定義樣式函數
def style_function(feature):
    name = feature["properties"].get("name:en", "Unknown")
    return {
        "color": color_map.get(name, "#000000"),  # 根據 name:en 屬性設置顏色
        "weight": 2,
        "opacity": 0.8,
    }

# 添加 GeoJSON 圖層
folium.GeoJson(
    geojson_data_rail,
    style_function=style_function
).add_to(m)

# 這裡創建摺疊式圖例的 HTML
legend_html = """
    <div style="position: fixed; 
                top: 50px; right: 50px; 
                background-color: white; 
                padding: 10px; 
                box-shadow: 0px 0px 10px rgba(0,0,0,0.3); 
                z-index: 9999;">
        <button onclick="document.getElementById('legend').style.display='block'">
            Show Legend
        </button>
        <div id="legend" style="display:none; margin-top: 10px;">
            <button onclick="document.getElementById('legend').style.display='none'">Close Legend</button>
            <ul>
"""
# 添加每個鐵路路線的顏色到圖例
for name, color in color_map.items():
    legend_html += f'<li><span style="background-color:{color}; width: 20px; height: 10px; display: inline-block;"></span> {name}</li>'
    
legend_html += """
            </ul>
        </div>
    </div>
"""

# 添加自定義 HTML 到地圖
m.get_root().html.add_child(folium.Element(legend_html))

# 顯示地圖
st.map(m)

