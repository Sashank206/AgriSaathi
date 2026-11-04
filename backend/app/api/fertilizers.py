from fastapi import APIRouter, HTTPException, Query, status
from typing import List, Optional
from app.services.fertilizer_service import fertilizer_service
from app.schemas.fertilizer import FertilizerProduct, FertilizerCompareRequest, FertilizerCompareResponse

router = APIRouter(prefix="/fertilizers", tags=["Fertilizer Price & Quality Comparison"])

@router.get("", response_model=List[FertilizerProduct])
async def list_fertilizers(
    category: Optional[str] = Query(None, description="Category filter (e.g. Nitrogenous, Phosphatic, Organic)"),
    search: Optional[str] = Query(None, description="Search by fertilizer name or brand")
):
    """Retrieve list of verified fertilizer products with market price & rating metrics."""
    products = await fertilizer_service.get_all_products(category=category, search=search)
    return products

@router.get("/{product_id}", response_model=FertilizerProduct)
async def get_fertilizer_details(product_id: str):
    """Get single fertilizer details by ID."""
    prod = await fertilizer_service.get_product_by_id(product_id)
    if not prod:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fertilizer product with ID '{product_id}' was not found."
        )
    return prod

@router.post("/compare", response_model=FertilizerCompareResponse)
async def compare_fertilizers(payload: FertilizerCompareRequest):
    """
    Compare multiple fertilizer products based on formula:
    S_i = α * (1 - u_i / u_max) + (1 - α) * (r_i / r_max)
    """
    selected_products = []
    for pid in payload.product_ids:
        prod = await fertilizer_service.get_product_by_id(pid)
        if prod:
            selected_products.append(prod)

    if len(selected_products) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide at least 2 valid fertilizer product IDs to perform comparison."
        )

    result = fertilizer_service.calculate_comparison(selected_products, alpha=payload.alpha)
    return result

