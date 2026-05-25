import streamlit as st
import app.main as main
from app.components.sidebar import render_sidebar
from core.weather.client import WeatherClient
from core.planning.action_planner import ActionPlanner

st.set_page_config(page_title="Action Planner", layout="wide")
main.load_css()
render_sidebar()

st.header("📝 Daily Farm Action Plan")
st.markdown("Your optimized task list based on current weather limits and operational bounds.")

lat = st.session_state.get('farm_lat', 0.0)
lon = st.session_state.get('farm_lon', 0.0)

with st.spinner("Compiling algorithmic planner..."):
    weather = WeatherClient.get_7_day_forecast(lat, lon)
    tasks = ActionPlanner.generate_daily_plan(weather_data=weather, recent_anomalies=0)

if not tasks:
    st.info("No actionable tasks generated for today. Resume standard observation.")
else:
    for idx, t in enumerate(tasks):
        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 5px solid #10b981;">
            <p style="margin: 0; color: #a7f3d0; font-weight: bold;">{t['time']}</p>
            <h3 style="margin: 5px 0; color: #ffffff;">{t['task']}</h3>
            <p style="margin: 0; color: #9ca3af; font-size: 0.95rem;">{t['reason']}</p>
        </div>
        """, unsafe_allow_html=True)
