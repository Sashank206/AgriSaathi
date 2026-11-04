from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime, timezone
from bson import ObjectId
import uuid
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from app.database.mongodb import get_database, db_manager
from app.middleware.auth_middleware import get_current_user, _mock_users_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate):
    db = get_database()
    
    # Check if user already exists
    if db_manager.is_connected and db is not None:
        existing = await db.users.find_one({"email": user_in.email.lower()})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email address already exists. Please log in."
            )
    else:
        # Check mock store
        for u in _mock_users_db.values():
            if u["email"].lower() == user_in.email.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A user with this email address already exists. Please log in."
                )

    hashed_pw = get_password_hash(user_in.password)
    user_doc = {
        "full_name": user_in.full_name,
        "email": user_in.email.lower(),
        "password_hash": hashed_pw,
        "phone_number": user_in.phone_number,
        "role": user_in.role.value if hasattr(user_in.role, "value") else str(user_in.role),
        "village_district": user_in.village_district,
        "state": user_in.state,
        "created_at": datetime.now(timezone.utc),
        "is_active": True
    }

    if db_manager.is_connected and db is not None:
        result = await db.users.insert_one(user_doc)
        user_id = str(result.inserted_id)
    else:
        user_id = str(uuid.uuid4())
        user_doc["_id"] = user_id
        _mock_users_db[user_id] = user_doc

    token = create_access_token({"sub": user_id, "role": user_doc["role"], "email": user_doc["email"]})
    
    response_user = UserResponse(
        id=user_id,
        full_name=user_doc["full_name"],
        email=user_doc["email"],
        phone_number=user_doc["phone_number"],
        role=user_doc["role"],
        village_district=user_doc["village_district"],
        state=user_doc["state"],
        created_at=user_doc["created_at"],
        is_active=True
    )
    return Token(access_token=token, user=response_user)

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    email = credentials.email.lower()
    user = None
    db = get_database()
    
    if db_manager.is_connected and db is not None:
        user = await db.users.find_one({"email": email})
    
    if not user:
        for u in _mock_users_db.values():
            if u["email"].lower() == email:
                user = u
                break
                
    if not user or not verify_password(credentials.password, user.get("password_hash", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password. Please verify your credentials."
        )

    user_id = str(user.get("_id", user.get("id")))
    token = create_access_token({"sub": user_id, "role": user["role"], "email": user["email"]})

    response_user = UserResponse(
        id=user_id,
        full_name=user["full_name"],
        email=user["email"],
        phone_number=user["phone_number"],
        role=user["role"],
        village_district=user["village_district"],
        state=user["state"],
        created_at=user.get("created_at", datetime.now(timezone.utc)),
        is_active=user.get("is_active", True)
    )
    return Token(access_token=token, user=response_user)

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user.get("_id", current_user.get("id")))
    return UserResponse(
        id=user_id,
        full_name=current_user["full_name"],
        email=current_user["email"],
        phone_number=current_user["phone_number"],
        role=current_user["role"],
        village_district=current_user["village_district"],
        state=current_user["state"],
        created_at=current_user.get("created_at", datetime.now(timezone.utc)),
        is_active=current_user.get("is_active", True)
    )

