import time
import requests
from typing import Optional, Tuple, Dict, Any
from config.settings import settings
from utils.logger import get_logger

logger = get_logger("Geocoder")

class Geocoder:
    BASE_URL = "https://nominatim.openstreetmap.org/search"
    
    @staticmethod
    def get_coordinates(query: str) -> Optional[Tuple[float, float]]:
        """
        Geocodes a search query string into (lat, lon).
        Respects Nominatim's 1-second usage policy.
        """
        headers = {
            "User-Agent": settings.NOMINATIM_USER_AGENT
        }
        params = {
            "q": query,
            "format": "json",
            "limit": 1
        }
        
        try:
            logger.debug(f"Geocoding query: {query}")
            # Nominatim explicitly requests a 1 second delay between requests
            time.sleep(1.0)
            
            response = requests.get(Geocoder.BASE_URL, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return lat, lon
                
            logger.warning(f"No coordinates found for query: {query}")
            return None
            
        except requests.RequestException as e:
            logger.error(f"Geocoding error: {str(e)}")
            return None

    @staticmethod
    def detect_ip_location() -> Optional[Dict[str, Any]]:
        """
        Automatically detects the user's location based on their IP address
        using a fast, free, no-key IP geolocation service.
        """
        try:
            logger.debug("Detecting IP location...")
            response = requests.get("http://ip-api.com/json/", timeout=5)
            response.raise_for_status()
            data = response.json()
            if data.get("status") == "success":
                return {
                    "lat": float(data.get("lat")),
                    "lon": float(data.get("lon")),
                    "city": data.get("city"),
                    "region": data.get("regionName"),
                    "country": data.get("country")
                }
            logger.warning("IP location detection returned non-success status.")
            return None
        except Exception as e:
            logger.error(f"IP Location detection failed: {e}")
            return None
