from pydantic import BaseModel, field_validator, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from app.models.order import OrderStatus


class OrderItemBase(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., gt=0, decimal_places=2)
    total_price: Decimal = Field(..., gt=0, decimal_places=2)




class OrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class OrderBase(BaseModel):
    delivery_address_id: int = Field(..., gt=0)
    total_amount: Decimal = Field(..., gt=0, decimal_places=2)
    tax_amount: Decimal = Field(default=Decimal('0.00'), ge=0, decimal_places=2)
    shipping_cost: Decimal = Field(default=Decimal('0.00'), ge=0, decimal_places=2)
    estimated_delivery_date: Optional[datetime] = None
    notes: Optional[str] = None


class OrderCreate(BaseModel):
    delivery_address_id: int = Field(..., gt=0)
    items: List[OrderItemCreate] = Field(..., min_length=1)
    notes: Optional[str] = None

    @field_validator('items')
    @classmethod
    def validate_items(cls, v):
        if not v:
            raise ValueError('Order must contain at least one item')
        return v


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    estimated_delivery_date: Optional[datetime] = None
    actual_delivery_date: Optional[datetime] = None
    notes: Optional[str] = None


class OrderResponse(OrderBase):
    id: int
    order_number: str
    user_id: int
    status: OrderStatus
    actual_delivery_date: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    order_items: List[OrderItemResponse] = []

    model_config = {"from_attributes": True}