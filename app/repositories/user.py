from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User, BusinessType
from app.repositories.base import BaseRepository
import logging

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository[User]):
    """User-specific repository with additional methods"""

    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            return self.db.query(User).filter(User.email == email).first()
        except SQLAlchemyError as e:
            logger.error(f"Error getting user by email {email}: {e}")
            raise

    def get_by_gstin(self, gstin: str) -> Optional[User]:
        """Get user by GSTIN"""
        try:
            return self.db.query(User).filter(User.gstin == gstin).first()
        except SQLAlchemyError as e:
            logger.error(f"Error getting user by GSTIN {gstin}: {e}")
            raise

    def get_by_phone(self, phone: str) -> Optional[User]:
        """Get user by phone number"""
        try:
            return self.db.query(User).filter(User.phone == phone).first()
        except SQLAlchemyError as e:
            logger.error(f"Error getting user by phone {phone}: {e}")
            raise

    def get_by_business_type(self, business_type: BusinessType, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users by business type"""
        try:
            return (
                self.db.query(User)
                .filter(User.business_type == business_type)
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting users by business type {business_type}: {e}")
            raise

    def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get active users"""
        try:
            return (
                self.db.query(User)
                .filter(User.is_active == True)
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting active users: {e}")
            raise

    def get_verified_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get verified users"""
        try:
            return (
                self.db.query(User)
                .filter(User.is_verified == True)
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting verified users: {e}")
            raise

    def verify_user(self, user_id: int) -> Optional[User]:
        """Mark user as verified"""
        try:
            user = self.get_by_id(user_id)
            if user:
                user.is_verified = True
                self.db.commit()
                self.db.refresh(user)
                logger.info(f"User {user_id} verified successfully")
            return user
        except SQLAlchemyError as e:
            logger.error(f"Error verifying user {user_id}: {e}")
            self.db.rollback()
            raise

    def deactivate_user(self, user_id: int) -> Optional[User]:
        """Deactivate user"""
        try:
            user = self.get_by_id(user_id)
            if user:
                user.is_active = False
                self.db.commit()
                self.db.refresh(user)
                logger.info(f"User {user_id} deactivated successfully")
            return user
        except SQLAlchemyError as e:
            logger.error(f"Error deactivating user {user_id}: {e}")
            self.db.rollback()
            raise

    def search_users(self, search_term: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Search users by business name or email"""
        try:
            return (
                self.db.query(User)
                .filter(
                    (User.business_name.ilike(f"%{search_term}%")) |
                    (User.email.ilike(f"%{search_term}%"))
                )
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error searching users with term {search_term}: {e}")
            raise