import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import geopandas as gpd
import numpy as np
import geopandas as gpd
import plotly.express as px
import requests
import pydeck as pdk
import plotly.express as px


st.set_page_config(layout="wide")

# Customize the sidebar

st.sidebar.title("About")
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

# Customize page title
st.title("東京的旅遊景點以及鐵路視覺化")


st.header("簡介")

markdown = """
日本是台灣的熱門旅遊聖地，東京更是當中的佼佼者，我們希望能夠在這個Steamlit裡面視覺化東京的熱門旅遊景點以及相關旅遊配套！

"""

st.markdown(markdown)

# 準備數據
data = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E8%A7%80%E5%85%89%E5%AE%A2%E5%9C%8B%E7%B1%8D.csv")

geojson_url = "https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/tourism_comefrom.geojson"
geojson_data = requests.get(geojson_url).json()

st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v10",
        initial_view_state=pdk.ViewState(
            latitude=40.0,  # Center near Spain for better view
            longitude=0.0,
            zoom=1,
            pitch=45,
        ),
        layers=[
            pdk.Layer(
                "ColumnLayer",
                data,
                get_position="[X, Y]",  # Note: Longitude is X, Latitude is Y
                get_elevation="Number / 10",  # Set the elevation (height of the column) proportional to 'Number'
                elevation_scale=8000,  # Scale factor for elevation 誇張程度
                get_color=[0, 0, 255],  # Color of the columns RGBA
                radius=80000,  # Radius of the columns
                pickable=True,
            ),
            pdk.Layer(
                "GeoJsonLayer",  # Add GeoJSON layer
                geojson_data,  # Use the filtered GeoJSON
                get_fill_color=[255, 0, 0, 255],  # Color for the route line (red)
                get_line_color=[255, 0, 0],  # Line color for the route (red)
                line_width=4,  # Line width for the route
                pickable=True,
            )
        ],
    )
)
#########################################
pie = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E8%A7%80%E5%85%89%E5%AE%A2%E5%85%A5%E5%9C%8B%E6%A9%9F%E5%A0%B4%20%E6%A9%AB%E5%BC%8F.csv")
# 繪製圓餅圖
fig = px.pie(
    pie,
    names="國家/入境機場",
    values="全體",
    title="景點數量圓餅圖",
    hole=0,  # 中心空洞比例（甜甜圈圖效果）
)

st.plotly_chart(fig)
#########################################
# 確認資料格式
if pie.empty or len(pie.columns) < 2:
    st.error("數據有誤，請確認資料格式正確。")
else:
    # 選擇欄位
    st.sidebar.title("圓餅圖設定")
    columns = pie.columns.tolist()

    # 提供用戶選擇 X（名稱）和 Y（數值）
    selected_x = st.sidebar.selectbox("選擇名稱欄位 (X)", columns, index=columns.index("國家/入境機場") if "國家/入境機場" in columns else 0)
    selected_y = st.sidebar.selectbox("選擇數值欄位 (Y)", columns, index=columns.index("全體") if "全體" in columns else 1)

    # 選擇行政區
    districts = ["全部區域"] + pie["國家/入境機場"].unique().tolist()
    selected_district = st.sidebar.selectbox("國家", districts)

    # 過濾數據
    if selected_district == "全部區域":
        filtered_pie = pie
    else:
        filtered_pie = pie[pie["國家/入境機場"] == selected_district]

    # 繪製圓餅圖
    try:
        fig = px.pie(
            filtered_heat_data,
            names=selected_x,
            values=selected_y,
            title=f"圓餅圖 - {selected_district}",
            hole=0.2,  # 中心空洞比例
        )

        # 顯示圓餅圖
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"無法生成圓餅圖，請檢查選擇的欄位。錯誤訊息：{e}")
#########################################
chart_data = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E8%A7%80%E5%85%89%E5%AE%A2%E5%85%A5%E5%9C%8B%E6%A9%9F%E5%A0%B4_%E7%99%BE%E5%88%86%E6%AF%94.csv")
# Show the table of chart_data
st.table(chart_data)  # Display the chart data as a table



