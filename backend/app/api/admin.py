from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from bson import ObjectId
import uuid
from app.schemas.user import UserRole, UserResponse
from app.schemas.admin import SystemStatsResponse
from app.schemas.fertilizer import FertilizerCreate, FertilizerProduct
from app.middleware.auth_middleware import require_role, _mock_users_db
from app.database.mongodb import get_database, db_manager
from app.services.disease_service import disease_service
from app.services.crop_service import crop_service
from app.services.fertilizer_service import fertilizer_service, INITIAL_FERTILIZERS

router = APIRouter(prefix="/admin", tags=["Admin Operations"])

@router.get("/stats", response_model=SystemStatsResponse)
async def get_system_statistics(admin_user: dict = Depends(require_role([UserRole.ADMIN]))):
    """Admin-only: Aggregate system activity metrics and component statuses."""
    db = get_database()
    
    total_users = 0
    total_farmers = 0
    total_experts = 0
    total_scans = 0
    pending_reviews = 0
    total_fertilizers = 0
    
    if db_manager.is_connected and db is not None:
        try:
            total_users = await db.users.count_documents({})
            total_farmers = await db.users.count_documents({"role": "farmer"})
            total_experts = await db.users.count_documents({"role": "expert"})
            total_scans = await db.disease_cases.count_documents({})
            pending_reviews = await db.disease_cases.count_documents({"status": "pending_expert_review"})
            total_fertilizers = await db.fertilizer_products.count_documents({})
        except Exception:
            pass
    else:
        # Fallback to in-memory stats
        total_users = len(_mock_users_db) + 3
        total_farmers = sum(1 for u in _mock_users_db.values() if u.get("role") == "farmer") + 2
        total_experts = sum(1 for u in _mock_users_db.values() if u.get("role") == "expert") + 1
        total_fertilizers = len(fertilizer_service.mock_products)
        pending_reviews = 2
        total_scans = 5

    return SystemStatsResponse(
        total_users=total_users,
        total_farmers=total_farmers,
        total_experts=total_experts,
        total_disease_scans=total_scans,
        pending_expert_reviews=pending_reviews,
        total_fertilizers=total_fertilizers,
        database_connected=db_manager.is_connected,
        ai_models_status={
            "cnn_disease_detection": disease_service.model_loaded,
            "crop_recommendation_ml": crop_service.model_loaded
        },
        active_weather_alerts=3
    )

@router.get("/users")
async def list_all_users(admin_user: dict = Depends(require_role([UserRole.ADMIN]))):
    """Admin-only: View registered platform users."""
    db = get_database()
    users = []
    if db_manager.is_connected and db is not None:
        cursor = db.users.find({}, {"password_hash": 0}).sort("created_at", -1)
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            users.append(doc)
    else:
        for u in _mock_users_db.values():
            safe = {k: v for k, v in u.items() if k != "password_hash"}
            users.append(safe)
            
    return users

@router.post("/fertilizers", response_model=FertilizerProduct)
async def add_fertilizer_product(
    product_in: FertilizerCreate,
    admin_user: dict = Depends(require_role([UserRole.ADMIN]))
):
    """Admin-only: Add a new verified fertilizer product to the database."""
    price_per_kg = round(product_in.price / product_in.pack_size_kg, 2)
    new_doc = product_in.model_dump()
    new_doc["price_per_kg"] = price_per_kg

    db = get_database()
    if db_manager.is_connected and db is not None:
        res = await db.fertilizer_products.insert_one(new_doc)
        new_doc["id"] = str(res.inserted_id)
    else:
        pid = str(uuid.uuid4())
        new_doc["_id"] = pid
        new_doc["id"] = pid
        fertilizer_service.mock_products[pid] = new_doc

    return new_doc

@router.delete("/fertilizers/{product_id}")
async def delete_fertilizer_product(
    product_id: str,
    admin_user: dict = Depends(require_role([UserRole.ADMIN]))
):
    """Admin-only: Remove a fertilizer product."""
    db = get_database()
    deleted = False
    if db_manager.is_connected and db is not None:
        res = await db.fertilizer_products.delete_one({"_id": ObjectId(product_id) if ObjectId.is_valid(product_id) else product_id})
        deleted = res.deleted_count > 0
    elif product_id in fertilizer_service.mock_products:
        del fertilizer_service.mock_products[product_id]
        deleted = True

    if not deleted:
        raise HTTPException(status_code=404, detail="Fertilizer product not found.")
    return {"success": True, "message": "Fertilizer product removed successfully."}

