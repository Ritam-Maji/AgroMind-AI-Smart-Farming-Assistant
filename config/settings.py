import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "AgroMind AI")
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    
    # Database Settings
    _db_path_str: str = os.getenv("DB_PATH", "data/agromind.db")
    DB_PATH: Path = BASE_DIR / _db_path_str
    
    # Cache Settings
    _weather_cache_dir_str: str = os.getenv("WEATHER_CACHE_DIR", "data/weather_cache/")
    WEATHER_CACHE_DIR: Path = BASE_DIR / _weather_cache_dir_str
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # API Settings
    OVERPASS_URL: str = os.getenv("OVERPASS_URL", "https://overpass-api.de/api/interpreter")
    NOMINATIM_USER_AGENT: str = os.getenv("NOMINATIM_USER_AGENT", "AgroMind_Prototype_v1")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # ML Models Paths
    DISEASE_MODEL_PATH: Path = BASE_DIR / "models" / "disease" / "model.pth"
    CROP_ADVISOR_MODEL_PATH: Path = BASE_DIR / "models" / "crop_advisor" / "model.pkl"
    YIELD_PREDICTOR_MODEL_PATH: Path = BASE_DIR / "models" / "yield_predictor" / "model.pkl"

settings = Settings()
