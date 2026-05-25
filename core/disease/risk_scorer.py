from typing import Dict, Any, List
from utils.logger import get_logger

logger = get_logger("RiskScorer")

class RiskScorer:
    @staticmethod
    def calculate_integrated_risk(disease_confidence: float, disease_severity: str, environment_anomalies: int) -> Dict[str, Any]:
        """
        Synthesizes ML visual confidence with environmental stressors to produce 
        a composite 1-100 risk score for the crop.
        """
        base_score = 10.0
        
        # Factor 1: Image severity
        severity_multiplier = {
            "LOW": 1.0,
            "MEDIUM": 2.5,
            "HIGH": 4.0,
            "CRITICAL": 5.0
        }.get(disease_severity.upper(), 1.0)
        
        # 0.0-1.0 confidence scaled
        disease_impact = (disease_confidence * 100.0) * (severity_multiplier / 5.0)
        
        # Factor 2: Environment
        # Each active anomaly adds up to 15% risk
        environment_impact = min(environment_anomalies * 15.0, 40.0)
        
        total_risk = min(base_score + disease_impact + environment_impact, 100.0)
        
        action_level = "Monitoring"
        if total_risk > 75.0:
            action_level = "Immediate Intervention Required"
        elif total_risk > 40.0:
            action_level = "Treatment Recommended"
            
        logger.debug(f"Calculated composite risk: {total_risk:.1f}/100")
        
        return {
            "composite_score_100": round(total_risk, 1),
            "action_level": action_level,
            "contributing_factors": {
                "disease_impact_weight": round(disease_impact, 1),
                "environmental_stress_weight": round(environment_impact, 1)
            }
        }
