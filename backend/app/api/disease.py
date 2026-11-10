from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from typing import Optional, List
from datetime import datetime, timezone
from bson import ObjectId
import uuid
from app.services.disease_service import disease_service, DISEASE_KNOWLEDGE_BASE
from app.schemas.disease import DiseasePredictResponse, DiseaseCaseResponse, DiseaseKnowledgeItem
from app.middleware.auth_middleware import get_current_user
from app.database.mongodb import get_database, db_manager

router = APIRouter(prefix="/disease", tags=["Plant Disease Detection"])

# Mock store for cases if MongoDB is disconnected
_mock_disease_cases = {}

@router.post("/predict", response_model=DiseasePredictResponse)
async def predict_plant_disease(
    file: UploadFile = File(...),
    crop_type: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
):
    """
    Primary AI Feature: Analyze plant leaf image.
    Performs image validation, handles modular CNN model integration,
    and logs case record for the farmer and expert review.
    """
    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty. Please select a valid plant leaf image."
        )

    # Invoke modular disease service
    analysis_result = await disease_service.predict(
        file_bytes=file_bytes,
        filename=file.filename or "leaf.jpg",
        crop_type=crop_type
    )

    if not analysis_result["success"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=analysis_result["message"]
        )

    user_id = str(current_user.get("_id", current_user.get("id")))
    case_doc = {
        "user_id": user_id,
        "crop_type": crop_type or analysis_result.get("plant_name", "Unknown"),
        "image_path": analysis_result.get("image_path"),
        "image_url": analysis_result.get("image_url"),
        "predicted_disease": analysis_result.get("predicted_disease"),
        "confidence_score": analysis_result.get("confidence_score"),
        "model_configured": analysis_result.get("model_configured", False),
        "status": "pending_expert_review" if not analysis_result.get("model_configured") else "analyzed",
        "expert_diagnosis": None,
        "expert_treatment": None,
        "created_at": datetime.now(timezone.utc)
    }

    db = get_database()
    if db_manager.is_connected and db is not None:
        result = await db.disease_cases.insert_one(case_doc)
        case_id = str(result.inserted_id)
    else:
        case_id = str(uuid.uuid4())
        case_doc["_id"] = case_id
        _mock_disease_cases[case_id] = case_doc

    return DiseasePredictResponse(
        success=True,
        plant_name=analysis_result.get("plant_name"),
        predicted_disease=analysis_result.get("predicted_disease"),
        confidence_score=analysis_result.get("confidence_score"),
        disease_description=analysis_result.get("disease_description"),
        visible_symptoms=analysis_result.get("visible_symptoms", []),
        treatment_recommendations=analysis_result.get("treatment_recommendations", []),
        preventive_measures=analysis_result.get("preventive_measures", []),
        image_url=analysis_result.get("image_url"),
        case_id=case_id,
        model_configured=analysis_result.get("model_configured", False),
        message=analysis_result.get("message"),
        risk_level=analysis_result.get("risk_level", "Medium"),
        top_probabilities=analysis_result.get("top_probabilities"),
        top_predictions=analysis_result.get("top_predictions", [])
    )

@router.get("/cases", response_model=List[DiseaseCaseResponse])
async def get_my_disease_cases(current_user: dict = Depends(get_current_user)):
    """Retrieve history of uploaded plant scans for the current farmer."""
    user_id = str(current_user.get("_id", current_user.get("id")))
    db = get_database()
    cases = []
    
    if db_manager.is_connected and db is not None:
        cursor = db.disease_cases.find({"user_id": user_id}).sort("created_at", -1)
        async for doc in cursor:
            cases.append(DiseaseCaseResponse(
                id=str(doc["_id"]),
                user_id=doc["user_id"],
                crop_type=doc.get("crop_type"),
                image_path=doc.get("image_path", ""),
                image_url=doc.get("image_url", ""),
                predicted_disease=doc.get("predicted_disease"),
                confidence_score=doc.get("confidence_score"),
                status=doc.get("status", "pending"),
                expert_diagnosis=doc.get("expert_diagnosis"),
                expert_treatment=doc.get("expert_treatment"),
                expert_id=doc.get("expert_id"),
                created_at=doc.get("created_at", datetime.now(timezone.utc))
            ))
    else:
        for c in _mock_disease_cases.values():
            if c.get("user_id") == user_id:
                cases.append(DiseaseCaseResponse(
                    id=str(c.get("_id")),
                    user_id=c["user_id"],
                    crop_type=c.get("crop_type"),
                    image_path=c.get("image_path", ""),
                    image_url=c.get("image_url", ""),
                    predicted_disease=c.get("predicted_disease"),
                    confidence_score=c.get("confidence_score"),
                    status=c.get("status", "pending"),
                    expert_diagnosis=c.get("expert_diagnosis"),
                    expert_treatment=c.get("expert_treatment"),
                    expert_id=c.get("expert_id"),
                    created_at=c.get("created_at", datetime.now(timezone.utc))
                ))
    return cases

@router.get("/knowledge", response_model=List[DiseaseKnowledgeItem])
async def get_disease_knowledge_base():
    """Retrieve agronomic reference data from verified knowledge-base."""
    items = []
    for k, v in DISEASE_KNOWLEDGE_BASE.items():
        items.append(DiseaseKnowledgeItem(
            crop_name=v["crop_name"],
            disease_name=v["disease_name"],
            description=v["description"],
            symptoms=v["symptoms"],
            treatment_recommendations=v["treatment_recommendations"],
            preventive_measures=v["preventive_measures"],
            risk_level=v.get("risk_level", "Medium")
        ))
    return items

@router.post("/cases/{case_id}/request-review")
async def request_expert_review(case_id: str, current_user: dict = Depends(get_current_user)):
    """Flag a case for Agriculture Expert manual review and diagnosis."""
    db = get_database()
    updated = False
    if db_manager.is_connected and db is not None:
        res = await db.disease_cases.update_one(
            {"_id": ObjectId(case_id) if ObjectId.is_valid(case_id) else case_id},
            {"$set": {"status": "pending_expert_review", "review_requested_at": datetime.now(timezone.utc)}}
        )
        updated = res.modified_count > 0
    elif case_id in _mock_disease_cases:
        _mock_disease_cases[case_id]["status"] = "pending_expert_review"
        updated = True

    if not updated:
        raise HTTPException(status_code=404, detail="Disease case not found.")
        
    return {"success": True, "message": "Case successfully submitted to Agriculture Expert queue for review."}

