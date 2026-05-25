import pyttsx3
import threading
from utils.logger import get_logger

logger = get_logger("VoiceSpeaker")

class VoiceSpeaker:
    @staticmethod
    def _speak_thread(text: str):
        try:
            # We initialize pyttsx3 inside the thread to avoid COM context issues in Windows Streamlit apps
            engine = pyttsx3.init()
            
            # Configure slightly slower speaking rate for clarity
            rate = engine.getProperty('rate')
            engine.setProperty('rate', max(150, rate - 30))
            
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS synthesis failure: {e}")

    @staticmethod
    def synthesize_speech(text: str) -> None:
        """
        Converts text payload into offline SAPI5 audible speech.
        Fires in a daemon thread so Streamlit UI isn't hard-blocked while talking.
        """
        if not text:
            return
            
        logger.info(f"Synthesizing speech: {text}")
        t = threading.Thread(target=VoiceSpeaker._speak_thread, args=(text,))
        t.daemon = True
        t.start()
