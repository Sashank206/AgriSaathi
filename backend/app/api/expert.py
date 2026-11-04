from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone
from bson import ObjectId
from app.schemas.user import UserRole
from app.middleware.auth_middleware import require_role
from app.database.mongodb import get_database, db_manager
from app.api.disease import _mock_disease_cases

router = APIRouter(prefix="/expert", tags=["Agriculture Expert Operations"])

class ExpertReviewSubmission(BaseModel):
    expert_diagnosis: str = Field(..., min_length=3)
    expert_treatment: str = Field(..., min_length=10)
    severity_assessment: Optional[str] = "Moderate"
    status: str = "reviewed"

@router.get("/pending-cases")
async def get_pending_review_cases(
    expert_user: dict = Depends(require_role([UserRole.EXPERT, UserRole.ADMIN]))
):
    """Expert-only: Retrieve all disease scan cases awaiting expert diagnosis."""
    db = get_database()
    cases = []
    
    if db_manager.is_connected and db is not None:
        cursor = db.disease_cases.find({}).sort("created_at", -1)
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            cases.append(doc)
    else:
        for cid, doc in _mock_disease_cases.items():
            item = doc.copy()
            item["id"] = cid
            cases.append(item)

    # If no cases in store yet, provide a demo case so the expert dashboard UI is testable immediately
    if not cases:
        demo_case = {
            "id": "demo-case-101",
            "user_id": "demo-farmer-id",
            "crop_type": "Tomato",
            "image_url": "/uploads/disease_images/demo_tomato.jpg",
            "predicted_disease": "Early Blight (Alternaria solani)",
            "confidence_score": None,
            "model_configured": False,
            "status": "pending_expert_review",
            "expert_diagnosis": None,
            "expert_treatment": None,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        cases.append(demo_case)

    return cases

@router.post("/cases/{case_id}/review")
async def submit_expert_diagnosis(
    case_id: str,
    review: ExpertReviewSubmission,
    expert_user: dict = Depends(require_role([UserRole.EXPERT, UserRole.ADMIN]))
):
    """Expert-only: Submit agronomic verification, clinical diagnosis, and chemical/organic prescription."""
    expert_id = str(expert_user.get("_id", expert_user.get("id")))
    expert_name = expert_user.get("full_name", "Agriculture Expert")

    update_payload = {
        "expert_diagnosis": review.expert_diagnosis,
        "expert_treatment": review.expert_treatment,
        "severity_assessment": review.severity_assessment,
        "expert_id": expert_id,
        "expert_name": expert_name,
        "status": "reviewed",
        "reviewed_at": datetime.now(timezone.utc)
    }

    db = get_database()
    updated = False

    if db_manager.is_connected and db is not None:
        res = await db.disease_cases.update_one(
            {"_id": ObjectId(case_id) if ObjectId.is_valid(case_id) else case_id},
            {"$set": update_payload}
        )
        updated = res.modified_count > 0
    elif case_id in _mock_disease_cases:
        _mock_disease_cases[case_id].update(update_payload)
        updated = True
    elif case_id == "demo-case-101":
        updated = True

    if not updated:
        raise HTTPException(status_code=404, detail="Disease case not found.")

    return {
        "success": True,
        "message": f"Diagnosis successfully recorded by {expert_name}.",
        "case_id": case_id
    }

