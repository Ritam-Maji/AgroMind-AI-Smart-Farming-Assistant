import json
import time
from pathlib import Path
from typing import Optional, Dict, Any
from config.settings import settings
from utils.logger import get_logger

logger = get_logger("WeatherCache")

class WeatherCache:
    TTL_SECONDS = 1800  # 30 minutes
    
    @staticmethod
    def _get_cache_file(lat: float, lon: float) -> Path:
        settings.WEATHER_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        # Simple rounding to 2 decimal places to avoid duplicate caches for extremely close locations
        filename = f"{lat:.2f}_{lon:.2f}.json"
        return settings.WEATHER_CACHE_DIR / filename
        
    @staticmethod
    def get(lat: float, lon: float) -> Optional[Dict[str, Any]]:
        cache_file = WeatherCache._get_cache_file(lat, lon)
        if cache_file.exists():
            mod_time = cache_file.stat().st_mtime
            if time.time() - mod_time < WeatherCache.TTL_SECONDS:
                try:
                    with open(cache_file, "r") as f:
                        return json.load(f)
                except Exception as e:
                    logger.warning(f"Failed to read cache file {cache_file}: {e}")
            else:
                logger.debug(f"Cache expired for {lat}, {lon}")
        return None
        
    @staticmethod
    def set(lat: float, lon: float, data: Dict[str, Any]) -> None:
        cache_file = WeatherCache._get_cache_file(lat, lon)
        try:
            with open(cache_file, "w") as f:
                json.dump(data, f)
            logger.debug(f"Weather successfully cached for {lat}, {lon}")
        except Exception as e:
            logger.error(f"Failed to write weather cache: {e}")
