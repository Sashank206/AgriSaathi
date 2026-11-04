import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)

class WeatherService:
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def evaluate_agricultural_alerts(
        self,
        temp_c: float,
        humidity: int,
        wind_kmh: float,
        rain_mm: float,
        location: str
    ) -> List[Dict[str, Any]]:
        """
        Rule-based agricultural weather alert evaluation.
        Evaluates conditions for:
        - Heavy rainfall / waterlogging risk
        - Strong wind / lodging risk
        - Frost / cold injury risk
        - High temperature / heat stress
        - Soil moisture / irrigation advisories
        """
        alerts = []
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        # 1. Heavy Rainfall Alert
        if rain_mm >= 25.0:
            alerts.append({
                "id": f"rain-{int(datetime.now().timestamp())}",
                "alert_type": "Heavy Rainfall Warning",
                "severity": "Warning" if rain_mm < 50.0 else "Critical",
                "title": f"Excess Rainfall Alert ({rain_mm} mm expected)",
                "description": f"Intense precipitation expected in {location}. High likelihood of field waterlogging.",
                "agricultural_suggestion": (
                    "Clear field drainage channels immediately. Postpone all chemical sprayings and nitrogen top-dressing. "
                    "Ensure newly sown nurseries have protective ridge bunds."
                ),
                "timestamp": now_str
            })

        # 2. Strong Wind / Lodging Alert
        if wind_kmh >= 30.0:
            alerts.append({
                "id": f"wind-{int(datetime.now().timestamp())}",
                "alert_type": "Strong Wind Advisory",
                "severity": "Warning",
                "title": f"High Gust Winds ({wind_kmh} km/h)",
                "description": "High wind velocities can induce lodging in tall cereal crops (sugarcane, maize, tall paddy).",
                "agricultural_suggestion": (
                    "Withhold heavy furrow irrigation to avoid loose soil root anchorage. "
                    "Tie / prop tall standing sugarcane and banana pseudo-stems. Suspend foliar spray operations."
                ),
                "timestamp": now_str
            })

        # 3. Frost Advisory
        if temp_c <= 4.0:
            alerts.append({
                "id": f"frost-{int(datetime.now().timestamp())}",
                "alert_type": "Frost / Chilling Injury Risk",
                "severity": "Critical",
                "title": f"Sub-Freezing/Near-Frost Night Temperatures ({temp_c}°C)",
                "description": "Severe risk of cellular ice crystal damage to tender vegetable crops and mustard flowers.",
                "agricultural_suggestion": (
                    "Apply light evening sprinkler irrigation to stabilize soil boundary temperatures. "
                    "Burn dry stubble/smoke screens on windward field perimeters during early morning hours. Cover nursery beds with plastic mulch."
                ),
                "timestamp": now_str
            })

        # 4. Extreme Heat / Thermal Stress
        if temp_c >= 38.0:
            alerts.append({
                "id": f"heat-{int(datetime.now().timestamp())}",
                "alert_type": "Heat Stress Warning",
                "severity": "Warning",
                "title": f"Extreme Afternoon Temperatures ({temp_c}°C)",
                "description": "Evapotranspiration rates peak; pollen sterility risk in flowering pulses and vegetables.",
                "agricultural_suggestion": (
                    "Provide frequent light irrigation during early morning or evening hours. "
                    "Apply straw/crop residue mulch over soil to prevent rapid moisture evaporation. Avoid spraying agrochemicals in mid-day sun."
                ),
                "timestamp": now_str
            })

        # 5. High Humidity & Fungal Pathogen Advisory
        if humidity >= 85 and temp_c >= 22.0:
            alerts.append({
                "id": f"pathogen-{int(datetime.now().timestamp())}",
                "alert_type": "Fungal Spore Proliferation Alert",
                "severity": "Information",
                "title": f"High Atmospheric Humidity ({humidity}%)",
                "description": "Prolonged high leaf wetness duration heavily favors fungal sporulation (blast, downy mildew, leaf spot).",
                "agricultural_suggestion": (
                    "Scout lower leaf canopy closely for early lesions. Prepare preventive bio-fungicides or copper sprays "
                    "once rainfall subsides."
                ),
                "timestamp": now_str
            })

        # Default standard advisory if no critical warnings
        if not alerts:
            alerts.append({
                "id": "norm-1",
                "alert_type": "Favorable Field Conditions",
                "severity": "Information",
                "title": "Optimal Weather Conditions for Farming Operations",
                "description": f"Mild temperatures ({temp_c}°C) and balanced humidity ({humidity}%).",
                "agricultural_suggestion": "Excellent window for scheduled weed management, intercultural operations, and balanced fertilizing.",
                "timestamp": now_str
            })

        return alerts

    def get_fallback_weather(
        self,
        location: str = "Central Agricultural Zone",
        reason: str = "Weather API key not configured or offline"
    ) -> Dict[str, Any]:
        """Provides realistic meteorological fallback data with honest provenance disclaimer."""
        now = datetime.now()
        temp = 27.5
        humidity = 58
        wind = 12.0
        rain = 0.0

        alerts = self.evaluate_agricultural_alerts(temp, humidity, wind, rain, location)
        
        forecast = []
        for i in range(1, 6):
            f_date = now + timedelta(days=i)
            forecast.append({
                "date": f_date.strftime("%Y-%m-%d"),
                "day_name": f_date.strftime("%A"),
                "temp_max": round(temp + (i % 3) - 1, 1),
                "temp_min": round(temp - 8 + (i % 2), 1),
                "humidity": min(85, humidity + (i * 3)),
                "pop_percent": 15 if i < 4 else 35,
                "condition": "Partly Cloudy" if i % 2 == 0 else "Sunny",
                "icon": "02d" if i % 2 == 0 else "01d",
                "wind_speed_kmh": round(wind + (i * 1.2), 1)
            })

        return {
            "current": {
                "temperature_celsius": temp,
                "feels_like_celsius": temp + 1.2,
                "humidity_percent": humidity,
                "rainfall_mm": rain,
                "wind_speed_kmh": wind,
                "wind_direction_deg": 180,
                "weather_condition": "Clear Sky / Mild",
                "weather_icon": "01d",
                "location_name": location,
                "country": "IN",
                "is_live_data": False,
                "data_source_note": f"Demonstration reference weather data ({reason}). Configure OPENWEATHER_API_KEY in .env for live satellite feed."
            },
            "forecast": forecast,
            "alerts": alerts,
            "farming_advisory": [
                "Schedule irrigation in accordance with local soil moisture depth.",
                "Monitor pest traps in morning hours.",
                "Weed eradication optimal during current dry spell."
            ]
        }

    async def get_weather(
        self,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        city: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Fetch weather from OpenWeatherMap or deliver structured fallback with honest status.
        Handles:
        - Missing API key
        - Invalid location / 404
        - Network failure
        """
        location_label = city or f"Coordinates ({lat:.2f}, {lon:.2f})" if lat and lon else "Regional Farm"
        
        if not self.api_key or self.api_key.strip() == "":
            return self.get_fallback_weather(location_label, "OPENWEATHER_API_KEY is not configured in backend/.env")

        try:
            params = {
                "appid": self.api_key,
                "units": "metric"
            }
            if lat is not None and lon is not None:
                params["lat"] = lat
                params["lon"] = lon
            elif city:
                params["q"] = city
            else:
                params["q"] = "Delhi,IN"

            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(f"{self.base_url}/weather", params=params)
                if resp.status_code != 200:
                    return self.get_fallback_weather(location_label, f"OpenWeather API returned status code {resp.status_code}")
                
                data = resp.json()
                
                # Fetch 5-day forecast
                forecast_resp = await client.get(f"{self.base_url}/forecast", params=params)
                forecast_days = []
                if forecast_resp.status_code == 200:
                    f_data = forecast_resp.json()
                    # Filter 1 per day around 12:00
                    for item in f_data.get("list", []):
                        if "12:00:00" in item.get("dt_txt", ""):
                            dt = datetime.fromtimestamp(item["dt"])
                            forecast_days.append({
                                "date": dt.strftime("%Y-%m-%d"),
                                "day_name": dt.strftime("%A"),
                                "temp_max": round(item["main"]["temp_max"], 1),
                                "temp_min": round(item["main"]["temp_min"], 1),
                                "humidity": item["main"]["humidity"],
                                "pop_percent": int(item.get("pop", 0) * 100),
                                "condition": item["weather"][0]["main"],
                                "icon": item["weather"][0]["icon"],
                                "wind_speed_kmh": round(item.get("wind", {}).get("speed", 0) * 3.6, 1)
                            })

                temp_c = round(data["main"]["temp"], 1)
                feels_like = round(data["main"]["feels_like"], 1)
                humidity = data["main"]["humidity"]
                wind_kmh = round(data.get("wind", {}).get("speed", 0) * 3.6, 1)
                rain_mm = round(data.get("rain", {}).get("1h", 0.0), 1)

                alerts = self.evaluate_agricultural_alerts(temp_c, humidity, wind_kmh, rain_mm, data.get("name", location_label))

                return {
                    "current": {
                        "temperature_celsius": temp_c,
                        "feels_like_celsius": feels_like,
                        "humidity_percent": humidity,
                        "rainfall_mm": rain_mm,
                        "wind_speed_kmh": wind_kmh,
                        "wind_direction_deg": data.get("wind", {}).get("deg"),
                        "weather_condition": data["weather"][0]["description"].title(),
                        "weather_icon": data["weather"][0]["icon"],
                        "location_name": data.get("name", location_label),
                        "country": data.get("sys", {}).get("country", "IN"),
                        "is_live_data": True,
                        "data_source_note": "Live satellite feed verified via OpenWeatherMap API."
                    },
                    "forecast": forecast_days,
                    "alerts": alerts,
                    "farming_advisory": [
                        "Plan spraying operations around wind speed readings.",
                        "Irrigate based on current humidity levels to curb evaporation loss."
                    ]
                }
        except Exception as e:
            logger.warning(f"Failed to fetch live weather: {e}")
            return self.get_fallback_weather(location_label, f"Network/API connection error: {str(e)}")

weather_service = WeatherService()

