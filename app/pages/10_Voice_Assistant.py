import streamlit as st
import time
import app.main as main
from app.components.sidebar import render_sidebar
from core.voice.listener import VoiceListener
from core.voice.speaker import VoiceSpeaker
from core.voice.ai_responder import AIResponder
from config.settings import settings

st.set_page_config(page_title="Voice Assistant", layout="wide")
main.load_css()
render_sidebar()

with st.sidebar:
    st.divider()
    st.markdown("### 🤖 Engine Configuration")
    user_api_key = st.text_input("Gemini API Key (Required for AI)", value=settings.GEMINI_API_KEY, type="password")

st.header("🗣️ AgroMind Voice Assistant")
st.markdown("Query the framework using standard microphone peripherals. Synthesized offline SAPI5 will respond verbally using Gemini AI.")

st.warning("**Hardware Notice:** This module requires an active, unmuted system microphone. Do not run this over a headless server without physical audio input enabled.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Audio Trigger")
    
    if st.button("🎙️ Activate Microphone (Listen for 5s)", use_container_width=True):
        status_box = st.info("Initializing microphone hardware. Please speak clearly...")
        
        # We explicitly lock progress in Streamlit so the user sees something is happening.
        # Transcription hits SpeechRecognition wrapped in Phase 4.
        transcribed_text = VoiceListener.listen_and_transcribe()
        
        if not transcribed_text:
            status_box.error("Silence detected, or SpeechRecognition API failed to convert audio.")
        else:
            status_box.success("Audio captured and converted successfully.")
            st.session_state['latest_voice_query'] = transcribed_text

with col2:
    st.markdown("### Conversation Log")
    
    query = st.session_state.get('latest_voice_query', None)
    if query:
        st.markdown(f"**You:** *\"{query}\"*")
        
        with st.spinner("AI is thinking..."):
            response = AIResponder.generate_response(query, api_key=user_api_key)
        st.markdown(f"<div style='background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;'><span style='color: #4ade80; font-weight:bold;'>AgroMind:</span> {response}</div>", unsafe_allow_html=True)
        
        with st.spinner("Synthesizing verbal offline response..."):
            VoiceSpeaker.synthesize_speech(response)
            time.sleep(1) # Allow thread to init safely inside the UI bound
    else:
        st.caption("No queries recorded in current session state.")
