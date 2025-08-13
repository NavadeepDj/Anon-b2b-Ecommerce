from pydantic import BaseModel, field_validator, Field
from typing import Optional
from datetime import datetime


class AddressBase(BaseModel):
    address_line_1: str = Field(..., min_length=5, max_length=255)
    address_line_2: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    postal_code: str = Field(..., pattern=r'^\d{6}$')
    country: str = Field(default="India", max_length=100)
    is_default: bool = Field(default=False)

    @field_validator('postal_code')
    @classmethod
    def validate_postal_code(cls, v):
        if not v or len(v) != 6 or not v.isdigit():
            raise ValueError('Postal code must be exactly 6 digits')
        return v

    @field_validator('city', 'state')
    @classmethod
    def validate_text_fields(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip().title()


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    address_line_1: Optional[str] = Field(None, min_length=5, max_length=255)
    address_line_2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, min_length=2, max_length=100)
    state: Optional[str] = Field(None, min_length=2, max_length=100)
    postal_code: Optional[str] = Field(None, pattern=r'^\d{6}$')
    country: Optional[str] = Field(None, max_length=100)
    is_default: Optional[bool] = None


class AddressResponse(AddressBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}