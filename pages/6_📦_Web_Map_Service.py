import streamlit as st
import pydeck as pdk
import geocoder


st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

# 讓用戶輸入要搜尋的地點
search_location = st.text_input("搜尋地點", "Tokyo")  # 預設為 Tokyo

# 使用 geocoder 查詢地點的經緯度
# 設置 User-Agent 用來識別你的應用程式
g = geocoder.osm(search_location, headers={'gisfinal-k6feevkdz3yjadgbifgezt': 'streamlit-app/1.0'})

if g.ok:
    lat, lng = g.latlng
    st.write(f"搜尋地點: {search_location} 的座標是：{lat}, {lng}")
else:
    st.write("無法找到該地點")
