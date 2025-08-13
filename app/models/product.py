from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.types import Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    sku = Column(String(100), unique=True, index=True, nullable=False)
    retail_price = Column(Numeric(10, 2), nullable=False)
    company_price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True)
    weight_kg = Column(Numeric(8, 3), nullable=True)
    dimensions = Column(String(100), nullable=True)  # Format: "LxWxH in cm"
    category = Column(String(100), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    order_items = relationship("OrderItem", back_populates="product")