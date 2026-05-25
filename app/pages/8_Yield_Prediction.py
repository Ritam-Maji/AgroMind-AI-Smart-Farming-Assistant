import streamlit as st
import app.main as main
from app.components.sidebar import render_sidebar
from core.yield_prediction.predictor import YieldPredictor

st.set_page_config(page_title="Yield Prediction", layout="wide")
main.load_css()
render_sidebar()

st.header("📈 Harvest Yield Prediction")
st.markdown("Estimate gross tonnage based on region, historical data, and current environment scoring.")

col1, col2 = st.columns([1, 1])

with col1:
    crop = st.text_input("Harvested Crop", value="Wheat")
    area = st.number_input("Field Area (Hectares)", min_value=0.1, value=10.0, step=0.5)
    env_health = st.slider("Environmental Health Slider (1.0 = Perfection)", 0.0, 1.0, 0.85)

    btn = st.button("Forecast Yield")

with col2:
    if btn:
        with st.spinner("Regressing metrics..."):
            predictor = YieldPredictor()
            result = predictor.predict_yield(crop, float(area), float(env_health))
            
        tonnage = result['estimated_tons']
        risk = result['risk_factor_percent']
        
        box_color = "#3b82f6"
        st.markdown(f"""
        <div style="background: rgba(59, 130, 246, 0.1); padding: 25px; border-radius: 16px; border: 1px solid rgba(59, 130, 246, 0.3); text-align: center;">
            <p style="margin: 0; color: #93c5fd; font-weight: 600; text-transform: uppercase;">Estimated Production</p>
            <h1 style="margin: 10px 0; color: #ffffff; font-size: 4rem;">{tonnage} <span style="font-size: 1.5rem; font-weight: normal;">Tons</span></h1>
            <p style="margin: 0; color: {'#ef4444' if risk > 50 else '#10b981'}; font-weight: bold;">Calculated Environmental Risk: {risk}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        if result['is_mocked']:
            st.caption("Note: Utilizing internal deterministic mapping while true Scikit-Learn '.pkl' weights are unpopulated.")
