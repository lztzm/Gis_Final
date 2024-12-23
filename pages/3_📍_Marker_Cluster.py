import streamlit as st
import leafmap.foliumap as leafmap

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

m = leafmap.Map(center=(center_lat, center_lon), zoom=12)

views = "https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E6%9D%B1%E4%BA%AC%E6%99%AF%E9%BB%9E.csv"       m.add_geojson(regions, layer_name="US Regions")
    
m.add_points_from_xy(
    cities,
    x="經度",
    y="緯度",
    color_column="region",
    spin=True,
    add_legend=True,
)

heatmap_layer = leafmap.folium.FeatureGroup(name="熱區地圖")
m.add_heatmap(
    filepath,
    latitude="latitude",
    longitude="longitude",
    value="pop_max",
    name="Heat map",
    radius=20,
)

# 新增圖層控制
leafmap.folium.LayerControl().add_to(m)

# 顯示地圖
m.to_streamlit(height=700)
