import streamlit as st
import app.main as main
from app.components.sidebar import render_sidebar
from core.recommendation.fertilizer_advisor import FertilizerAdvisor

st.set_page_config(page_title="Fertilizer & Nutrient Advisor", layout="wide")
main.load_css()
render_sidebar()

# Page title and description
st.markdown("""
<div style="margin-bottom: 25px;">
    <h1 style="margin: 0; color: #4ade80;">🧪 Fertilizer & Nutrient Advisor</h1>
    <p style="color: #a7f3d0; font-size: 1.1rem; margin-top: 5px;">
        Receive tailored crop-specific fertilizing strategies, dynamically adjusted for soil deficits, farming modes, and disease severity.
    </p>
</div>
""", unsafe_allow_html=True)

# Layout division: Input sidebar-style column and output result column
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.03); padding: 18px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.08);">
        <h3 style="margin:0 0 15px 0; color: #4ade80; font-size: 1.25rem;">🌾 Input Farm Conditions</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 1. Target Crop Selector
    popular_crops = [
        "Wheat", "Rice", "Maize", "Potato", "Tomato", "Cotton", 
        "Sugarcane", "Soybean", "Other / Custom"
    ]
    selected_crop_option = st.selectbox("Target Crop", popular_crops, index=0)
    
    if selected_crop_option == "Other / Custom":
        crop_name = st.text_input("Enter Custom Crop Name", value="Barley")
    else:
        crop_name = selected_crop_option
        
    # 2. Farming Mode
    mode = st.selectbox(
        "Farming Mode", 
        ["Standard", "Organic", "Urgent Fix", "High Yield"],
        help="Standard uses minerals; Organic uses natural fertilizers; Urgent Fix focuses on rapid spray absorption; High Yield pushes maximum productivity."
    )
    
    # 3. Disease Severity
    disease_sev = st.radio(
        "Current Disease Severity", 
        ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
        horizontal=True,
        help="High/Critical disease status automatically dials down Nitrogen to inhibit pathogen growth and boosts Potassium to strengthen defenses."
    )
    
    # 4. Optional Soil Nutrient Levels
    with st.expander("🧪 Soil Test Analysis (Optional)", expanded=False):
        st.markdown("<small style='color: #a7f3d0;'>Provide your soil's general N-P-K classification to calculate precise deficits.</small>", unsafe_allow_html=True)
        soil_n = st.selectbox("Soil Nitrogen (N) Status", ["Medium", "Low", "High"], index=0)
        soil_p = st.selectbox("Soil Phosphorus (P) Status", ["Medium", "Low", "High"], index=0)
        soil_k = st.selectbox("Soil Potassium (K) Status", ["Medium", "Low", "High"], index=0)
    
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    btn = st.button("Generate Fertilizer Prescription", use_container_width=True)

# Initialize Session State to persist calculation results
if 'fert_result' not in st.session_state:
    st.session_state.fert_result = None

# If button clicked, generate results
if btn:
    with st.spinner("Analyzing soil profiles and crop-specific N-P-K parameters..."):
        adv = FertilizerAdvisor()
        st.session_state.fert_result = adv.get_recommendations(
            crop_name=crop_name,
            disease_severity=disease_sev,
            mode=mode,
            soil_n=soil_n,
            soil_p=soil_p,
            soil_k=soil_k
        )

