from pydantic import BaseModel
from typing import Dict, Any, List

class SystemStatsResponse(BaseModel):
    total_users: int
    total_farmers: int
    total_experts: int
    total_disease_scans: int
    pending_expert_reviews: int
    total_fertilizers: int
    database_connected: bool
    ai_models_status: Dict[str, bool]
    active_weather_alerts: int

