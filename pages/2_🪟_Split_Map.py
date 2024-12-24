import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import requests
import folium
from folium import plugins

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

# 自定義樣式函數，根據 "colour" 屬性設置顏色
def style_function(feature):
    colour = feature["properties"].get("colour", "#000000")  # 默認為黑色
    return {
        "color": colour,  # 邊界顏色
        "weight": 2,      # 邊界寬度
        "fillOpacity": 0.2,   # 填充透明度
        "fillColor": colour,  # 填充顏色
    }

# 添加鐵路路線圖層，根據 "colour" 屬性顯示不同顏色
m.add_geojson(
    geojson_data_rail,
    layer_name="鐵路路線",
    style_function=style_function,  # 使用自定義樣式函數
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

# 創建圖例 HTML
legend_html = """
    <div style="position: fixed; bottom: 50px; right: 10px; background-color: white; border-radius: 5px; padding: 10px; z-index: 9999;">
        <h4>鐵路路線顏色圖例</h4>
        <ul style="list-style-type: none; padding: 0;">
"""

# 為每條鐵路路線添加顏色和名稱
for feature in geojson_data_rail['features']:
    color = feature['properties'].get('colour', '#000000')
    name = feature['properties'].get('name:en', 'Unknown')
    legend_html += f'<li><span style="display: inline-block; width: 20px; height: 20px; background-color: {color};"></span> {name}</li>'

legend_html += """
        </ul>
    </div>
"""

# 添加圖例到地圖
legend = folium.Popup(folium.Html(legend_html, script=True), max_width=500)
folium.Marker([35.68, 139.76], popup=legend).add_to(m)

# 添加定位功能
folium.plugins.LocateControl().add_to(m)

# 新增圖層控制
m.add_layer_control()

# 顯示地圖
m.to_streamlit(height=700)
