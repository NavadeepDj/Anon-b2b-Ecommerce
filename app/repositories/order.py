from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
from app.models.order import Order, OrderItem, OrderStatus
from app.repositories.base import BaseRepository
import logging

logger = logging.getLogger(__name__)


class OrderRepository(BaseRepository[Order]):
    """Order-specific repository with additional methods"""

    def __init__(self, db: Session):
        super().__init__(Order, db)

    def get_by_order_number(self, order_number: str) -> Optional[Order]:
        """Get order by order number"""
        try:
            return (
                self.db.query(Order)
                .options(joinedload(Order.order_items))
                .filter(Order.order_number == order_number)
                .first()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting order by number {order_number}: {e}")
            raise

    def get_user_orders(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get orders for a specific user"""
        try:
            return (
                self.db.query(Order)
                .options(joinedload(Order.order_items))
                .filter(Order.user_id == user_id)
                .order_by(Order.created_at.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting orders for user {user_id}: {e}")
            raise

    def get_by_status(self, status: OrderStatus, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get orders by status"""
        try:
            return (
                self.db.query(Order)
                .options(joinedload(Order.order_items))
                .filter(Order.status == status)
                .order_by(Order.created_at.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting orders by status {status}: {e}")
            raise

    def get_orders_by_date_range(self, start_date: datetime, end_date: datetime, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get orders within a date range"""
        try:
            return (
                self.db.query(Order)
                .options(joinedload(Order.order_items))
                .filter(Order.created_at >= start_date)
                .filter(Order.created_at <= end_date)
                .order_by(Order.created_at.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting orders by date range: {e}")
            raise

    def update_status(self, order_id: int, status: OrderStatus) -> Optional[Order]:
        """Update order status"""
        try:
            order = self.get_by_id(order_id)
            if order:
                order.status = status
                if status == OrderStatus.DELIVERED:
                    order.actual_delivery_date = datetime.now(timezone.utc)
                
                self.db.commit()
                self.db.refresh(order)
                logger.info(f"Updated order {order_id} status to {status}")
            return order
        except SQLAlchemyError as e:
            logger.error(f"Error updating order {order_id} status: {e}")
            self.db.rollback()
            raise

    def get_pending_orders(self, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get pending orders"""
        return self.get_by_status(OrderStatus.PENDING, skip, limit)

    def get_overdue_orders(self, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get orders that are overdue for delivery"""
        try:
            current_time = datetime.now(timezone.utc)
            return (
                self.db.query(Order)
                .options(joinedload(Order.order_items))
                .filter(Order.estimated_delivery_date < current_time)
                .filter(Order.status.in_([OrderStatus.CONFIRMED, OrderStatus.PROCESSING, OrderStatus.SHIPPED]))
                .order_by(Order.estimated_delivery_date.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting overdue orders: {e}")
            raise


class OrderItemRepository(BaseRepository[OrderItem]):
    """OrderItem-specific repository with additional methods"""

    def __init__(self, db: Session):
        super().__init__(OrderItem, db)

    def get_by_order_id(self, order_id: int) -> List[OrderItem]:
        """Get all items for a specific order"""
        try:
            return (
                self.db.query(OrderItem)
                .filter(OrderItem.order_id == order_id)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting order items for order {order_id}: {e}")
            raise

    def get_by_product_id(self, product_id: int, skip: int = 0, limit: int = 100) -> List[OrderItem]:
        """Get all order items for a specific product"""
        try:
            return (
                self.db.query(OrderItem)
                .filter(OrderItem.product_id == product_id)
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting order items for product {product_id}: {e}")
            raise