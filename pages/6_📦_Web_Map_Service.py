pip install streamlit-folium

import streamlit as st
import folium
from folium.plugins import LocateControl
from streamlit_folium import st_folium
import geocoder

st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

# 顯示搜尋框
search_location = st.text_input("搜尋地點", "Tokyo")  # 預設為東京

# 使用 geocoder 取得搜尋地點的座標
g = geocoder.osm(search_location)

if g.ok:
    # 取得搜尋結果的座標
    lat, lng = g.latlng
    st.write(f"搜尋地點: {search_location} 的座標是：{lat}, {lng}")
else:
    st.write("無法找到該地點")

# 設置地圖
m = folium.Map(location=[lat, lng], zoom_start=12)  # 使用搜尋結果的座標初始化地圖

# 添加定位控制
LocateControl().add_to(m)

# 顯示地圖
st_folium(m, height=700)

m.to_streamlit(width, height)
