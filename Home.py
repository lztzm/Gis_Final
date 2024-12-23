import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import geopandas as gpd

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

data = gd.read_csv("https://github.com/qaz7000810/tower/blob/main/%E8%A7%80%E5%85%89%E5%AE%A2%E5%85%A5%E5%9C%8B%E6%A9%9F%E5%A0%B4.csv")

m = leafmap.Map(minimap_control=True)
  
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
