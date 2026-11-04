import logging
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from app.core.config import settings

logger = logging.getLogger(__name__)

class MongoDBManager:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None
    is_connected: bool = False

db_manager = MongoDBManager()

async def connect_to_mongo():
    """Connect to MongoDB Atlas or local MongoDB instance."""
    try:
        logger.info(f"Connecting to MongoDB at {settings.MONGODB_URI.split('@')[-1] if '@' in settings.MONGODB_URI else 'local'}...")
        db_manager.client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=4000,
            connectTimeoutMS=4000
        )
        # Test connection with ping
        await db_manager.client.admin.command('ping')
        db_manager.db = db_manager.client[settings.DATABASE_NAME]
        db_manager.is_connected = True
        logger.info(f"Successfully connected to MongoDB database: {settings.DATABASE_NAME}")
        
        # Initialize indexes
        await init_db_indexes()
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        db_manager.is_connected = False
        logger.warning(
            f"MongoDB connection could not be established: {e}. "
            "Backend will run with in-memory fallback store for demonstration/development."
        )
    except Exception as e:
        db_manager.is_connected = False
        logger.error(f"Unexpected MongoDB connection error: {e}")

async def close_mongo_connection():
    """Close MongoDB connection pool."""
    if db_manager.client:
        db_manager.client.close()
        db_manager.is_connected = False
        logger.info("MongoDB connection closed.")

async def init_db_indexes():
    """Create indexes for performance and unique constraints."""
    if not db_manager.is_connected or db_manager.db is None:
        return
    try:
        # Users collection
        await db_manager.db.users.create_index("email", unique=True)
        await db_manager.db.users.create_index("role")
        
        # Disease cases
        await db_manager.db.disease_cases.create_index("user_id")
        await db_manager.db.disease_cases.create_index("created_at")
        await db_manager.db.disease_cases.create_index("status")
        
        # Fertilizer products
        await db_manager.db.fertilizer_products.create_index("category")
        await db_manager.db.fertilizer_products.create_index("price_per_kg")
        
        # Crop recommendations
        await db_manager.db.crop_recommendations.create_index("user_id")
        
        # Soil reference
        await db_manager.db.soil_reference.create_index([("state", 1), ("district", 1)])
        
        # Weather alerts
        await db_manager.db.weather_alerts.create_index("created_at")
        
        logger.info("MongoDB indexes verified/created successfully.")
        await seed_demo_users_if_needed()
    except Exception as e:
        logger.warning(f"Could not initialize database indexes: {e}")

async def seed_demo_users_if_needed():
    """Seed baseline demo accounts for Farmer, Expert, and Admin if not present."""
    if not db_manager.is_connected or db_manager.db is None:
        return
    try:
        from datetime import datetime, timezone
        demo_users = [
            {
                "full_name": "Ramesh Patel (Farmer)",
                "email": "farmer@agrisaathi.org",
                "password_hash": "$2b$12$mqUCz8PH7NWk0eEkfmM3Vuy8i3RDt4yR8eO7/NEkXQgWpMUZFHrOu",
                "phone_number": "9876543210",
                "role": "farmer",
                "village_district": "Ludhiana",
                "state": "Punjab",
                "created_at": datetime.now(timezone.utc),
                "is_active": True
            },
            {
                "full_name": "Dr. Anita Sharma (Plant Pathologist)",
                "email": "expert@agrisaathi.org",
                "password_hash": "$2b$12$BJLRszSWlaZJjLosbMdRo.ntSwcrp/8b2lEzYwf6aHKuGs5jJP93e",
                "phone_number": "9876543211",
                "role": "expert",
                "village_district": "Krishi Vigyan Kendra",
                "state": "Maharashtra",
                "created_at": datetime.now(timezone.utc),
                "is_active": True
            },
            {
                "full_name": "System Administrator",
                "email": "admin@agrisaathi.org",
                "password_hash": "$2b$12$7/3LrjkXDrdGPBROBpmdlOjrpZH3NK67czweas1DKcWqQj2JPEKG6",
                "phone_number": "9876543212",
                "role": "admin",
                "village_district": "Central Agritech Hub",
                "state": "Delhi",
                "created_at": datetime.now(timezone.utc),
                "is_active": True
            }
        ]
        for user in demo_users:
            exists = await db_manager.db.users.find_one({"email": user["email"]})
            if not exists:
                await db_manager.db.users.insert_one(user)
        logger.info("Demo evaluator accounts verified in database.")
    except Exception as e:
        logger.warning(f"Could not seed demo users: {e}")

def get_database() -> Optional[AsyncIOMotorDatabase]:
    return db_manager.db

