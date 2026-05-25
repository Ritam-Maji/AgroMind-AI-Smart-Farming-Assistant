from typing import Dict, Any, List
from utils.logger import get_logger

logger = get_logger("WeatherAdvisor")

class WeatherAdvisor:
    @staticmethod
    def generate_advisories(forecast_data: Dict[str, Any]) -> List[str]:
        advisories = []
        
        if not forecast_data:
            return ["No forecast data available to generate advisories."]
            
        daily = forecast_data.get("daily", {})
        if not daily:
            return ["Missing daily metrics in Weather payload."]
            
        precipitation = daily.get("precipitation_sum", [])
        temps_max = daily.get("temperature_2m_max", [])
        
        # Look at the next 3 days
        lookahead = min(3, len(precipitation))
        for i in range(lookahead):
            day_label = "Tomorrow" if i == 1 else ("Today" if i == 0 else f"In {i} days")
            precip = precipitation[i]
            t_max = temps_max[i]
            
            if precip and precip > 15.0:
                advisories.append(f"Heavy Rain Expected {day_label}: {precip}mm. Delay fertilizer spraying and monitor field drainage.")
            elif precip and precip > 5.0:
                advisories.append(f"Moderate Rain Expected {day_label}: {precip}mm. Good natural irrigation, but avoid pesticide application.")
                
            if t_max and t_max > 38.0:
                advisories.append(f"Heat Alert {day_label}: High of {t_max}°C. Ensure crop hydration early in the morning.")
                
        if not advisories:
            advisories.append("Standard Weather Conditions: No immediate disruptive weather events detected in the near term.")
            
        return advisories
