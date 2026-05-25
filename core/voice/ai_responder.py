from google import genai
from config.settings import settings
from utils.logger import get_logger

logger = get_logger("AIResponder")

class AIResponder:
    _client = None
    _configured_key = None
    
    @classmethod
    def _get_client(cls, api_key: str):
        if cls._configured_key != api_key or cls._client is None:
            cls._client = genai.Client(api_key=api_key)
            cls._configured_key = api_key
            logger.info("Configured Google Gemini API Client.")
        return cls._client

    @classmethod
    def generate_response(cls, query: str, api_key: str = None) -> str:
        """
        Generates an AI response using Google Gemini models, or falls back to local intent matching.
        """
        active_key = api_key or settings.GEMINI_API_KEY
        if not active_key or len(active_key) < 5:
            logger.info("No valid Gemini API key found, falling back to local intent parser.")
            return cls._local_intent_fallback(query)
            
        try:
            client = cls._get_client(active_key)
            
            instructions = (
                "You are the AgroMind AI Voice Assistant. You respond verbally to farmers. "
                "You help them understand agriculture, weather, crops, and how to navigate the AgroMind dashboard. "
                "Keep responses extremely concise, conversational, and direct. Do not use complex markdown, bullet points, or list formats, because your response will be read aloud by a Text-To-Speech engine."
            )
            
            # Incorporate system prompt directly cleanly
            full_prompt = f"System Instructions: {instructions}\n\nUser Query: {query}"
            
            logger.info(f"Generating AI response for: {query}")
            
            # Using standard recommended model for new genai SDK
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=full_prompt,
            )
            
            if response.text:
                # Remove markdown asterisks which TTS might pronounce literally
                clean_text = response.text.replace("*", "").replace("#", "").strip()
                return clean_text
            else:
                return "The AI model did not return a valid verbal response."
                
        except Exception as e:
            logger.error(f"Failed to generate AI response: {e}")
            return f"I encountered a cloud processing error: {str(e)}. However, I can still parse basic instructions offline."

    @staticmethod
    def _local_intent_fallback(user_query: str) -> str:
        lower_q = user_query.lower()
        
        # Greetings
        if any(word in lower_q for word in ["hello", "hi", "hey", "greetings"]):
            return "Hello! I am your offline AgroMind Assistant. How can I help you with your farming today?"
        elif any(word in lower_q for word in ["how are you", "who are you"]):
            return "I am the AgroMind Voice Assistant, operating in offline mode. I can help you with crop management, weather, and more."
        
        # Disease Detection
        elif any(word in lower_q for word in ["disease", "sick", "yellow", "spot", "wilt", "blight", "fungus", "pest", "bug"]):
            return "I recommend using the Disease Detection module. You can upload a photo of the affected plant leaf, and our local AI will identify the issue."
            
        # Crop Recommendation
        elif any(word in lower_q for word in ["recommend", "which crop", "what to grow", "what to plant", "best crop"]):
            return "To find the best crop for your field, please head over to the Crop Recommendation module. It analyzes your soil and weather to suggest options."
            
        # Fertilizer Advisor
        elif any(word in lower_q for word in ["fertilizer", "manure", "nutrient", "npk", "urea", "compost"]):
            return "To balance your soil's NPK levels and receive a custom fertilization plan, please visit the Fertilizer Advisor."
            
        # Weather Intelligence
        elif any(word in lower_q for word in ["weather", "rain", "temperature", "forecast", "climate", "storm", "sun"]):
            return "For accurate, real-time weather intelligence and upcoming forecasts, please navigate to the Weather Intelligence tab in the sidebar."
            
        # Yield Prediction
        elif any(word in lower_q for word in ["yield", "produce", "harvest", "output", "production"]):
            return "If you are looking to estimate your farm's productivity, try the Yield Prediction module."
            
        # Action Planner
        elif any(word in lower_q for word in ["plan", "schedule", "task", "action", "to do", "activity"]):
            return "Your Action Planner contains a schedule of your farming activities. Please check the Action Planner module to stay on top of your tasks."
            
        # Shop Locator
        elif any(word in lower_q for word in ["shop", "store", "buy", "purchase", "market", "seed", "equipment", "pesticides"]):
            return "Looking for farming supplies? The Shop Locator will show you nearby agricultural stores and markets on an interactive map."
            
        # Farm History
        elif any(word in lower_q for word in ["history", "past", "record", "previous"]):
            return "You can securely view your past farming logs, yields, and activities in the Farm History module."
            
        # Default fallback
        else:
            return "I heard you perfectly! Since I am offline without an API key, I operate on keywords. Ask me about recommendations, diseases, weather, or fertilizers!"
