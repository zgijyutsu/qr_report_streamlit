import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st
import requests
import json

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.title("QR Report")


# LOAD DATA ONCE
# @st.cache_resource
def load_data():
    res = requests.get(
        "https://ei8q66xnw1.execute-api.ap-northeast-1.amazonaws.com/test/retrieve_qrreport?duration_minutes=1440"
    )
    data = json.loads(res.__dict__["_content"])

    df = pd.DataFrame(data)
    st.write("最新24時間のデータを表示")
    return df


# FUNCTION FOR AIRPORT MAPS
def map(data, lat, lon, zoom):
    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v8",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 10,
            },
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=data,
                    get_position="[lon, lat]",
                    radius=300,
                    elevation_scale=4,
                    elevation_range=[0, 5000],
                    pickable=True,
                    extruded=True,
                ),
            ],
        )
    )


# CALCULATE MIDPOINT FOR GIVEN SET OF DATA
# @st.cache_data
def mpoint(lat, lon):
    return np.average(lat), np.average(lon)


def list_report(data):
    data
    pass


# STREAMLIT APP LAYOUT
data = load_data()

# SETTING THE ZOOM LOCATIONS FOR THE AIRPORTS
zoom_level = 12
midpoint = mpoint(data["lat"], data["lon"])
map(data, midpoint[0], midpoint[1], 8.5)
list_report(data)
