import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import requests
import folium
import json
from folium import plugins

st.set_page_config(layout="wide")

markdown = """
東京都是位於日本關東地方的一級行政區，也是日本首都，是日本唯一以「都」命名的行政區哦。
"""

st.sidebar.title("東京冷知識")
st.sidebar.info(markdown)
logo = "https://img.olympics.com/images/image/private//f_auto/primary/utp8z5rbcrcqcbcnfswh"
st.sidebar.image(logo)

st.title("🚃東京鐵路圖")

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

# 提供選擇行政區的功能
districts = ['全部區域'] + list(set([feature["properties"].get("市町村名", "Unknown") for feature in geojson_data["features"]]))
selected_district = st.selectbox('選擇行政區', districts)

# 確保緯度與經度欄位存在
if '緯度' not in station.columns or '經度' not in station.columns:
    st.error("CSV檔案中缺少緯度或經度欄位！")
else:
    # 根據選擇的行政區過濾景點資料
    if selected_district == '全部區域':
        filtered_station = station
        filtered_heat_data = heat_data
        filtered_geojson = geojson_data  # 顯示所有區域
        filtered_geojson_rail = geojson_data_rail
        map_center = [35.68388267239132, 139.77317043877568]  # 東京的中心位置
    else:
        filtered_station = station[station['市町村名'] == selected_district]
        filtered_heat_data = heat_data[heat_data['市町村名'] == selected_district]
        filtered_geojson = {
            "type": "FeatureCollection",
            "features": [feature for feature in geojson_data["features"] if feature["properties"].get("市町村名", "") == selected_district]
        }
        filtered_geojson_rail = geojson_data_rail  # 可選擇過濾鐵路路線
        # 獲取該區的中心點
        district_data = heat_data[heat_data['市町村名'] == selected_district]
        map_center = [district_data['緯度'].mean(), district_data['經度'].mean()]

    # 添加篩選後的 GeoJSON 圖層
    m.add_geojson(
        filtered_geojson,  # 使用篩選後的 GeoJSON 數據
        layer_name="行政區域",
        style={
            "color": "grey",  # 邊界顏色
            "weight": 1.5,      # 邊界寬度
            "opacity": 0.5,     # Line transparency
            "fillColor": "none",  # 填充顏色
        },
    )

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
        filtered_geojson_rail,  # 使用篩選後的鐵路路線數據
        layer_name="鐵路路線",
        style_function=style_function,  # 使用自定義樣式函數
    )

    # 添加景點圖層
    m.add_points_from_xy(
        filtered_station,  # 使用篩選後的資料
        x="經度",
        y="緯度",
        spin=True,
        add_legend=True,
    )

    # 添加定位功能
    folium.plugins.LocateControl().add_to(m)

    # 新增圖層控制
    m.add_layer_control()

    # 顯示地圖
    m.to_streamlit(height=700)
    #################################
st.image("https://www.tokyometro.jp/tcn/subwaymap/img/img_01.png")

