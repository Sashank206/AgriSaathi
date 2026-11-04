from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime, timezone
from bson import ObjectId
import uuid
from app.schemas.crop import CropRecommendationRequest, CropRecommendationResponse
from app.services.crop_service import crop_service
from app.services.weather_service import weather_service
from app.middleware.auth_middleware import get_current_user
from app.database.mongodb import get_database, db_manager

router = APIRouter(prefix="/crop", tags=["Location-Based Crop Recommendation"])

_mock_crop_history = {}

@router.post("/recommend", response_model=CropRecommendationResponse)
async def recommend_crops(
    req: CropRecommendationRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Location-Based Crop Recommendation without requiring manual NPK entries.
    Combines GPS/district location, regional/farmer soil, practical irrigation availability,
    and weather conditions.
    """
    # Retrieve weather context for the location
    weather_info = None
    try:
        w_data = await weather_service.get_weather(
            lat=req.latitude,
            lon=req.longitude,
            city=f"{req.district},IN"
        )
        weather_info = w_data.get("current")
    except Exception:
        pass

    result = await crop_service.recommend_crops(
        state=req.state,
        district=req.district,
        village=req.village,
        latitude=req.latitude,
        longitude=req.longitude,
        soil_type=req.soil_type,
        water_source=req.water_source,
        season=req.season,
        weather_info=weather_info
    )

    user_id = str(current_user.get("_id", current_user.get("id")))
    rec_record = {
        "user_id": user_id,
        "request": req.model_dump(),
        "response": result,
        "created_at": datetime.now(timezone.utc)
    }

    db = get_database()
    if db_manager.is_connected and db is not None:
        await db.crop_recommendations.insert_one(rec_record)
    else:
        rec_id = str(uuid.uuid4())
        _mock_crop_history[rec_id] = rec_record

    return result

@router.get("/history")
async def get_crop_history(current_user: dict = Depends(get_current_user)):
    """Retrieve farmer's past crop recommendation evaluations."""
    user_id = str(current_user.get("_id", current_user.get("id")))
    db = get_database()
    history = []

    if db_manager.is_connected and db is not None:
        cursor = db.crop_recommendations.find({"user_id": user_id}).sort("created_at", -1).limit(10)
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            history.append(doc)
    else:
        for rec_id, doc in _mock_crop_history.items():
            if doc.get("user_id") == user_id:
                item = doc.copy()
                item["id"] = rec_id
                history.append(item)

    return history

