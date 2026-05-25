import folium
from streamlit_folium import st_folium

def render_farm_map(lat: float, lon: float, markers=None):
    """
    Renders an interactive OpenStreetMap view centered on the farm.
    """
    m = folium.Map(location=[lat, lon], zoom_start=12)
    
    # Base Farm marker
    folium.Marker(
        [lat, lon],
        popup="Your Farm",
        icon=folium.Icon(color="green", icon="leaf")
    ).add_to(m)
    
    # Process additional dynamic markers (e.g. shops)
    if markers:
        for marker in markers:
            folium.Marker(
                [marker['lat'], marker['lon']],
                popup=marker.get('name', 'Unknown'),
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)
            
    # Render inside streamlit natively
    st_folium(m, width=700, height=400)
