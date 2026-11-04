from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    FARMER = "farmer"
    ADMIN = "admin"
    EXPERT = "expert"

class UserBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone_number: str = Field(..., min_length=10, max_length=15)
    role: UserRole = UserRole.FARMER
    village_district: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: str
    created_at: datetime
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
    email: Optional[str] = None
