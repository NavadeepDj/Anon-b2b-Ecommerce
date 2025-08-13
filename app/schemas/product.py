from pydantic import BaseModel, field_validator, model_validator, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    sku: str = Field(..., min_length=3, max_length=100)
    retail_price: Decimal = Field(..., gt=0, decimal_places=2)
    company_price: Decimal = Field(..., gt=0, decimal_places=2)
    stock_quantity: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True)
    weight_kg: Optional[Decimal] = Field(None, gt=0, decimal_places=3)
    dimensions: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=100)

    @field_validator('sku')
    @classmethod
    def validate_sku(cls, v):
        if not v or not v.strip():
            raise ValueError('SKU cannot be empty')
        return v.strip().upper()

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Product name cannot be empty')
        return v.strip()

    @model_validator(mode='after')
    def validate_pricing(self):
        if self.company_price >= self.retail_price:
            raise ValueError('Company price must be less than retail price')
        return self


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    retail_price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    company_price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    stock_quantity: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None
    weight_kg: Optional[Decimal] = Field(None, gt=0, decimal_places=3)
    dimensions: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=100)


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}