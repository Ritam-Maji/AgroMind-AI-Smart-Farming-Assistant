from typing import List, Dict, Any, Optional
from utils.logger import get_logger

logger = get_logger("ActionPlanner")

class ActionPlanner:
    @staticmethod
    def generate_daily_plan(weather_data: Optional[Dict[str, Any]], recent_anomalies: int) -> List[Dict[str, str]]:
        """
        Translates environmental constraints and weather forecasts into concrete, physical farming tasks.
        """
        tasks = []
        
        # 1. Base default task
        tasks.append({
            "time": "06:00 AM",
            "task": "Visual Crop Inspection",
            "reason": "Standard daily operating procedure to catch disease early."
        })
        
        # 2. Weather dependent logic
        precip_today = 0.0
        temp_max_today = 25.0
        
        if weather_data and "daily" in weather_data:
            precip_today = weather_data["daily"].get("precipitation_sum", [0.0])[0]
            temp_max_today = weather_data["daily"].get("temperature_2m_max", [25.0])[0]
            
        if precip_today < 2.0:
            tasks.append({
                "time": "07:30 AM",
                "task": "Drip Irrigation Cycle",
                "reason": f"Expected natural rainfall today is only {precip_today}mm. Soils require manual hydration."
            })
        else:
            tasks.append({
                "time": "07:30 AM",
                "task": "Skip Morning Irrigation",
                "reason": f"Sufficient natural rainfall expected today: {precip_today}mm."
            })
            
        if temp_max_today > 36.0:
            tasks.append({
                "time": "01:00 PM",
                "task": "Activate Heat Protection",
                "reason": f"Extreme heat forecasted ({temp_max_today}°C). Deploy shade nets if applicable or run misting sprinklers."
            })
            
        # 3. Anomaly response
        if recent_anomalies > 0:
            tasks.append({
                "time": "04:00 PM",
                "task": "Remedial Field Work",
                "reason": f"Target fields addressing {recent_anomalies} active severe environmental or disease stressors identified."
            })
            
        return tasks
