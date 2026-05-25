import requests
from typing import Dict, Any, Optional
from core.weather.cache import WeatherCache
from utils.logger import get_logger

logger = get_logger("WeatherClient")

class WeatherClient:
    URL = "https://api.open-meteo.com/v1/forecast"
    
    @staticmethod
    def get_7_day_forecast(lat: float, lon: float) -> Optional[Dict[str, Any]]:
        # 1. Check Cache
        cached_data = WeatherCache.get(lat, lon)
        if cached_data:
            logger.debug("Returning weather data from local JSON cache.")
            return cached_data
            
        # 2. Fetch from Open-Meteo
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "relative_humidity_2m", "precipitation"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"],
            "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation"],
            "timezone": "auto"
        }
        
        try:
            logger.info("Fetching fresh forecast from Open-Meteo.")
            response = requests.get(WeatherClient.URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # 3. Store in Cache
            WeatherCache.set(lat, lon, data)
            return data
            
        except requests.RequestException as e:
            logger.error(f"Weather fetch failed: {e}")
            return None
