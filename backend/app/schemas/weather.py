from pydantic import BaseModel, Field
from typing import List, Optional

class WeatherAlertItem(BaseModel):
    id: str
    alert_type: str  # Heavy Rainfall, Strong Wind, Frost, High Temperature, Irrigation Notice
    severity: str    # Information, Warning, Severe, Critical
    title: str
    description: str
    agricultural_suggestion: str
    timestamp: str

class CurrentWeather(BaseModel):
    temperature_celsius: float
    feels_like_celsius: float
    humidity_percent: int
    rainfall_mm: float
    wind_speed_kmh: float
    wind_direction_deg: Optional[int] = None
    weather_condition: str
    weather_icon: str
    location_name: str
    country: str = "IN"
    is_live_data: bool
    data_source_note: str

class ForecastDay(BaseModel):
    date: str
    day_name: str
    temp_max: float
    temp_min: float
    humidity: int
    pop_percent: int  # probability of precipitation
    condition: str
    icon: str
    wind_speed_kmh: float

class WeatherOverviewResponse(BaseModel):
    current: CurrentWeather
    forecast: List[ForecastDay]
    alerts: List[WeatherAlertItem]
    farming_advisory: List[str]

