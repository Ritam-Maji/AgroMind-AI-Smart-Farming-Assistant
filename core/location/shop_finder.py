import requests
from typing import List, Dict, Any
from config.settings import settings
from utils.logger import get_logger

logger = get_logger("ShopFinder")

class ShopFinder:
    @staticmethod
    def find_nearby_shops(lat: float, lon: float, radius_meters: int = 50000) -> List[Dict[str, Any]]:
        """
        Queries Overpass API to find agricultural, fertilizer, or farming shops within radius.
        """
        overpass_url = settings.OVERPASS_URL
        
        # Searching for 'shop=agrochemical' or generic farming shops
        overpass_query = f"""
        [out:json];
        (
          node["shop"="agribusiness"](around:{radius_meters},{lat},{lon});
          node["shop"="agrochemical"](around:{radius_meters},{lat},{lon});
          node["shop"="farm"](around:{radius_meters},{lat},{lon});
          node["shop"="fertilizer"](around:{radius_meters},{lat},{lon});
          node["shop"="agrarian"](around:{radius_meters},{lat},{lon});
        );
        out body;
        """
        
        logger.debug(f"Querying Overpass API for shops at {lat}, {lon}")
        
        try:
            headers = {'User-Agent': settings.NOMINATIM_USER_AGENT}
            response = requests.post(overpass_url, data={'data': overpass_query}, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            shops = []
            for element in data.get('elements', []):
                tags = element.get('tags', {})
                shop_name = tags.get('name', 'Unnamed Shop')
                shops.append({
                    "id": element.get('id'),
                    "name": shop_name,
                    "lat": element.get('lat'),
                    "lon": element.get('lon'),
                    "type": tags.get('shop', 'Unknown')
                })
                
            return shops
        except requests.RequestException as e:
            logger.error(f"Failed to fetch nearby shops: {str(e)}")
            return []
