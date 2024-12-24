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
station = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E8%BB%8A%E7%AB%99%E9%BB%9E%E4%BD%8D.csv")
railway_url = "https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E6%9D%B1%E4%BA%AC%E9%90%B5%E8%B7%AF.geojson"
region_url = "https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E6%9D%B1%E4%BA%AC%E8%A1%8C%E6%94%BF%E5%8D%80%E5%88%86%E7%95%8C.geojson"

# 從 URL 加載 GeoJSON 文件
response = requests.get(region_url)
geojson_data = response.json()

response_railway = requests.get(railway_url)
geojson_data_rail = response_railway.json()

# 創建地圖
m = leafmap.Map()
###############################################
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
################################################
m.add_points_from_xy(
    station,  # 使用篩選後的資料
    x="經度",
    y="緯度",
    spin=True,
    add_legend=True,
)
###############################################
# 自定義樣式函數，根據 "colour" 屬性設置顏色
def style_function(feature):
    colour = feature["properties"].get("colour", "#000000")  # 默認為黑色
    return {
        "color": colour,  # 邊界顏色
        "weight": 3,      # 邊界寬度
        "fillOpacity": 0.2,   # 填充透明度
        "fillColor": colour,  # 填充顏色
    }

# 添加鐵路路線圖層，根據 "colour" 屬性顯示不同顏色
m.add_geojson(
    geojson_data_rail,
    layer_name="鐵路路線",
    style_function=style_function,  # 使用自定義樣式函數
)

# 添加定位功能
folium.plugins.LocateControl().add_to(m)

# 新增圖層控制
m.add_layer_control()

# 創建可滾動的顏色圖例，並將其放置在地圖下方
def add_color_legend(map_obj, geojson_data):
    color_list = list(set([feature["properties"].get("colour", "#000000") for feature in geojson_data["features"]]))
    name_list = list(set([feature["properties"].get("name:en", "Unknown") for feature in geojson_data["features"]]))
    
    # 排序顏色和名稱（這裡假設顏色與名稱是一一對應的）
    color_name_pairs = sorted(zip(color_list, name_list))
    
    legend_html = '''
    <div style="position: absolute; bottom: 10px; left: 10px; background: white; border: 2px solid #ccc; padding: 10px; z-index: 9999;">
        <h4>顏色圖例</h4>
        <div style="max-height: 200px; overflow-y: scroll;">
    '''
    for color, name in color_name_pairs:
        legend_html += f'<div style="display: flex; align-items: center; margin: 5px;">'
        legend_html += f'<div style="background-color: {color}; width: 20px; height: 20px; margin-right: 5px;"></div>'
        legend_html += f'<span>{name}</span></div>'
    legend_html += '''
        </div>
    </div>
    '''
    map_obj.get_root().html.add_child(folium.Element(legend_html))

# 添加顏色圖例
add_color_legend(m, geojson_data_rail)

# 顯示地圖
m.to_streamlit(height=700)
