import os
import logging
from typing import Dict, Any, List, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

# Regional Soil and Agro-Climatic Data Reference (ICAR / National Bureau of Soil Survey & Land Use Planning)
REGIONAL_SOIL_DATABASE: Dict[str, Dict[str, str]] = {
    "punjab": {"predominant_soil": "Alluvial Soil (Inceptisols/Entisols)", "characteristics": "Deep, fertile, well-drained loamy to sandy loam with neutral to slightly alkaline pH."},
    "haryana": {"predominant_soil": "Alluvial & Sandy Loam", "characteristics": "Permeable, rich in potash, moderate organic matter."},
    "maharashtra": {"predominant_soil": "Black Soil (Vertisols/Regur)", "characteristics": "High clay content, moisture-retentive, rich in calcium carbonate, magnesium, and potash."},
    "madhya pradesh": {"predominant_soil": "Medium & Deep Black Soil", "characteristics": "Clayey, crack-forming during dry spells, excellent moisture retention."},
    "uttar pradesh": {"predominant_soil": "Gangetic Alluvial Soil", "characteristics": "Loamy to silt loam, very fertile, suitable for multi-cropping."},
    "gujarat": {"predominant_soil": "Black Soil & Coastal Alluvial", "characteristics": "Calcareous, clayey in central zones, sandy loam in northern plains."},
    "rajasthan": {"predominant_soil": "Arid Desert & Sandy Soil (Aridisols)", "characteristics": "Low moisture holding capacity, low nitrogen, high permeability."},
    "karnataka": {"predominant_soil": "Red Loam & Black Soil (Deccan)", "characteristics": "Rich in iron and manganese, porous, responds well to irrigation and fertilizers."},
    "andhra pradesh": {"predominant_soil": "Red Sandy Loam & Coastal Alluvial", "characteristics": "Well-drained red soil in uplands, rich fertile deltaic alluvium along rivers."},
    "telangana": {"predominant_soil": "Red Earths (Chalka) & Black Cotton", "characteristics": "Chalka soils are gravelly and light; black soils are heavy clay with high swelling."},
    "tamil nadu": {"predominant_soil": "Red Loam & Coastal Alluvial", "characteristics": "Acidic to neutral pH, moderate water retention, requires micronutrient support."},
    "west bengal": {"predominant_soil": "Alluvial & Deltaic Clay Loam", "characteristics": "High water-retention capacity, organic rich, ideal for wet-field paddy and jute."},
    "bihar": {"predominant_soil": "North & South Alluvial Plains", "characteristics": "Fine texture, high moisture retention, high natural fertility."},
    "kerala": {"predominant_soil": "Laterite Soil (Ultisols/Oxisols)", "characteristics": "Porous, rich in organic matter and iron oxides, low phosphorus fixing capacity."}
}

