import streamlit as st
import pandas as pd
import app.main as main
from app.components.sidebar import render_sidebar
from core.weather.client import WeatherClient
from core.weather.advisor import WeatherAdvisor

st.set_page_config(page_title="Weather Intelligence", layout="wide")
main.load_css()
render_sidebar()

st.header("☁️ 7-Day Weather Intelligence")
city = st.session_state.get('farm_city', 'Unknown Location')
lat = st.session_state.get('farm_lat', 0.0)
lon = st.session_state.get('farm_lon', 0.0)

st.markdown(f"Fetching precise micro-climate data for **{city}** ({lat}, {lon})...")

with st.spinner("Connecting to Open-Meteo Satellites..."):
    data = WeatherClient.get_7_day_forecast(lat, lon)
    
if data and "daily" in data:
    daily = data["daily"]
    dates = daily.get("time", [])
    t_max = daily.get("temperature_2m_max", [])
    t_min = daily.get("temperature_2m_min", [])
    precip = daily.get("precipitation_sum", [])
    
    # 1. Visualization
    st.subheader("Temperature & Precipitation Trends")
    df = pd.DataFrame({
        "Date": dates,
        "Max Temp (°C)": t_max,
        "Min Temp (°C)": t_min,
        "Rainfall (mm)": precip
    }).set_index("Date")
    
    st.line_chart(df[["Max Temp (°C)", "Min Temp (°C)"]], use_container_width=True)
    st.bar_chart(df[["Rainfall (mm)"]], use_container_width=True)
    
    # 2. Advisories
    st.markdown("---")
    st.subheader("AI Meteorological Advisories")
    advisories = WeatherAdvisor.generate_advisories(data)
    for adv in advisories:
        if "Alert" in adv or "Warning" in adv:
            st.error(adv)
        elif "Heavy" in adv:
            st.warning(adv)
        else:
            st.info(adv)
else:
    st.error("Failed to load weather data. Please ensure internet connectivity and try again.")