# Render results column
with col2:
    if st.session_state.fert_result is None:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.02); border: 2px dashed rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 60px; text-align: center; margin-top: 5px;">
            <span style="font-size: 50px;">🧪</span>
            <h3 style="margin-top: 15px; color: #86efac;">Awaiting Input</h3>
            <p style="color: #94a3b8; font-size: 0.95rem; max-width: 400px; margin: 5px auto 0 auto;">
                Set your target crop, soil test stats, and farming mode on the left, then click <strong>Generate Fertilizer Prescription</strong> to compute the scientific recipe.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        res = st.session_state.fert_result
        crop_disp = res['crop_name']
        mode_disp = res['mode']
        sev_disp = res['disease_severity']
        
        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.08); padding: 15px; border-radius: 12px; border-left: 5px solid #10b981; margin-bottom: 20px;">
            <h3 style="margin: 0; color: #ffffff; font-size: 1.4rem;">🔬 Prescription for {crop_disp}</h3>
            <p style="margin: 5px 0 0 0; color: #a7f3d0; font-size: 0.9rem;">
                Farming Mode: <strong>{mode_disp}</strong> • Disease Severity: <strong style="color: {'#ef4444' if sev_disp in ['HIGH', 'CRITICAL'] else '#fbbf24' if sev_disp == 'MEDIUM' else '#34d399'}">{sev_disp}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Section 1: Nutrient Budget (Base vs Adjusted)
        st.markdown("### 📊 Nutrient Target Budget (kg/hectare)")
        
        # Display elegant metrics comparing Base vs Adjusted
        m_col1, m_col2, m_col3 = st.columns(3)
        
        with m_col1:
            base_n = res['base_npk']['N']
            adj_n = res['adjusted_npk']['N']
            diff_n = round(adj_n - base_n, 1)
            delta_str = f"{diff_n:+d} kg" if diff_n != 0 else "Optimal"
            
            st.metric(
                label="Nitrogen (N) Target",
                value=f"{adj_n} kg/ha",
                delta=delta_str if diff_n != 0 else None,
                delta_color="normal" if diff_n <= 0 else "inverse" # nitrogen reduction is good in disease
            )
            
        with m_col2:
            base_p = res['base_npk']['P']
            adj_p = res['adjusted_npk']['P']
            diff_p = round(adj_p - base_p, 1)
            delta_str = f"{diff_p:+d} kg" if diff_p != 0 else "Optimal"
            
            st.metric(
                label="Phosphorus (P) Target",
                value=f"{adj_p} kg/ha",
                delta=delta_str if diff_p != 0 else None
            )
            
        with m_col3:
            base_k = res['base_npk']['K']
            adj_k = res['adjusted_npk']['K']
            diff_k = round(adj_k - base_k, 1)
            delta_str = f"{diff_k:+d} kg" if diff_k != 0 else "Optimal"
            
            st.metric(
                label="Potassium (K) Target",
                value=f"{adj_k} kg/ha",
                delta=delta_str if diff_k != 0 else None
            )

        # Section 2: Adaptations Info list
        if res['adjustments']:
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            with st.expander("🛠️ Agronomic Calculations & Adjustments Explained", expanded=True):
                for adj in res['adjustments']:
                    # Highlight critical disease warnings
                    if "⚠️" in adj or "🚨" in adj or "CRITICAL" in adj:
                        st.markdown(f"<div style='background: rgba(239, 68, 68, 0.08); padding: 8px 12px; border-radius: 6px; margin-bottom: 6px; font-size: 0.88rem; color: #fca5a5;'>{adj}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='background: rgba(255, 255, 255, 0.03); padding: 8px 12px; border-radius: 6px; margin-bottom: 6px; font-size: 0.88rem; color: #e2f0e5; border-left: 3px solid #34d399;'>{adj}</div>", unsafe_allow_html=True)

        # Section 3: Exact Doses Cards
        st.markdown("### 🛒 Prescribed Fertilizer Doses")
        
        # Display as elegant glassmorphic cards
        recs = res['recommendations']
        
        if not recs:
            st.info("No matching fertilizers found for this specific mode and severity combination.")
        else:
            # Grid layout for fertilizer cards (2 columns per row)
            for i in range(0, len(recs), 2):
                grid_cols = st.columns(2)
                for j in range(2):
                    idx = i + j
                    if idx < len(recs):
                        r = recs[idx]
                        badge_color = "#3b82f6" if r['type'] == 'Chemical' else "#10b981"
                        
                        with grid_cols[j]:
                            st.markdown(f"""
                            <div style="background: rgba(255, 255, 255, 0.04); padding: 18px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 15px; min-height: 230px; display: flex; flex-direction: column; justify-content: space-between;">
                                <div>
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                        <h4 style="margin: 0; color: #ffffff; font-size: 1.1rem; font-weight: 600;">{r['name']}</h4>
                                        <span style="font-size: 0.75rem; background: {badge_color}; color: #ffffff; padding: 2px 8px; border-radius: 10px; font-weight: bold;">
                                            {r['type']}
                                        </span>
                                    </div>
                                    <div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 10px;">
                                        NPK Profile: <code style="background: rgba(255,255,255,0.1); padding: 2px 5px; border-radius: 4px; color: #4ade80;">{r['n_p_k']}</code>
                                    </div>
                                    <div style="margin: 10px 0;">
                                        <div style="font-size: 1.7rem; font-weight: 700; color: #4ade80; display: inline-block;">
                                            {r['dosage_kg_ha']:,} <span style="font-size: 0.9rem; font-weight: normal; color: #a7f3d0;">kg/ha</span>
                                        </div>
                                        <div style="font-size: 0.9rem; color: #a7f3d0; margin-top: 2px;">
                                            Equivalent to: <strong>{r['dosage_kg_acre']:,} kg/acre</strong>
                                        </div>
                                    </div>
                                    <div style="margin-top: 10px; font-size: 0.85rem; color: #e2f0e5;">
                                        <strong>Application:</strong> {r['method']}
                                    </div>
                                </div>
                                <div style="margin-top: 12px; padding-top: 10px; border-top: 1px solid rgba(255, 255, 255, 0.05); font-size: 0.8rem; color: #fca5a5; font-style: italic;">
                                    ⚠️ {r['cautions']}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
        # Section 4: Split application timeline
        if res['splits']:
            st.markdown("### 📅 Optimal Splitting & Timing Schedule")
            st.markdown("<p style='color: #a7f3d0; font-size: 0.88rem; margin-top: -8px; margin-bottom: 15px;'>Applying fertilizer in synchronized stages dramatically increases plant absorption and minimizes environmental runoff.</p>", unsafe_allow_html=True)
            
            # Display split timeline
            for stage, formulation in res['splits'].items():
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.02); padding: 12px 18px; border-radius: 8px; border-left: 4px solid #4ade80; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;">
                    <div style="font-weight: 600; color: #ffffff; font-size: 0.95rem;">
                        ⏱️ {stage}
                    </div>
                    <div style="background: rgba(74, 222, 128, 0.1); color: #4ade80; padding: 4px 12px; border-radius: 6px; font-size: 0.9rem; font-weight: 600; border: 1px solid rgba(74, 222, 128, 0.2);">
                        {formulation}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("""
            <div style="margin-top: 20px; background: rgba(59, 130, 246, 0.05); border: 1px solid rgba(59, 130, 246, 0.1); padding: 12px; border-radius: 8px; font-size: 0.85rem; color: #93c5fd; text-align: center;">
                💡 <strong>Tip:</strong> Always ensure sufficient soil moisture (either via rainfall or irrigation) prior to applying fertilizer top-dressings.
            </div>
            """, unsafe_allow_html=True)
