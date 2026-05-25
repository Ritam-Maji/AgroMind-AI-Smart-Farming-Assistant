import json
from pathlib import Path
from typing import Dict, Any, Optional
from config.settings import settings
from utils.logger import get_logger

logger = get_logger("YieldPredictor")

class YieldPredictor:
    def __init__(self):
        self.model_path = settings.YIELD_PREDICTOR_MODEL_PATH
        self.kb_path = settings.BASE_DIR / 'knowledge' / 'crops.json'
        self.crops_kb = {}
        self._load_kb()
        
    def _load_kb(self):
        if self.kb_path.exists():
            with open(self.kb_path, 'r') as f:
                data = json.load(f)
                self.crops_kb = {c['name'].lower(): c for c in data}
        else:
            logger.error("Crops KB missing for Yield Prediction deterministic fallback.")
            
    def predict_yield(self, crop_name: str, area_hectares: float, environmental_score: float = 1.0) -> Dict[str, Any]:
        """
        Calculates or predicts estimated harvest yields.
        Returns expected deterministic metrics if scikit-learn models are missing.
        """
        crop_name = crop_name.lower().strip()
        
        if crop_name not in self.crops_kb:
            logger.warning(f"Unknown crop {crop_name}. Cannot formulate fallback estimation.")
            return {
                "estimated_tons": 0.0,
                "risk_factor_percent": 100.0,
                "is_mocked": True
            }
            
        base_yield_ha = self.crops_kb[crop_name].get('expected_yield_tons_ha', 5.0)
        
        # Environmental score is a 0.0 - 1.0 health multiplier
        total_estimated = base_yield_ha * area_hectares * environmental_score
        
        # Calculate risk based on how much the environmental score deviates from perfect 1.0
        risk_percentage = (1.0 - environmental_score) * 100.0
        
        # Floor boundaries for realism
        risk_percentage = min(max(risk_percentage, 5.0), 95.0)
        
        logger.info(f"Calculated Mock Yield for {area_hectares}ha of {crop_name}: {total_estimated:.2f} tons")
        
        return {
            "estimated_tons": float(round(total_estimated, 1)),
            "risk_factor_percent": float(round(risk_percentage, 1)),
            "is_mocked": True
        }
