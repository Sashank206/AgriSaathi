from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class WaterSourceEnum(str):
    BOREWELL = "Borewell"
    CANAL = "Canal irrigation"
    RAINFED = "Rain-fed"
    OTHER = "Other irrigation source"
    UNKNOWN = "Unknown"

class CropRecommendationRequest(BaseModel):
    state: str = Field(..., description="State where the farm is located")
    district: str = Field(..., description="District name")
    village: Optional[str] = Field(default="", description="Optional village name")
    latitude: Optional[float] = Field(default=None, description="GPS latitude from browser")
    longitude: Optional[float] = Field(default=None, description="GPS longitude from browser")
    soil_type: Optional[str] = Field(default=None, description="Observed soil type (e.g. Alluvial, Black, Red, Sandy Loam, Clay)")
    water_source: str = Field(default="Unknown", description="Irrigation water source availability")
    season: Optional[str] = Field(default=None, description="Agricultural season (Kharif, Rabi, Zaid)")

class CropRecommendationItem(BaseModel):
    crop_name: str
    suitability_score: float = Field(..., description="Calculated suitability percentage (0 - 100)")
    reason: str
    suitable_season: str
    water_requirement: str
    basic_guidance: str

class LocationDetails(BaseModel):
    state: str
    district: str
    village: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    source: str = "user_input"

class SoilDetails(BaseModel):
    soil_type: Optional[str] = None
    source: str = "unavailable"  # "regional_database", "farmer_provided", or "unavailable"
    characteristics: Optional[str] = None

class WeatherDetails(BaseModel):
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    rainfall_estimate: Optional[float] = None
    season_detected: Optional[str] = None
    source: str = "api"  # "openweather_live" or "seasonal_regional_normals"

class CropRecommendationResponse(BaseModel):
    success: bool
    location: LocationDetails
    soil_info: SoilDetails
    weather_info: WeatherDetails
    water_source: str
    model_configured: bool = False
    model_type: str = "RandomForest / Heuristic Fallback"
    recommendations: List[CropRecommendationItem]
    message: str

