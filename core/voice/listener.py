import speech_recognition as sr
from typing import Optional
from utils.logger import get_logger

logger = get_logger("VoiceListener")

class VoiceListener:
    @staticmethod
    def listen_and_transcribe(timeout_seconds: int = 5) -> Optional[str]:
        """
        Activates the default system microphone, records audio, and translates to text 
        using Google Web Speech. Highly experimental inside Streamlit.
        """
        recognizer = sr.Recognizer()
        
        try:
            with sr.Microphone() as source:
                logger.debug("Adjusting for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1.0)
                
                logger.info("Microphone Active: Listening for command...")
                audio = recognizer.listen(source, timeout=timeout_seconds, phrase_time_limit=10)
                
            logger.debug("Audio captured. Attempting transcription...")
            # Requires internet. Free tier.
            text = recognizer.recognize_google(audio)
            return text
            
        except sr.WaitTimeoutError:
            logger.warning("Listening timed out. No speech detected.")
            return None
        except sr.UnknownValueError:
            logger.warning("Speech unintelligible to algorithm.")
            return None
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech service: {e}")
            return None
        except Exception as e:
            logger.error(f"Microphone or Hardware Error: {e}")
            return None
