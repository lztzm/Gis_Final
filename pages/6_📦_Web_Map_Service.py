import streamlit as st
import pydeck as pdk
import geocoder


st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""
import streamlit as st

# 顯示搜尋框
search_location = st.text_input("搜尋地點", "Tokyo")  # 預設為東京

# 使用 geocoder 取得搜尋地點的座標
g = geocoder.osm(search_location)

if g.ok:
    lat, lng = g.latlng
    st.write(f"搜尋地點: {search_location} 的座標是：{lat}, {lng}")

    # 創建 Deck
    deck = pdk.Deck(
        initial_view_state=pdk.ViewState(latitude=lat, longitude=lng, zoom=12),
        layers=[],
    )

    # 顯示地圖
    st.pydeck_chart(deck)
else:
    st.write("無法找到該地點")
