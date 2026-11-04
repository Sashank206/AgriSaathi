from fastapi import APIRouter, Query
from typing import Optional
from app.services.weather_service import weather_service
from app.schemas.weather import WeatherOverviewResponse

router = APIRouter(prefix="/weather", tags=["Weather Monitoring & Smart Alerts"])

@router.get("/current", response_model=WeatherOverviewResponse)
async def get_current_weather(
    lat: Optional[float] = Query(None, description="GPS latitude"),
    lon: Optional[float] = Query(None, description="GPS longitude"),
    city: Optional[str] = Query(None, description="City / District name in India")
):
    """
    Get current weather, 5-day agro-forecast, and smart rule-based agricultural alerts.
    Gracefully handles missing OpenWeather keys with transparent reference data provenance.
    """
    data = await weather_service.get_weather(lat=lat, lon=lon, city=city)
    return data

@router.get("/forecast")
async def get_weather_forecast(
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    city: Optional[str] = Query(None)
):
    """Get multi-day agricultural weather forecast."""
    data = await weather_service.get_weather(lat=lat, lon=lon, city=city)
    return {
        "location": data["current"]["location_name"],
        "is_live": data["current"]["is_live_data"],
        "forecast": data["forecast"],
        "farming_advisory": data["farming_advisory"]
    }

