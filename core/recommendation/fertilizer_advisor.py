import json
from typing import List, Dict, Any, Tuple
from config.settings import settings
from utils.logger import get_logger

logger = get_logger("FertilizerAdvisor")

class FertilizerAdvisor:
    def __init__(self):
        # Dictionary of standard crop N-P-K nutrient requirements in kg/hectare (N, P, K)
        self.crop_npk_standards = {
            "wheat": (120, 60, 40),
            "rice": (120, 60, 40),
            "maize": (150, 60, 40),
            "potato": (150, 120, 150),
            "tomato": (120, 100, 100),
            "cotton": (100, 50, 50),
            "sugarcane": (250, 75, 100),
            "soybean": (30, 60, 80),
        }
        
    def get_recommendations(
        self, 
        crop_name: str, 
        disease_severity: str = "LOW", 
        mode: str = "Standard",
        soil_n: str = "Medium", 
        soil_p: str = "Medium", 
        soil_k: str = "Medium"
    ) -> Dict[str, Any]:
        """
        Calculates scientific fertilizer recommendations adjusted for:
        1. Crop-specific baseline N-P-K requirements
        2. Soil test nutrient levels (Low, Medium, High)
        3. Disease status (reducing N, boosting K)
        4. Farming mode (Standard, Organic, High Yield, Urgent Fix)
        
        Returns a rich prescription dictionary.
        """
        crop_key = crop_name.lower().strip()
        
        # Get base NPK or default to standard balanced crop requirement
        if crop_key in self.crop_npk_standards:
            base_n, base_p, base_k = self.crop_npk_standards[crop_key]
            is_custom_crop = False
        else:
            base_n, base_p, base_k = (100, 60, 60)
            is_custom_crop = True
            
        adjustments_made = []
        
        # 1. Soil nutrient level adjustments (STCR principles)
        # Low soil level means we need to supply MORE nutrients to build up soil pool.
        # High soil level means soil is already rich, we can reduce application to save cost.
        soil_multipliers = {"Low": 1.3, "Medium": 1.0, "High": 0.7}
        
        adj_n = base_n * soil_multipliers.get(soil_n, 1.0)
        adj_p = base_p * soil_multipliers.get(soil_p, 1.0)
        adj_k = base_k * soil_multipliers.get(soil_k, 1.0)
        
        if soil_n != "Medium":
            adjustments_made.append(f"Adjusted Nitrogen target by {int((soil_multipliers.get(soil_n) - 1)*100):+d}% due to {soil_n} soil Nitrogen level.")
        if soil_p != "Medium":
            adjustments_made.append(f"Adjusted Phosphorus target by {int((soil_multipliers.get(soil_p) - 1)*100):+d}% due to {soil_p} soil Phosphorus level.")
        if soil_k != "Medium":
            adjustments_made.append(f"Adjusted Potassium target by {int((soil_multipliers.get(soil_k) - 1)*100):+d}% due to {soil_k} soil Potassium level.")

        # 2. Disease Severity Adjustments
        # Pathogens thrive on soft plant tissues stimulated by high Nitrogen.
        # Potassium enhances structural cell wall strength and plant defense mechanisms.
        disease_sev = disease_severity.upper().strip()
        if disease_sev == "MEDIUM":
            adj_n *= 0.90
            adj_k *= 1.10
            adjustments_made.append("Reduced Nitrogen target by 10% and increased Potassium by 10% due to moderate disease presence to boost structural defense.")
        elif disease_sev == "HIGH":
            adj_n *= 0.70
            adj_k *= 1.20
            adjustments_made.append("⚠️ Reduced Nitrogen target by 30% to suppress pathogen reproduction and boosted Potassium by 20% to build disease resistance.")
        elif disease_sev == "CRITICAL":
            adj_n *= 0.50
            adj_k *= 1.30
            adjustments_made.append("🚨 CRITICAL ALERT: Suspended Nitrogen top-dressing by 50% to prevent soft vegetative tissue spread; increased Potassium by 30% to assist cell repair.")

        # 3. Farming Mode Adjustments
        if mode == "High Yield":
            adj_n *= 1.20
            adj_p *= 1.20
            adj_k *= 1.20
            adjustments_made.append("Boosted all nutrient targets by 20% to support high-density crop yield projections.")
        elif mode == "Organic":
            # Organic farming focuses on slow-release organic carbon pools
            adjustments_made.append("Converted fertilizer prescriptions entirely to slow-release organic and microbial amendments.")
        elif mode == "Urgent Fix":
            adjustments_made.append("Prioritized highly water-soluble, fast-absorption formulations for rapid crop recovery.")

        # Round nutrient targets
        adj_n = round(adj_n, 1)
        adj_p = round(adj_p, 1)
        adj_k = round(adj_k, 1)

        recommendations = []
        splits = {}

        # 4. Calculate actual fertilizer applications
        if mode != "Organic":
            # Chemical Mode: Using DAP (18-46-0), Urea (46-0-0), and MOP (0-0-60)
            
            # Satisfy Phosphorus requirement first using DAP
            dap_kg = round(adj_p / 0.46, 1)
            # DAP also contributes nitrogen: 18% of DAP weight
            n_from_dap = round(dap_kg * 0.18, 1)
            
            # Satisfy remaining Nitrogen using Urea
            remaining_n = max(0.0, adj_n - n_from_dap)
            urea_kg = round(remaining_n / 0.46, 1)
            
            # Satisfy Potassium using MOP (Muriate of Potash, 60% K2O)
            mop_kg = round(adj_k / 0.60, 1)
            
            if dap_kg > 0:
                recommendations.append({
                    "name": "DAP (Diammonium Phosphate)",
                    "type": "Chemical",
                    "n_p_k": "18-46-0",
                    "dosage_kg_ha": dap_kg,
                    "dosage_kg_acre": round(dap_kg * 0.4047, 1),
                    "cautions": "Apply as basal dressing. Ensure thorough soil mixing at sowing to avoid direct root contact.",
                    "method": "Basal Broadcasting or Placement"
                })
            
            if urea_kg > 0:
                recommendations.append({
                    "name": "Urea",
                    "type": "Chemical",
                    "n_p_k": "46-0-0",
                    "dosage_kg_ha": urea_kg,
                    "dosage_kg_acre": round(urea_kg * 0.4047, 1),
                    "cautions": "Do not apply on wet leaves. Best applied in split doses to minimize leaching and ammonia volatilization.",
                    "method": "Top Dressing"
                })
                
            if mop_kg > 0:
                recommendations.append({
                    "name": "MOP (Muriate of Potash)",
                    "type": "Chemical",
                    "n_p_k": "0-0-60",
                    "dosage_kg_ha": mop_kg,
                    "dosage_kg_acre": round(mop_kg * 0.4047, 1),
                    "cautions": "Apply in splits if soil is sandy. Helps regulate plant water balance and builds disease tolerance.",
                    "method": "Basal + Vegetative Top Dressing"
                })
                
            # Micronutrient recommendation
            if disease_sev in ["HIGH", "CRITICAL"]:
                recommendations.append({
                    "name": "Zinc Sulfate & Borax Blend",
                    "type": "Chemical",
                    "n_p_k": "Micronutrients",
                    "dosage_kg_ha": 25.0,
                    "dosage_kg_acre": 10.1,
                    "cautions": "Foliar spray is highly recommended if symptoms persist. Helps trigger defense enzymes.",
                    "method": "Foliar Spray or Soil Application"
                })
                
            # Set split schedule for Chemical
            if mode == "Urgent Fix":
                splits = {
                    "Basal (At Sowing/Planting)": "30% DAP + 20% MOP",
                    "Early Vegetative (Foliar Spray)": "30% Urea (dissolved in water) + 30% MOP",
                    "Flowering Stage (Top Dressing)": "50% Urea + 50% MOP + Zinc Sulfate"
                }
            elif mode == "High Yield":
                splits = {
                    "Basal (At Planting)": "100% DAP + 30% Urea + 50% MOP",
                    "Active Tillering / Branching": "35% Urea + 25% MOP",
                    "Panicle Initiation / Pre-flowering": "35% Urea + 25% MOP"
                }
            else: # Standard
                splits = {
                    "Basal (At Planting)": "100% DAP + 50% MOP",
                    "Vegetative Growth (Top Dressing)": "50% Urea + 50% MOP",
                    "Flowering / Heading Stage": "50% Urea"
                }

        else:
            # Organic Mode: Using Compost/Manure, Neem Cake, Bone Meal, Wood Ash
            # Base organic compost
            compost_tonnes_ha = 6.0
            if mode == "High Yield":
                compost_tonnes_ha = 8.0
                
            recommendations.append({
                "name": "Well-Rotted Compost / Vermicompost",
                "type": "Organic",
                "n_p_k": "1.5-1.0-1.5",
                "dosage_kg_ha": compost_tonnes_ha * 1000,
                "dosage_kg_acre": round(compost_tonnes_ha * 1000 * 0.4047, 1),
                "cautions": "Apply 3 weeks before sowing. Enhances organic carbon, moisture retention, and soil microflora.",
                "method": "Soil Incorporation"
            })
            
            # Satisfy Nitrogen booster using Neem Cake (acts as pesticide too!)
            neem_cake_kg = round(max(200.0, adj_n * 3.5), 1)
            recommendations.append({
                "name": "Neem Cake Powder",
                "type": "Organic",
                "n_p_k": "5.0-1.0-1.5",
                "dosage_kg_ha": neem_cake_kg,
                "dosage_kg_acre": round(neem_cake_kg * 0.4047, 1),
                "cautions": "Double benefit: acts as a rich slow-release nitrogen source and controls soil-borne nematodes/fungi.",
                "method": "Basal Soil Incorporation"
            })
            
            # Satisfy Phosphorus booster using Bone Meal
            bone_meal_kg = round(max(150.0, adj_p * 4.0), 1)
            recommendations.append({
                "name": "Bone Meal",
                "type": "Organic",
                "n_p_k": "3.0-20.0-0.0",
                "dosage_kg_ha": bone_meal_kg,
                "dosage_kg_acre": round(bone_meal_kg * 0.4047, 1),
                "cautions": "Slow-release phosphorus. Promotes excellent root establishment. Best applied in basal dressing.",
                "method": "Basal dressing or Row application"
            })
            
            # Satisfy Potassium booster using Wood Ash
            wood_ash_kg = round(max(100.0, adj_k * 8.0), 1)
            recommendations.append({
                "name": "Wood Ash / Potash-Rich Biochar",
                "type": "Organic",
                "n_p_k": "0.0-1.5-7.0",
                "dosage_kg_ha": wood_ash_kg,
                "dosage_kg_acre": round(wood_ash_kg * 0.4047, 1),
                "cautions": "Apply around root zones. Corrects potassium deficiency and adjusts acidic soil pH.",
                "method": "Top dressing or Ring application"
            })
            
            if disease_sev in ["HIGH", "CRITICAL"]:
                recommendations.append({
                    "name": "Liquid Seaweed Extract / Bio-stimulant",
                    "type": "Organic",
                    "n_p_k": "Trace Minerals",
                    "dosage_kg_ha": 5.0, # liters/ha
                    "dosage_kg_acre": 2.0,
                    "cautions": "Foliar application activates systemically acquired resistance (SAR) in plants to combat diseases.",
                    "method": "Foliar Spray"
                })
                
            splits = {
                "Pre-planting (3 Weeks Prior)": "100% Compost incorporated into the topsoil",
                "At Sowing / Transplanting": "100% Bone Meal + 100% Neem Cake",
                "Vegetative Development Stage": "100% Wood Ash top-dressed around roots"
            }

        return {
            "crop_name": crop_name,
            "is_custom_crop": is_custom_crop,
            "base_npk": {"N": base_n, "P": base_p, "K": base_k},
            "adjusted_npk": {"N": adj_n, "P": adj_p, "K": adj_k},
            "adjustments": adjustments_made,
            "recommendations": recommendations,
            "splits": splits,
            "mode": mode,
            "disease_severity": disease_severity
        }
