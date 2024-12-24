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
東京在日本一級行政區中排名第45位，但日本最南端（沖之鳥島）和最東端（南鳥島）均位於其轄區內，因此擁有日本各一級行政區中最大的經緯度跨度哦。
"""

st.sidebar.title("日本小知識")
st.sidebar.info(markdown)
logo = "https://img.olympics.com/images/image/private//f_auto/primary/utp8z5rbcrcqcbcnfswh"
st.sidebar.image(logo)

st.title("🥰觀光景點及熱點分佈")

"""
這一頁是觀光景點及熱點分佈，這邊你可以找到
"""
"""
-) 觀光景點及其熱點分佈圖
"""
"""
-) 觀光景點的表格及補充資訊
"""
"""
可以透過上面的按鈕搜尋想要的行政區哦
"""
"""
同時下方地圖也有定位功能哦
"""
"""
👈🏻按這邊有更多內容哦！

"""

# 讀取景點和熱區數據
views = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E6%9D%B1%E4%BA%AC%E6%99%AF%E9%BB%9E.csv")
heat_data = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E5%90%84%E5%8D%80%E6%99%AF%E9%BB%9E%E6%95%B8%E9%87%8F.csv")

# 讀取 GeoJSON 數據
geojson_url =  "https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E6%9D%B1%E4%BA%AC%E8%A1%8C%E6%94%BF%E5%8D%80%E5%88%86%E7%95%8C.geojson" # 替換成你的 URL

response = requests.get(geojson_url)
geojson_data = response.json()

# 確保緯度與經度欄位存在
if '緯度' not in views.columns or '經度' not in views.columns:
    st.error("CSV檔案中缺少緯度或經度欄位！")
else:
    # 獲取所有的行政區，並添加一個 "全部區域" 選項
    districts = ['全部區域'] + views['市町村名'].unique().tolist()
    
    # 添加選擇行政區的 selectbox 到應用程式的主要區域
    selected_district = st.selectbox('選擇行政區', districts)

    # 根據選擇的行政區過濾景點資料
    if selected_district == '全部區域':
        filtered_views = views
        filtered_heat_data = heat_data
        filtered_geojson = geojson_data  # 不過濾 GeoJSON
        map_center = [35.68388267239132, 139.77317043877568]  # 東京的中心位置
    else:
        # 過濾景點和熱區數據
        filtered_views = views[views['市町村名'] == selected_district]
        filtered_heat_data = heat_data[heat_data['市町村名'] == selected_district]

        # 過濾 GeoJSON 數據，根據 'laa' 欄位過濾
        filtered_geojson = {
        "type": "FeatureCollection",
        "features": [
            feature for feature in geojson_data["features"]
            if feature["properties"].get("市町村名") == selected_district
        ]
    }

        # 獲取該區的中心點
        district_data = heat_data[heat_data['市町村名'] == selected_district]
        map_center = [district_data['緯度'].mean(), district_data['經度'].mean()]
    
    # 初始化地圖
    m = leafmap.Map(center=map_center, zoom=12)

    # 添加篩選後的點標記
    m.add_points_from_xy(
        filtered_views,  # 使用篩選後的資料
        x="經度",
        y="緯度",
        spin=True,
        add_legend=True,
    )

    # 添加篩選後的熱區地圖
    m.add_heatmap(
        filtered_heat_data,  # 使用篩選後的資料
        latitude="緯度",
        longitude="經度",
        value="景點數量",
        name="Heat map",
        radius=20,
    )

    # 添加篩選後的 GeoJSON 圖層
    m.add_geojson(
        filtered_geojson,  # 使用篩選後的 GeoJSON 數據
        layer_name="行政區域",
        style={
            "color": "grey",  # 邊界顏色
            "weight": 1.5,      # 邊界寬度
            "opacity": 0.5,
            "fillColor": "white",  # 填充顏色
            "fillOpacity": 0.1,   # 填充透明度
        },
    )

    # 添加定位功能
    folium.plugins.LocateControl().add_to(m)

    # 新增圖層控制
    m.add_layer_control()

    # 顯示地圖
    m.to_streamlit(height=700)

    ########################################################
# 讀取景點展示數據
views_display = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E6%9D%B1%E4%BA%AC%E6%99%AF%E9%BB%9E_display.csv")

# 根據選擇的行政區過濾表格資料
if selected_district == "全部區域":
    filtered_display = views_display  # 不過濾
else:
    filtered_display = views_display[views_display["市町村名"] == selected_district]  # 過濾資料

# 顯示篩選後的表格
st.subheader(f"景點資料 - {selected_district}")
st.dataframe(filtered_display, height=400)  # 設置高度並讓表格可滾動

