import sys
import os
from pathlib import Path

# Add root project path to Python's module search to fix ModuleNotFoundError
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import streamlit as st
from config.settings import settings
import database.schema as schema

def load_css():
    css_path = settings.BASE_DIR / 'app' / 'assets' / 'style.css'
    if css_path.exists():
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            
def initialize_system():
    # Initialize DB schema if it's the very first run
    try:
        schema.init_db()
    except Exception as e:
        # Ignore if tables already exist or path missing, log would handle it normally
        pass

st.set_page_config(
    page_title=settings.APP_NAME,
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load global configurations
load_css()
initialize_system()

st.title(f"Welcome to {settings.APP_NAME} 🌱")
st.markdown("""
This is your **Intelligent Farming Assistant**. 
Navigate through the sidebar to access ML-powered insights, environmental analyzers, and crop recommendations perfectly tailored to your farm's condition.

### Get Started
Please select a module from the left menu to begin.
""")

# Standard aesthetic footer
st.markdown("---")
st.caption("AgroMind AI 2026 • Premium Desktop Client • Python Core Architecture")
