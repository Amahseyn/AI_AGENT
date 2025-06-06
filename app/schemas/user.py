from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
import re

# ---------------------------
# Shared/User Base Schema
# ---------------------------

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

    @field_validator('username')
    def validate_username(cls, value):
        if not re.match(r'^[\w.@+-]+$', value):
            raise ValueError('Username contains invalid characters')
        return value


# ---------------------------
# Create User Schema
# ---------------------------

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

    @field_validator('password')
    def validate_password(cls, value):
        # You can add more complex rules here (e.g., uppercase + number requirement)
        return value


# ---------------------------
# Update User Schema (Optional Fields)
# ---------------------------

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None

    @field_validator('username')
    def validate_username(cls, value):
        if value and not re.match(r'^[\w.@+-]+$', value):
            raise ValueError('Username contains invalid characters')
        return value


# ---------------------------
# Response Schema for User
# ---------------------------

class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        from_attributes = True  # For compatibility with SQLAlchemy models


# ---------------------------
# Token Schemas
# ---------------------------

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    exp: Optional[int] = None


# ---------------------------
# Login Schema
# ---------------------------

class UserLogin(BaseModel):
    username: str
    password: str

