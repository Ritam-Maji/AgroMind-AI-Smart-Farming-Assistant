from typing import Dict, Any, List
from utils.logger import get_logger

logger = get_logger("EnvironmentAnalyzer")

class EnvironmentAnalyzer:
    @staticmethod
    def analyze_conditions(temp_c: float, humidity_percent: float, soil_ph: float, rainfall_mm: float) -> Dict[str, Any]:
        """
        Evaluates current physical state of the environment and returns severe anomalies
        or plain-language intelligence regarding farming viability.
        """
        anomalies: List[str] = []
        is_favorable = True
        
        # Extremely hot temperature
        if temp_c > 38.0:
            anomalies.append(f"Critical Heat Warning: {temp_c}°C. Severe heat stress possible on most crops.")
            is_favorable = False
        elif temp_c < 5.0:
            anomalies.append(f"Frost Warning: {temp_c}°C. High risk of frost damage to non-winter crops.")
            is_favorable = False
            
        # Humidity
        if humidity_percent > 85.0:
            anomalies.append(f"High Humidity Notification: {humidity_percent}%. High risk for fungal disease proliferation.")
        elif humidity_percent < 20.0:
            anomalies.append(f"Very Low Humidity Notification: {humidity_percent}%. Increased evaporation rates, consider extra irrigation.")
            
        # Soil pH
        if soil_ph < 5.5:
            anomalies.append(f"Highly Acidic Soil Notification: pH {soil_ph}. Most crops will require agricultural lime to optimize nutrient availability.")
            is_favorable = False
        elif soil_ph > 8.0:
            anomalies.append(f"Alkaline Soil Notification: pH {soil_ph}. Risk of iron/zinc deficiency. Use acidifying fertilizers.")
            is_favorable = False
            
        return {
            "overall_status": "FAVORABLE" if is_favorable else "AT RISK",
            "anomalies_detected": anomalies,
            "anomalies_count": len(anomalies)
        }
