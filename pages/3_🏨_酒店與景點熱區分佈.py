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

st.title("🏨酒店與景點熱區分佈")

# 讀取景點和熱區數據
Hotel = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E9%85%92%E5%BA%97%E5%90%8D%E5%96%AE.csv")
heat_data = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E5%90%84%E5%8D%80%E6%99%AF%E9%BB%9E%E6%95%B8%E9%87%8F.csv")
railway_url = "https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E6%9D%B1%E4%BA%AC%E9%90%B5%E8%B7%AF.geojson"

response_railway = requests.get(railway_url)
geojson_data_rail = response_railway.json()

m = leafmap.Map(center=[35.68388267239132, 139.77317043877568], zoom=12)
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
 radius=25,
 opacity = 0.2,
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
 geojson_data_rail,  # 使用篩選後的鐵路路線數據
 layer_name="鐵路路線",
 style_function=style_function,  # 使用自定義樣式函數
)

    # 添加定位功能
folium.plugins.LocateControl().add_to(m)

    # 新增圖層控制
m.add_layer_control()

    # 顯示地圖
m.to_streamlit(height=700)

    ########################################################
# 根據選擇的行政區顯示表格
Hotel_display = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E9%85%92%E5%BA%97%E5%90%8D%E5%96%AE_display.csv")
st.subheader("飯店資料")
st.dataframe(Hotel_display, height=400)  # 設置高度並讓表格可滾動
