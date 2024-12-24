import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd

st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("Marker Cluster")

# 讀取 CSV 檔案並轉換為 DataFrame
views = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E6%9D%B1%E4%BA%AC%E6%99%AF%E9%BB%9E.csv")
heat_data = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E5%90%84%E5%8D%80%E6%99%AF%E9%BB%9E%E6%95%B8%E9%87%8F.csv")
geojson_url = "https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E6%9D%B1%E4%BA%AC%E8%A1%8C%E6%94%BF%E5%8D%80%E5%88%86%E7%95%8C.geojson"  # 替換成你的 GeoJSON 文件 URL


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
        map_center = [35.68388267239132, 139.77317043877568]  # 東京的中心位置
    else:
        filtered_views = views[views['市町村名'] == selected_district]
        filtered_heat_data = heat_data[heat_data['市町村名'] == selected_district]
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

    # **添加 GeoJSON 圖層**
    m.add_geojson(
        geojson_url,
        layer_name="行政區域",
        style={
            "color": "blue",  # 邊界顏色
            "weight": 2,      # 邊界寬度
            "fillColor": "cyan",  # 填充顏色
            "fillOpacity": 0.2,   # 填充透明度
        },
    )

    # 新增圖層控制
    m.add_layer_control()

    # 顯示地圖
    m.to_streamlit(height=700)