# Crop Agro-Ecological Profiles
CROP_AGRO_DATABASE = [
    {
        "crop_name": "Wheat (Triticum aestivum)",
        "suitable_seasons": ["Rabi (Winter)"],
        "temp_min": 10.0,
        "temp_max": 25.0,
        "water_requirement": "Moderate (4-6 irrigations at critical CRI stages)",
        "preferred_soils": ["alluvial", "loam", "clay loam"],
        "min_water_sources": ["Borewell", "Canal irrigation", "Other irrigation source"],
        "guidance": "Sow between Nov 1 - Nov 20 for optimal tillering. Ensure Crown Root Initiation (CRI) irrigation at 21 days."
    },
    {
        "crop_name": "Paddy / Rice (Oryza sativa)",
        "suitable_seasons": ["Kharif (Monsoon)", "Zaid (Summer)"],
        "temp_min": 20.0,
        "temp_max": 38.0,
        "water_requirement": "High (continuous standing water 2-5 cm during vegetative phase)",
        "preferred_soils": ["alluvial", "clay loam", "black"],
        "min_water_sources": ["Canal irrigation", "Borewell", "Rain-fed"],
        "guidance": "Transplant 21-25 day seedlings. Maintain water levels and incorporate balanced nitrogen in 3 split doses."
    },
    {
        "crop_name": "Cotton (Gossypium hirsutum)",
        "suitable_seasons": ["Kharif (Monsoon)"],
        "temp_min": 21.0,
        "temp_max": 35.0,
        "water_requirement": "Moderate (requires well-drained soil; sensitive to waterlogging)",
        "preferred_soils": ["black", "vertisol", "alluvial"],
        "min_water_sources": ["Borewell", "Canal irrigation", "Rain-fed", "Other irrigation source"],
        "guidance": "Deep black soils offer ideal moisture buffering. Avoid standing water during boll formation."
    },
    {
        "crop_name": "Soybean (Glycine max)",
        "suitable_seasons": ["Kharif (Monsoon)"],
        "temp_min": 18.0,
        "temp_max": 32.0,
        "water_requirement": "Moderate (rainfall dependent or 2-3 protective irrigations)",
        "preferred_soils": ["black", "loam", "alluvial"],
        "min_water_sources": ["Rain-fed", "Borewell", "Canal irrigation", "Other irrigation source"],
        "guidance": "Inoculate seeds with Bradyrhizobium japonicum culture before sowing. Ensure good drainage."
    },
    {
        "crop_name": "Mustard / Rapeseed (Brassica juncea)",
        "suitable_seasons": ["Rabi (Winter)"],
        "temp_min": 10.0,
        "temp_max": 25.0,
        "water_requirement": "Low to Moderate (1-2 irrigations sufficient; drought tolerant)",
        "preferred_soils": ["alluvial", "sandy loam", "loam"],
        "min_water_sources": ["Borewell", "Rain-fed", "Canal irrigation", "Other irrigation source", "Unknown"],
        "guidance": "Optimal sowing mid-October. Monitor for aphid pest during flowering in foggy conditions."
    },
    {
        "crop_name": "Pearl Millet / Bajra (Pennisetum glaucum)",
        "suitable_seasons": ["Kharif (Monsoon)", "Zaid (Summer)"],
        "temp_min": 25.0,
        "temp_max": 42.0,
        "water_requirement": "Low (highly drought resistant and resilient in arid belts)",
        "preferred_soils": ["sandy loam", "desert", "red", "alluvial"],
        "min_water_sources": ["Rain-fed", "Borewell", "Unknown", "Other irrigation source"],
        "guidance": "Thrives with minimal water inputs (250-400 mm). Excellent climate-resilient coarse grain."
    },
    {
        "crop_name": "Chickpea / Gram (Cicer arietinum)",
        "suitable_seasons": ["Rabi (Winter)"],
        "temp_min": 12.0,
        "temp_max": 28.0,
        "water_requirement": "Low (rainfed residual moisture or 1 flowering irrigation)",
        "preferred_soils": ["black", "alluvial", "loam"],
        "min_water_sources": ["Rain-fed", "Borewell", "Canal irrigation", "Other irrigation source", "Unknown"],
        "guidance": "Avoid excess nitrogen fertilizer. Sensitive to waterlogging; nip apical buds at 30-40 days to promote branching."
    },
    {
        "crop_name": "Maize (Zea mays)",
        "suitable_seasons": ["Kharif (Monsoon)", "Rabi (Winter)", "Zaid (Summer)"],
        "temp_min": 18.0,
        "temp_max": 35.0,
        "water_requirement": "Moderate (450-650 mm; sensitive to drought at tasseling)",
        "preferred_soils": ["alluvial", "red loam", "black"],
        "min_water_sources": ["Borewell", "Canal irrigation", "Rain-fed", "Other irrigation source"],
        "guidance": "Ensure adequate soil moisture during silking and cob development. Highly responsive to potash."
    }
]

