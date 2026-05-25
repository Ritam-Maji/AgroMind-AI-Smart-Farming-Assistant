import streamlit as st
from core.location.geocoder import Geocoder

def render_sidebar():
    """
    Renders global context variables (Farm Location, Soil Type) into session state
    enabling global usage across pages.
    """
    st.sidebar.markdown("### 🌾 Your Farm Context")
    
    # 1. Initialize Auto-Detection
    if "farm_lat" not in st.session_state or "farm_lon" not in st.session_state:
        loc_data = Geocoder.detect_ip_location()
        if loc_data:
            st.session_state.farm_lat = loc_data["lat"]
            st.session_state.farm_lon = loc_data["lon"]
            st.session_state.farm_city = loc_data["city"]
        else:
            # Fallback to Delhi
            st.session_state.farm_lat = 28.6139  
            st.session_state.farm_lon = 77.2090
            st.session_state.farm_city = "Delhi"

    if "farm_city" not in st.session_state:
        st.session_state.farm_city = "Unknown"

    if "farm_soil" not in st.session_state:
        st.session_state.farm_soil = "Alluvial"
        
    # Display current location
    st.sidebar.markdown(f"""
    <div style="background: rgba(16, 185, 129, 0.1); padding: 10px; border-radius: 8px; border-left: 3px solid #10b981; margin-bottom: 15px;">
        <div style="font-size: 0.85rem; color: #a7f3d0;">📍 Current Location</div>
        <div style="font-size: 1.05rem; font-weight: bold; color: #ffffff;">{st.session_state.farm_city}</div>
        <div style="font-size: 0.75rem; color: #94a3b8; margin-top: 2px;">({st.session_state.farm_lat:.4f}, {st.session_state.farm_lon:.4f})</div>
    </div>
    """, unsafe_allow_html=True)
        
    with st.sidebar.form("context_form"):
        st.markdown("**Update Location via City Search**")
        search_query = st.text_input("City / Region Name", placeholder="e.g. Mumbai, Nairobi")
        
        st.session_state.farm_soil = st.selectbox("Soil Type", 
            ["Alluvial", "Black", "Red", "Laterite", "Arid", "Forest and Mountain"],
            index=["Alluvial", "Black", "Red", "Laterite", "Arid", "Forest and Mountain"].index(st.session_state.farm_soil)
        )
        
        submitted = st.form_submit_button("Update Settings")
        if submitted:
            if search_query.strip():
                coords = Geocoder.get_coordinates(search_query)
                if coords:
                    st.session_state.farm_lat, st.session_state.farm_lon = coords
                    st.session_state.farm_city = search_query.title()
                    st.rerun()
                else:
                    st.error("City not found. Please try another name.")
            else:
                st.success("Soil type updated!")
            
    st.sidebar.markdown("---")
    st.sidebar.caption("System Status: **Online**")
