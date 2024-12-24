import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import geopandas as gpd
import json
import folium
from folium.plugins import LocateControl

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
views = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E6%9D%B1%E4%BA%AC%E6%99%AF%E9%BB%9E.csv")
heat_data = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E5%90%84%E5%8D%80%E6%99%AF%E9%BB%9E%E6%95%B8%E9%87%8F.csv")

# 讀取 GeoJSON 數據
geojson_url = "https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E6%9D%B1%E4%BA%AC%E8%A1%8C%E6%94%BF%E5%8D%80%E5%88%86%E7%95%8C.geojson"  # 替換成你的 URL
geojson_data = gpd.read_file(geojson_url)

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
        filtered_geojson = geojson_data[geojson_data["laa"] == selected_district]

        # 獲取該區的中心點
        district_data = heat_data[heat_data['市町村名'] == selected_district]
        map_center = [district_data['緯度'].mean(), district_data['經度'].mean()]
    
    # 將篩選後的 GeoJSON 轉換為 JSON
    filtered_geojson_json = json.loads(filtered_geojson.to_json())

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
        filtered_geojson_json,  # 使用篩選後的 GeoJSON 數據
        layer_name="行政區域",
        style={
            "color": "grey",  # 邊界顏色
            "weight": 1.5,      # 邊界寬度
            "opacity": 0.5
            "fillColor": "wihte",  # 填充顏色
            "fillOpacity": 0.1,   # 填充透明度
        },
    )

    # 添加定位功能
    folium.plugins.LocateControl().add_to(m)

    # 新增圖層控制
    m.add_layer_control()

    # 顯示地圖
    m.to_streamlit(height=700)
