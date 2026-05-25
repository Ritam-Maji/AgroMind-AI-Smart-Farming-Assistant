import streamlit as st

def render_risk_card(risk_score: float, action_level: str):
    """
    Renders a premium visual card denoting the risk score using Streamlit containers and columns.
    """
    color = "#10b981" # Green
    if risk_score > 75:
        color = "#ef4444" # Red
    elif risk_score > 40:
        color = "#f59e0b" # Yellow
        
    # We use some HTML inside markdown to bypass streamlit's rigid metric colors for this specific UI
    html = f"""
    <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 12px; border-left: 5px solid {color}; margin-bottom: 20px;">
        <h4 style="margin:0; color: #e2f0e5;">Composite Risk Score</h4>
        <h1 style="margin:0; color: {color}; font-size: 3rem;">{risk_score:.1f}<span style="font-size: 1rem; color: #a7f3d0;"> / 100</span></h1>
        <p style="margin: 5px 0 0 0; color: #9ca3af; font-weight: 600;">Status: {action_level}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
