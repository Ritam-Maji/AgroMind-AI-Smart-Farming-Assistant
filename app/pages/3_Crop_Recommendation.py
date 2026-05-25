import streamlit as st
import app.main as main
from app.components.sidebar import render_sidebar
from core.recommendation.crop_advisor import CropAdvisor

st.set_page_config(page_title="Crop Recommendation", layout="wide")
main.load_css()
render_sidebar()

st.header("🌾 Smart Crop Recommendation")
st.markdown("Determine the most viable crops for your exact geographical and soil parameters.")

col1, col2 = st.columns([1, 2])

with col1:
    with st.container():
        st.subheader("Your Input Profile")
        soil = st.selectbox("Soil Type", ["Alluvial", "Black", "Red", "Laterite", "Arid"], index=0)
        temp = st.slider("Expected Average Temperature (°C)", -10.0, 50.0, 25.0)
        rainfall = st.slider("Expected Annual Rainfall (mm)", 0, 3000, 500)
        
        btn = st.button("Generate Recommendations")

with col2:
    if btn:
        with st.spinner("Analyzing soil and climate requirements..."):
            advisor = CropAdvisor()
            recs = advisor.get_recommendations(soil, temp, rainfall)
            
        if not recs:
            st.warning("No crops exactly matched these constraints. Try broadening your parameters.")
        else:
            st.success(f"Discovered {len(recs)} highly viable crops!")
            for r in recs:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #10b981;">
                    <h3 style="margin:0; color:#4ade80;">{r['crop_name']} <span style="font-size: 1rem; color: #a7f3d0; font-weight: 300;">(Confidence: {r['confidence_score']*100:.1f}%)</span></h3>
                    <p style="margin: 5px 0 0 0;"><strong>Ideal Season:</strong> {r['season']} | <strong>Expected Yield:</strong> {r['expected_yield']} tons/ha</p>
                    <p style="margin: 5px 0 0 0;"><small>Tags: {", ".join(r['tags'])}</small></p>
                </div>
                """, unsafe_allow_html=True)
