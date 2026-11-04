import logging
from typing import List, Dict, Any, Optional
from bson import ObjectId
from app.database.mongodb import get_database, db_manager

logger = logging.getLogger(__name__)

# Realistic seed catalog of agricultural fertilizers with official MRP / market reference rates in India
INITIAL_FERTILIZERS: List[Dict[str, Any]] = [
    {
        "_id": "6727a1b1c1d1e1f1a1b1c101",
        "name": "Neem Coated Urea (46% N)",
        "brand": "IFFCO",
        "category": "Nitrogenous",
        "pack_size_kg": 45.0,
        "price": 266.50,
        "price_per_kg": 5.92,
        "rating": 4.8,
        "rating_count": 1420,
        "nutrient_composition": "46% Nitrogen (N)",
        "description": "Government subsidized neem oil coated urea offering slow release nitrogen and pest deterrence.",
        "is_subsidized": True
    },
    {
        "_id": "6727a1b1c1d1e1f1a1b1c102",
        "name": "Di-Ammonium Phosphate (DAP 18-46-0)",
        "brand": "KRIBHCO",
        "category": "Phosphatic",
        "pack_size_kg": 50.0,
        "price": 1350.00,
        "price_per_kg": 27.00,
        "rating": 4.7,
        "rating_count": 980,
        "nutrient_composition": "18% Nitrogen (N), 46% Phosphorus (P2O5)",
        "description": "Essential basal fertilizer supplying soluble phosphate for strong root emergence and early seedling vigor.",
        "is_subsidized": True
    },
    {
        "_id": "6727a1b1c1d1e1f1a1b1c103",
        "name": "Muriate of Potash (MOP 0-0-60)",
        "brand": "IPL (Indian Potash Limited)",
        "category": "Potassic",
        "pack_size_kg": 50.0,
        "price": 1650.00,
        "price_per_kg": 33.00,
        "rating": 4.5,
        "rating_count": 620,
        "nutrient_composition": "60% Potassium (K2O)",
        "description": "Enhances crop disease resistance, lodging tolerance, drought resilience, and grain quality.",
        "is_subsidized": True
    },
    {
        "_id": "6727a1b1c1d1e1f1a1b1c104",
        "name": "Single Super Phosphate (SSP 16% P2O5, 11% S)",
        "brand": "Coromandel International",
        "category": "Phosphatic",
        "pack_size_kg": 50.0,
        "price": 550.00,
        "price_per_kg": 11.00,
        "rating": 4.3,
        "rating_count": 415,
        "nutrient_composition": "16% Water Soluble P2O5, 11% Sulfur, 19% Calcium",
        "description": "Cost-effective phosphorus and sulfur source particularly beneficial for oilseeds and pulse crops.",
        "is_subsidized": True
    },
    {
        "_id": "6727a1b1c1d1e1f1a1b1c105",
        "name": "NPK 10:26:26 Complex",
        "brand": "IFFCO",
        "category": "Complex",
        "pack_size_kg": 50.0,
        "price": 1470.00,
        "price_per_kg": 29.40,
        "rating": 4.6,
        "rating_count": 510,
        "nutrient_composition": "10% N, 26% P2O5, 26% K2O",
        "description": "High analysis complex fertilizer tailored for cash crops, cotton, sugarcane, and potato.",
        "is_subsidized": True
    },
    {
        "_id": "6727a1b1c1d1e1f1a1b1c106",
        "name": "Premium Enriched Vermicompost",
        "brand": "Jaivik Bharat / Organic Agro",
        "category": "Organic",
        "pack_size_kg": 40.0,
        "price": 320.00,
        "price_per_kg": 8.00,
        "rating": 4.4,
        "rating_count": 280,
        "nutrient_composition": "Organic Carbon 16%, NPK 1.5-2.0%, Beneficial Microbes",
        "description": "Enhances soil porosity, water holding capacity, and microbial biodiversity.",
        "is_subsidized": False
    },
    {
        "_id": "6727a1b1c1d1e1f1a1b1c107",
        "name": "Zinc Sulfate Heptahydrate (Zn 21%)",
        "brand": "Tata Chemicals (Paras)",
        "category": "Micronutrient",
        "pack_size_kg": 10.0,
        "price": 480.00,
        "price_per_kg": 48.00,
        "rating": 4.5,
        "rating_count": 310,
        "nutrient_composition": "21% Zinc (Zn), 10% Sulfur",
        "description": "Corrects Khaira disease in paddy and severe zinc deficiencies across calcareous soils.",
        "is_subsidized": False
    },
    {
        "_id": "6727a1b1c1d1e1f1a1b1c108",
        "name": "Pure Cold-Pressed Neem Cake Powder",
        "brand": "Green Agro",
        "category": "Bio-Fertilizer",
        "pack_size_kg": 25.0,
        "price": 450.00,
        "price_per_kg": 18.00,
        "rating": 4.2,
        "rating_count": 195,
        "nutrient_composition": "Organic N 2-5%, Azadirachtin organic bio-nematicide",
        "description": "Natural pest and nematode repellant that retards nitrification in soil for sustained nitrogen availability.",
        "is_subsidized": False
    }
]

