import json
from typing import List, Dict, Any
from config.settings import settings
from utils.logger import get_logger

logger = get_logger("CropAdvisor")

class CropAdvisor:
    def __init__(self):
        self.kb_path = settings.BASE_DIR / 'knowledge' / 'crops.json'
        self.crops_kb = []
        self._load_kb()
        
    def _load_kb(self):
        if self.kb_path.exists():
            with open(self.kb_path, 'r') as f:
                self.crops_kb = json.load(f)
        else:
            logger.error(f"Crops Knowledge base missing at {self.kb_path}")
            
    def get_recommendations(self, soil_type: str, temp: float, rainfall: float) -> List[Dict[str, Any]]:
        """
        Combines deterministic boundaries and mock ML ranking to recommend crops.
        """
        matches = []
        for crop in self.crops_kb:
            if soil_type in crop.get('soil_requirements', []):
                # Basic viability checks
                if crop.get('min_temperature', -50) <= temp <= crop.get('max_temperature', 100):
                    # Mock ML confidence score logic (we assume this replaces true scikit-learn for now)
                    confidence = 0.85
                    
                    matches.append({
                        "crop_name": crop['name'],
                        "confidence_score": confidence,
                        "season": crop['season'],
                        "expected_yield": crop['expected_yield_tons_ha'],
                        "tags": crop['tags']
                    })
                    
        # Sort by confidence descending
        matches.sort(key=lambda x: x['confidence_score'], reverse=True)
        return matches
