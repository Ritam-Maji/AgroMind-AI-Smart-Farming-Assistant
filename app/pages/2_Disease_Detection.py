import streamlit as st
import datetime
import json
import pandas as pd
from PIL import Image
from config.settings import settings

import app.main as main
from app.components.sidebar import render_sidebar
from app.components.risk_card import render_risk_card

from utils.image_utils import load_image
from core.disease.preprocessor import DiseasePreprocessor
from core.disease.detector import DiseaseDetector
from core.disease.explainer import DiseaseExplainer
from core.disease.risk_scorer import RiskScorer

st.set_page_config(page_title="Disease Detection", layout="wide")
main.load_css()
render_sidebar()

st.header("🦠 Intelligent Disease Detection")
st.markdown("Upload a close-up image of a crop leaf to identify pathogenic stresses.")

with st.expander("📊 View Model Training History"):
    history_path = settings.BASE_DIR / "models" / "disease" / "training_history.json"
    if history_path.exists():
        with open(history_path, "r") as f:
            history = json.load(f)
            
        if "train_acc" in history and "val_acc" in history:
            df = pd.DataFrame({
                "Train Accuracy": history["train_acc"],
                "Validation Accuracy": history["val_acc"]
            })
            st.line_chart(df)
            st.caption("CNN Model Accuracy Improvement over Epochs")
        else:
            st.warning("Training history format is invalid.")
    else:
        st.info("No training history found yet. Run `python scripts/train_disease.py` to train your model and view its learning curve here.")

st.markdown("---")

@st.cache_resource
def get_ml_pipeline():
    detector = DiseaseDetector()
    explainer = DiseaseExplainer(detector.model)
    return detector, explainer

detector, explainer = get_ml_pipeline()

uploaded_file = st.file_uploader("Choose a leaf image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    try:
        raw_image = load_image(uploaded_file)
        st.image(raw_image, caption="Uploaded Leaf via Camera", width=400)
        
        if st.button("Run Diagnostics Pipeline"):
            with st.spinner("Processing deep learning tensors..."):
                # 1. Preprocess
                tensor = DiseasePreprocessor.preprocess_image(raw_image)
                
                # 2. Detect
                disease_info, confidence = detector.predict(tensor)
                disease_name = disease_info.get("name", "Unknown")
                disease_cause = disease_info.get("cause", "Unknown Cause")
                disease_solution = disease_info.get("solution", [])
                
                # 3. Explain
                heatmap = explainer.generate_heatmap(tensor, raw_image)
                
                # 4. Score
                score_data = RiskScorer.calculate_integrated_risk(confidence, "MEDIUM", 0)

            st.markdown("---")
            st.subheader("Diagnostic Results")
            
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.metric("Detected Classification", disease_name)
                st.metric("Neural Confidence", f"{confidence * 100:.1f}%")
                
            with res_col2:
                st.markdown("**Grad-CAM Explainability Heatmap**")
                st.image(heatmap, caption="Red/Hot areas indicate model focus points.", width=400)
                
            st.markdown("---")
            st.subheader("Diagnosis Details")
            
            detail_col1, detail_col2 = st.columns(2)
            with detail_col1:
                st.markdown(f"**Pathogenic Cause:**\n\n{disease_cause}")
                
            with detail_col2:
                st.markdown("**Recommended Solution:**")
                if disease_solution:
                    for sol in disease_solution:
                        st.markdown(f"- {sol}")
                else:
                    st.markdown("No specific treatments listed.")
            
            st.markdown("---")
            st.subheader("Overall Action Risk")
            render_risk_card(score_data["composite_score_100"], score_data["action_level"])
                
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
