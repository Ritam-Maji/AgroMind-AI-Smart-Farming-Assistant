import streamlit as st
import pandas as pd
import json
import app.main as main
from app.components.sidebar import render_sidebar
from database.repositories.history_repo import HistoryRepository

st.set_page_config(page_title="Farm History", layout="wide")
main.load_css()
render_sidebar()

st.header("🗄️ Analytical Farm History")
st.markdown("Chronological logs of interventions, model queries, and recommended solutions.")

# In a multi-user app, this would be scoped to user auth ID. Since isolated desktop app, we mock Farm ID = 1.
farm_id = 1

st.info("Currently viewing records for unified default Farm #1.")

records = HistoryRepository.get_history_for_farm(farm_id)

if not records:
    st.warning("No logged analytical history discovered in the SQLite database.")
else:
    # Flatten records for pandas
    df_list = []
    for r in records:
        flat_p = r.get("payload", {})
        if isinstance(flat_p, dict):
            payload_str = ", ".join([f"{k}: {v}" for k, v in flat_p.items()])
        else:
            payload_str = str(flat_p)
            
        df_list.append({
            "Timestamp": r.get('created_at'),
            "Interaction Type": r.get('rec_type'),
            "System Output Details": payload_str,
            "Documented Outcome": r.get('outcome', 'Pending/Unknown')
        })
        
    df = pd.DataFrame(df_list)
    # Streamlit dataframe natively supports the styling context built in Phase 3 globally!
    st.dataframe(df, use_container_width=True, hide_index=True)
