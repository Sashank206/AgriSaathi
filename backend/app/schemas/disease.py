from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class DiseaseKnowledgeItem(BaseModel):
    crop_name: str
    disease_name: str
    description: str
    symptoms: List[str]
    treatment_recommendations: List[str]
    preventive_measures: List[str]
    risk_level: str = "Medium"  # Low, Medium, High, Critical

class TopPredictionItem(BaseModel):
    condition: str
    confidence_percentage: float
    is_healthy: bool = False

class DiseasePredictResponse(BaseModel):
    success: bool
    plant_name: Optional[str] = None
    predicted_disease: Optional[str] = None
    confidence_score: Optional[float] = None
    disease_description: Optional[str] = None
    visible_symptoms: List[str] = []
    treatment_recommendations: List[str] = []
    preventive_measures: List[str] = []
    image_url: Optional[str] = None
    case_id: Optional[str] = None
    model_configured: bool = False
    message: str
    risk_level: Optional[str] = "Medium"
    top_probabilities: Optional[dict] = None
    top_predictions: Optional[List[TopPredictionItem]] = []

class DiseaseCaseCreate(BaseModel):
    crop_type: Optional[str] = "Unknown"
    notes: Optional[str] = None

class DiseaseCaseResponse(BaseModel):
    id: str
    user_id: str
    crop_type: Optional[str] = None
    image_path: str
    image_url: str
    predicted_disease: Optional[str] = None
    confidence_score: Optional[float] = None
    status: str = "pending"  # pending, reviewed, closed
    expert_diagnosis: Optional[str] = None
    expert_treatment: Optional[str] = None
    expert_id: Optional[str] = None
    created_at: datetime