class FertilizerService:
    def __init__(self):
        # In-memory storage copy when MongoDB is offline
        self.mock_products = {p["_id"]: p.copy() for p in INITIAL_FERTILIZERS}

    async def get_all_products(
        self,
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Retrieve fertilizers with optional category and search query filters."""
        db = get_database()
        products = []
        if db_manager.is_connected and db is not None:
            try:
                query = {}
                if category and category != "all":
                    query["category"] = category
                if search:
                    query["$or"] = [
                        {"name": {"$regex": search, "$options": "i"}},
                        {"brand": {"$regex": search, "$options": "i"}},
                        {"category": {"$regex": search, "$options": "i"}}
                    ]
                cursor = db.fertilizer_products.find(query)
                async for doc in cursor:
                    doc["id"] = str(doc["_id"])
                    products.append(doc)
            except Exception as e:
                logger.warning(f"Error querying fertilizers from MongoDB: {e}")

        # If MongoDB is empty or unpopulated, seed it or return mock store
        if not products:
            if db_manager.is_connected and db is not None:
                try:
                    await self.seed_initial_products()
                    cursor = db.fertilizer_products.find({})
                    async for doc in cursor:
                        doc["id"] = str(doc["_id"])
                        products.append(doc)
                except Exception:
                    pass
            
            if not products:
                # Use in-memory catalog
                for pid, p in self.mock_products.items():
                    item = p.copy()
                    item["id"] = str(item["_id"])
                    if category and category != "all" and item["category"].lower() != category.lower():
                        continue
                    if search:
                        s_lower = search.lower()
                        if s_lower not in item["name"].lower() and s_lower not in item["brand"].lower():
                            continue
                    products.append(item)

        return products

    async def get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Fetch single fertilizer product by ID."""
        db = get_database()
        if db_manager.is_connected and db is not None:
            try:
                doc = await db.fertilizer_products.find_one({"_id": ObjectId(product_id) if ObjectId.is_valid(product_id) else product_id})
                if doc:
                    doc["id"] = str(doc["_id"])
                    return doc
            except Exception:
                pass
        
        if product_id in self.mock_products:
            item = self.mock_products[product_id].copy()
            item["id"] = str(item["_id"])
            return item
        return None

    async def seed_initial_products(self):
        """Seed initial realistic fertilizer catalog into MongoDB if empty."""
        db = get_database()
        if db_manager.is_connected and db is not None:
            try:
                count = await db.fertilizer_products.count_documents({})
                if count == 0:
                    await db.fertilizer_products.insert_many([p.copy() for p in INITIAL_FERTILIZERS])
                    logger.info("Seeded initial fertilizer catalog into MongoDB.")
            except Exception as e:
                logger.warning(f"Could not seed fertilizer catalog: {e}")

    def calculate_comparison(
        self,
        products: List[Dict[str, Any]],
        alpha: float = 0.5
    ) -> Dict[str, Any]:
        """
        Calculates ranking based on the requested formula:
        S_i = α * (1 - u_i / u_max) + (1 - α) * (r_i / r_max)
        Where:
        - S_i = overall score
        - u_i = price per unit (per kg)
        - u_max = maximum comparable unit price among selected products
        - r_i = product rating (1.0 to 5.0)
        - r_max = maximum rating (5.0)
        - α = price weight (0.0 to 1.0)
        """
        if not products:
            return {"ranked_products": [], "total_products": 0, "alpha_used": alpha, "max_price_per_kg": 0, "max_rating": 5.0}

        u_max = max(p.get("price_per_kg", 1.0) for p in products)
        if u_max <= 0:
            u_max = 1.0
        r_max = 5.0  # standard 5-star rating scale

        scored_items = []
        for p in products:
            u_i = p.get("price_per_kg", 0.0)
            
            # Handle unrated or missing rating gracefully (use neutral rating 3.0)
            raw_rating = p.get("rating")
            r_i = float(raw_rating) if raw_rating is not None else 3.0
            
            # Normalized component scores:
            price_score = max(0.0, 1.0 - (u_i / u_max))
            rating_score = min(1.0, max(0.0, r_i / r_max))
            
            overall_score = (alpha * price_score) + ((1.0 - alpha) * rating_score)
            overall_score_percentage = round(overall_score * 100, 2)
            
            # Formulate recommendation reasoning
            reasons = []
            if price_score >= 0.7:
                reasons.append("Highly economical unit cost (₹/kg)")
            if rating_score >= 0.85:
                reasons.append("High farmer satisfaction & verified reliability")
            if p.get("is_subsidized"):
                reasons.append("Government subsidized pricing")
            if not reasons:
                reasons.append("Balanced price-to-performance ratio")

            scored_items.append({
                "product": {
                    "id": str(p.get("_id", p.get("id"))),
                    "name": p.get("name"),
                    "brand": p.get("brand"),
                    "category": p.get("category"),
                    "pack_size_kg": p.get("pack_size_kg"),
                    "price": p.get("price"),
                    "price_per_kg": p.get("price_per_kg"),
                    "rating": p.get("rating"),
                    "rating_count": p.get("rating_count", 0),
                    "nutrient_composition": p.get("nutrient_composition"),
                    "description": p.get("description"),
                    "is_subsidized": p.get("is_subsidized", False)
                },
                "normalized_price_score": round(price_score, 4),
                "normalized_rating_score": round(rating_score, 4),
                "overall_score": overall_score_percentage,
                "rank": 1,  # will be assigned after sort
                "recommendation_note": "; ".join(reasons)
            })

        # Sort descending by overall score
        scored_items.sort(key=lambda x: x["overall_score"], reverse=True)
        for idx, item in enumerate(scored_items, start=1):
            item["rank"] = idx

        return {
            "total_products": len(scored_items),
            "alpha_used": alpha,
            "max_price_per_kg": u_max,
            "max_rating": r_max,
            "ranked_products": scored_items,
            "formula_used": "S_i = α * (1 - u_i / u_max) + (1 - α) * (r_i / r_max)"
        }

fertilizer_service = FertilizerService()

