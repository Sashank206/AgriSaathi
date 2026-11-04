from pydantic import BaseModel, Field
from typing import List, Optional

class FertilizerProduct(BaseModel):
    id: str
    name: str
    brand: str
    category: str  # Nitrogenous, Phosphatic, Potassic, Complex, Organic, Bio-Fertilizer, Micronutrient
    pack_size_kg: float
    price: float
    price_per_kg: float
    rating: Optional[float] = None  # Scale of 1 to 5, can be None if unrated
    rating_count: int = 0
    nutrient_composition: Optional[str] = None
    description: Optional[str] = None
    is_subsidized: bool = False

class FertilizerCreate(BaseModel):
    name: str = Field(..., min_length=2)
    brand: str = Field(..., min_length=2)
    category: str
    pack_size_kg: float = Field(..., gt=0)
    price: float = Field(..., gt=0)
    rating: Optional[float] = Field(default=None, ge=1.0, le=5.0)
    rating_count: int = Field(default=0, ge=0)
    nutrient_composition: Optional[str] = None
    description: Optional[str] = None
    is_subsidized: bool = False

class FertilizerScoredItem(BaseModel):
    product: FertilizerProduct
    normalized_price_score: float
    normalized_rating_score: float
    overall_score: float
    rank: int
    recommendation_note: str

class FertilizerCompareRequest(BaseModel):
    product_ids: List[str] = Field(..., min_length=2, max_length=10)
    alpha: float = Field(default=0.5, ge=0.0, le=1.0, description="Weight for price vs rating (0.0 to 1.0)")

class FertilizerCompareResponse(BaseModel):
    total_products: int
    alpha_used: float
    max_price_per_kg: float
    max_rating: float
    ranked_products: List[FertilizerScoredItem]
    formula_used: str = "S_i = α * (1 - u_i / u_max) + (1 - α) * (r_i / r_max)"

