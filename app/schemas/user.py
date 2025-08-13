from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional, List
from datetime import datetime
from app.models.user import BusinessType


class UserBase(BaseModel):
    email: EmailStr
    phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{1,14}$')
    business_name: str = Field(..., min_length=2, max_length=255)
    gstin: str = Field(..., pattern=r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$')
    business_type: BusinessType

    @field_validator('gstin')
    @classmethod
    def validate_gstin(cls, v):
        if not v or len(v) != 15:
            raise ValueError('GSTIN must be exactly 15 characters')
        return v.upper()

    @field_validator('business_name')
    @classmethod
    def validate_business_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Business name cannot be empty')
        return v.strip()


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{1,14}$')
    business_name: Optional[str] = Field(None, min_length=2, max_length=255)
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr
    password: str