class CropRecommendationService:
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self.model_type = "RandomForest / XGBoost Interface"
        self._check_and_load_model()

    def _check_and_load_model(self):
        """
        Check for trained Random Forest or XGBoost model.
        In accordance with guidelines:
        - Do not pretend that a trained model exists if it has not been trained.
        - Do not return fake predictions.
        """
        model_path = settings.CROP_MODEL_PATH
        if os.path.exists(model_path):
            try:
                import joblib
                self.model = joblib.load(model_path)
                self.model_loaded = True
                logger.info(f"Loaded trained crop recommendation model from {model_path}")
            except Exception as e:
                logger.warning(f"Failed to load crop model from {model_path}: {e}")
                self.model_loaded = False
        else:
            logger.info(
                f"No pre-trained crop model file found at '{model_path}'. "
                "Service will run in agronomic extension evaluation mode with clear model_configured=False status."
            )
            self.model_loaded = False

    def get_soil_reference(self, state: str, district: str) -> Dict[str, Any]:
        """Look up regional soil characteristics based on ICAR district/state reference."""
        state_key = state.strip().lower()
        if state_key in REGIONAL_SOIL_DATABASE:
            data = REGIONAL_SOIL_DATABASE[state_key]
            return {
                "soil_type": data["predominant_soil"],
                "source": "regional_database (ICAR Agro-Climatic Reference)",
                "characteristics": data["characteristics"]
            }
        return {
            "soil_type": None,
            "source": "unavailable",
            "characteristics": "District-specific soil map data is not yet configured for this region in the 40% milestone."
        }

    def determine_season(self, month: int) -> str:
        """Determine Indian agricultural season from current month."""
        if 6 <= month <= 10:
            return "Kharif (Monsoon)"
        elif 11 <= month or month <= 3:
            return "Rabi (Winter)"
        else:
            return "Zaid (Summer)"

    async def recommend_crops(
        self,
        state: str,
        district: str,
        village: Optional[str] = "",
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        soil_type: Optional[str] = None,
        water_source: str = "Unknown",
        season: Optional[str] = None,
        weather_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Produce environmental and location based crop recommendations.
        Does NOT rely on manual NPK values!
        Uses location, detected/farmer soil, water availability, and agro-climatic conditions.
        """
        import datetime
        current_month = datetime.datetime.now().month
        effective_season = season or self.determine_season(current_month)

        # Step 1: Resolve soil information with transparency
        if soil_type and soil_type.strip() and soil_type.lower() != "unknown":
            effective_soil = {
                "soil_type": soil_type.strip(),
                "source": "farmer_provided",
                "characteristics": f"Observed by farmer as {soil_type}."
            }
        else:
            effective_soil = self.get_soil_reference(state, district)

        # Step 2: Resolve weather information
        if weather_info and "temperature_celsius" in weather_info:
            weather_data = {
                "temperature": weather_info.get("temperature_celsius"),
                "humidity": weather_info.get("humidity_percent"),
                "rainfall_estimate": weather_info.get("rainfall_mm"),
                "season_detected": effective_season,
                "source": "openweather_live" if weather_info.get("is_live_data") else "seasonal_regional_normals"
            }
        else:
            # Fallback normal seasonal temperature estimation for Indian sub-continent
            avg_temp = 22.0 if "Rabi" in effective_season else (30.0 if "Kharif" in effective_season else 34.0)
            weather_data = {
                "temperature": avg_temp,
                "humidity": 65 if "Kharif" in effective_season else 45,
                "rainfall_estimate": 120.0 if "Kharif" in effective_season else 15.0,
                "season_detected": effective_season,
                "source": "seasonal_regional_normals"
            }

        # Step 3: Check if ML model is loaded (RandomForest / XGBoost)
        if self.model_loaded and self.model is not None:
            # In Phase 2, pipeline will transform (lat, lon, soil_encoded, water_encoded, temp, humidity, rainfall)
            # and call model.predict_proba()
            pass

        # Step 4: Agronomic heuristic rule matching for the first 40% milestone
        # Clear, truthful scoring based on agro-climatic constraints
        recommendations = []
        user_soil_str = (effective_soil.get("soil_type") or "").lower()
        temp = weather_data["temperature"] or 26.0

        for crop in CROP_AGRO_DATABASE:
            score = 70.0  # Base suitability
            reasons = []

            # 1. Season match
            season_match = any(effective_season.split()[0] in s for s in crop["suitable_seasons"])
            if season_match:
                score += 15.0
                reasons.append(f"Ideal fit for {effective_season}")
            else:
                score -= 30.0
                reasons.append(f"Sub-optimal season (best in {', '.join(crop['suitable_seasons'])})")

            # 2. Water source compatibility
            if water_source in crop["min_water_sources"]:
                score += 10.0
                reasons.append(f"Irrigation source '{water_source}' is suitable for crop water needs")
            elif water_source == "Rain-fed" and "Rain-fed" not in crop["min_water_sources"]:
                score -= 25.0
                reasons.append("Crop requires assured irrigation; rain-fed cultivation poses high risk")

            # 3. Soil compatibility
            if user_soil_str:
                matched_soil = any(ps in user_soil_str for ps in crop["preferred_soils"])
                if matched_soil:
                    score += 10.0
                    reasons.append(f"Well-adapted to regional {effective_soil.get('soil_type')}")

            # 4. Temperature range
            if crop["temp_min"] <= temp <= crop["temp_max"]:
                score += 5.0
            else:
                score -= 15.0
                reasons.append(f"Current temp {temp}°C is outside preferred band ({crop['temp_min']}-{crop['temp_max']}°C)")

            final_score = max(20.0, min(98.0, round(score, 1)))
            
            # Keep top candidates
            recommendations.append({
                "crop_name": crop["crop_name"],
                "suitability_score": final_score,
                "reason": ". ".join(reasons) + ".",
                "suitable_season": ", ".join(crop["suitable_seasons"]),
                "water_requirement": crop["water_requirement"],
                "basic_guidance": crop["guidance"]
            })

        # Sort descending by suitability score
        recommendations.sort(key=lambda x: x["suitability_score"], reverse=True)
        top_recommendations = recommendations[:5]

        return {
            "success": True,
            "location": {
                "state": state,
                "district": district,
                "village": village,
                "latitude": latitude,
                "longitude": longitude,
                "source": "gps_browser" if latitude and longitude else "farmer_selection"
            },
            "soil_info": effective_soil,
            "weather_info": weather_data,
            "water_source": water_source,
            "model_configured": self.model_loaded,
            "model_type": "Scikit-Learn Random Forest Pipeline (Pending trained weights; Agronomic Rule Baseline Active)",
            "recommendations": top_recommendations,
            "message": (
                "Location and environmental criteria evaluated without requiring manual NPK inputs. "
                "Trained Random Forest/XGBoost weights will be integrated in milestone phase 2."
            )
        }

crop_service = CropRecommendationService()

