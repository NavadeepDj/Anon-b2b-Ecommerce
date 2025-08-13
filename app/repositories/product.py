from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.product import Product
from app.repositories.base import BaseRepository
import logging

logger = logging.getLogger(__name__)


class ProductRepository(BaseRepository[Product]):
    """Product-specific repository with additional methods"""

    def __init__(self, db: Session):
        super().__init__(Product, db)

    def get_by_sku(self, sku: str) -> Optional[Product]:
        """Get product by SKU"""
        try:
            return self.db.query(Product).filter(Product.sku == sku).first()
        except SQLAlchemyError as e:
            logger.error(f"Error getting product by SKU {sku}: {e}")
            raise

    def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get products by category"""
        try:
            return (
                self.db.query(Product)
                .filter(Product.category == category)
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting products by category {category}: {e}")
            raise

    def get_active_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get active products"""
        try:
            return (
                self.db.query(Product)
                .filter(Product.is_active == True)
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting active products: {e}")
            raise

    def get_in_stock_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get products that are in stock"""
        try:
            return (
                self.db.query(Product)
                .filter(Product.stock_quantity > 0)
                .filter(Product.is_active == True)
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting in-stock products: {e}")
            raise

    def get_low_stock_products(self, threshold: int = 10, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get products with low stock"""
        try:
            return (
                self.db.query(Product)
                .filter(Product.stock_quantity <= threshold)
                .filter(Product.stock_quantity > 0)
                .filter(Product.is_active == True)
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting low stock products: {e}")
            raise

    def search_products(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Product]:
        """Search products by name, description, or SKU"""
        try:
            return (
                self.db.query(Product)
                .filter(
                    (Product.name.ilike(f"%{search_term}%")) |
                    (Product.description.ilike(f"%{search_term}%")) |
                    (Product.sku.ilike(f"%{search_term}%"))
                )
                .filter(Product.is_active == True)
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error searching products with term {search_term}: {e}")
            raise

    def update_stock(self, product_id: int, quantity_change: int) -> Optional[Product]:
        """Update product stock quantity"""
        try:
            product = self.get_by_id(product_id)
            if product:
                new_quantity = product.stock_quantity + quantity_change
                if new_quantity < 0:
                    raise ValueError("Stock quantity cannot be negative")
                
                product.stock_quantity = new_quantity
                self.db.commit()
                self.db.refresh(product)
                logger.info(f"Updated stock for product {product_id}: {quantity_change}")
            return product
        except SQLAlchemyError as e:
            logger.error(f"Error updating stock for product {product_id}: {e}")
            self.db.rollback()
            raise

    def get_categories(self) -> List[str]:
        """Get all unique product categories"""
        try:
            result = self.db.query(Product.category).filter(Product.category.isnot(None)).distinct().all()
            return [category[0] for category in result if category[0]]
        except SQLAlchemyError as e:
            logger.error(f"Error getting product categories: {e}")
            raise