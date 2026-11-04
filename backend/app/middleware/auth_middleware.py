from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from bson import ObjectId
from app.core.security import decode_access_token
from app.database.mongodb import get_database, db_manager
from app.schemas.user import UserRole

security_scheme = HTTPBearer(auto_error=False)

# In-memory store fallback for development/demo when MongoDB is not running locally
_mock_users_db = {
    "demo-farmer-id": {
        "_id": "demo-farmer-id",
        "id": "demo-farmer-id",
        "full_name": "Ramesh Patel (Farmer)",
        "email": "farmer@agrisaathi.org",
        "password_hash": "$2b$12$mqUCz8PH7NWk0eEkfmM3Vuy8i3RDt4yR8eO7/NEkXQgWpMUZFHrOu",
        "phone_number": "9876543210",
        "role": "farmer",
        "village_district": "Ludhiana",
        "state": "Punjab",
        "is_active": True
    },
    "demo-expert-id": {
        "_id": "demo-expert-id",
        "id": "demo-expert-id",
        "full_name": "Dr. Anita Sharma (Plant Pathologist)",
        "email": "expert@agrisaathi.org",
        "password_hash": "$2b$12$BJLRszSWlaZJjLosbMdRo.ntSwcrp/8b2lEzYwf6aHKuGs5jJP93e",
        "phone_number": "9876543211",
        "role": "expert",
        "village_district": "Krishi Vigyan Kendra",
        "state": "Maharashtra",
        "is_active": True
    },
    "demo-admin-id": {
        "_id": "demo-admin-id",
        "id": "demo-admin-id",
        "full_name": "System Administrator",
        "email": "admin@agrisaathi.org",
        "password_hash": "$2b$12$7/3LrjkXDrdGPBROBpmdlOjrpZH3NK67czweas1DKcWqQj2JPEKG6",
        "phone_number": "9876543212",
        "role": "admin",
        "village_district": "Central Agritech Hub",
        "state": "Delhi",
        "is_active": True
    }
}

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme)
) -> dict:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is missing. Please log in.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid, expired or tampered session token. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Try fetching from MongoDB
    db = get_database()
    if db_manager.is_connected and db is not None:
        try:
            user = await db.users.find_one({"_id": ObjectId(user_id)})
            if user:
                user["id"] = str(user["_id"])
                return user
        except Exception:
            pass
    
    # Check in-memory mock store
    if user_id in _mock_users_db:
        return _mock_users_db[user_id]
        
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User corresponding to token was not found.",
        headers={"WWW-Authenticate": "Bearer"},
    )

def require_role(allowed_roles: List[UserRole]):
    async def role_checker(current_user: dict = Depends(get_current_user)) -> dict:
        user_role = current_user.get("role")
        role_values = [r.value if isinstance(r, UserRole) else str(r) for r in allowed_roles]
        if user_role not in role_values:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: requires one of the following roles: {role_values}",
            )
        return current_user
    return role_checker

