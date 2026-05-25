import streamlit as st
from config.settings import settings
import database.schema as schema
from app.components.sidebar import render_sidebar
from app.components.risk_card import render_risk_card
from core.weather.client import WeatherClient
from core.environment.analyzer import EnvironmentAnalyzer

st.set_page_config(page_title="Dashboard | AgroMind", layout="wide")
import app.main as main
main.load_css()
render_sidebar()

city = st.session_state.get('farm_city', 'Unknown Location')
st.header(f"🎛️ Command Dashboard - {city}")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Farm Vitlas Preview")
    
    # Fetch real weather for the current configured coordinate
    lat = st.session_state.get('farm_lat', 0.0)
    lon = st.session_state.get('farm_lon', 0.0)
    
    with st.spinner("Syncing sensors and Open-Meteo..."):
        weather_data = WeatherClient.get_7_day_forecast(lat, lon)
        
    temp = 25.0
    humid = 50.0
    rain_prob = "Low"
    
    if weather_data and "current" in weather_data:
        temp = weather_data["current"]["temperature_2m"]
        humid = weather_data["current"]["relative_humidity_2m"]
        precip = weather_data["current"].get("precipitation", 0.0)
        rain_prob = "High" if precip > 0.5 else "Medium" if precip > 0.0 else "Low"
        
    mcol1, mcol2, mcol3 = st.columns(3)
    mcol1.metric("Local Temp (Current)", f"{temp}°C")
    mcol2.metric("Relative Humidity", f"{humid}%")
    mcol3.metric("Rain Probability", rain_prob)
    
    st.markdown("### Environment Analyzer")
    analysis = EnvironmentAnalyzer.analyze_conditions(temp, humid, 6.5, 0)
    
    if analysis['anomalies_count'] == 0:
        st.success("All environmental bounds are within highly favorable limits.")
    else:
        for anomaly in analysis['anomalies_detected']:
            st.warning(anomaly)

with col2:
    st.markdown("### Overview")
    render_risk_card(15.0, "Monitoring")
    
    st.markdown("---")
    st.info("💡 **Quick Tip:** Switch to the Disease Detection tab to scan a leaf manually if you notice yellowing.")
