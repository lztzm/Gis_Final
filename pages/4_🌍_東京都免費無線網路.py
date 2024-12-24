import os
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

# 設置頁面配置
st.set_page_config(layout="wide", page_title="Public Wireless LAN Data", page_icon=":globe_with_meridians:")

markdown = """
東京可以說是自動販賣機之城，到處都可以找到自動販賣機的蹤影。從飲料和小吃到雨傘、鮮花甚至新鮮雞蛋等更不尋常的物品，只有你想不到，沒有你買不到！
"""

st.sidebar.title("東京冷知識")
st.sidebar.info(markdown)
logo = "https://img.olympics.com/images/image/private//f_auto/primary/utp8z5rbcrcqcbcnfswh"
st.sidebar.image(logo)

"""
這一頁是東京都免費無線網路，這邊你可以找到
"""
"""
東京哪裡有免費的網絡~ 在這個時代，網絡可以說是人類最重要的東西之一！ 在這裡，你會知道哪裡可以蹭好蹭滿，就算旅遊的時候把網絡用完都沒關係！
"""
"""
👈🏻按這邊有更多內容哦！
"""

# 加載數據
@st.cache_resource
def load_data():
    path = "130001_public_wireless_lan_20240901.csv"
    if not os.path.isfile(path):
        path = f"https://github.com/qaz7000810/tower/raw/refs/heads/main/130001_public_wireless_lan_20240901.csv"

    try:
        data = pd.read_csv(
            path,
            usecols=[9, 10],  # 使用列索引來讀取第10和第11列
            encoding="iso-8859-1"  # 使用成功的編碼
        )
        data.columns = ["緯度", "経度"]  # 手動指定列名
        data["緯度"] = pd.to_numeric(data["緯度"], errors='coerce')  # 將緯度轉換為數字
        data["経度"] = pd.to_numeric(data["経度"], errors='coerce')  # 將経度轉換為數字
        data.dropna(subset=["緯度", "経度"], inplace=True)  # 丟棄包含 NaN 的行
        return data
    except Exception as e:
        st.write(f"Error loading data: {e}")
        return pd.DataFrame(columns=["緯度", "経度"])

# 繪製地圖函數
def map(data, lat, lon, zoom):
    try:
        st.write(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={
                    "latitude": lat,
                    "longitude": lon,
                    "zoom": zoom,
                    "pitch": 50,
                },
                layers=[
                    pdk.Layer(
                        "HexagonLayer",
                        data=data,
                        get_position=["経度", "緯度"],
                        radius=100,
                        elevation_scale=4,
                        elevation_range=[0, 1000],
                        pickable=True,
                        extruded=True,
                    ),
                ],
            )
        )
    except Exception as e:
        st.write(f"Error displaying map: {e}")

# 計算中點
@st.cache_data
def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))

# 主應用程序
data = load_data()

# 設置地圖縮放位置
if not data.empty:
    try:
        midpoint = mpoint(data["緯度"], data["経度"])
        st.title("🌍東京都免費無線網路")
        )
        map(data, midpoint[0], midpoint[1], 11)
    except Exception as e:
        st.write(f"Error in main application: {e}")
