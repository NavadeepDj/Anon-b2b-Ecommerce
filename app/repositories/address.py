from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.address import Address
from app.repositories.base import BaseRepository
import logging

logger = logging.getLogger(__name__)


class AddressRepository(BaseRepository[Address]):
    """Address-specific repository with additional methods"""

    def __init__(self, db: Session):
        super().__init__(Address, db)

    def get_user_addresses(self, user_id: int) -> List[Address]:
        """Get all addresses for a specific user"""
        try:
            return (
                self.db.query(Address)
                .filter(Address.user_id == user_id)
                .order_by(Address.is_default.desc(), Address.created_at.desc())
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting addresses for user {user_id}: {e}")
            raise

    def get_default_address(self, user_id: int) -> Optional[Address]:
        """Get the default address for a user"""
        try:
            return (
                self.db.query(Address)
                .filter(Address.user_id == user_id)
                .filter(Address.is_default == True)
                .first()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting default address for user {user_id}: {e}")
            raise

    def set_default_address(self, user_id: int, address_id: int) -> Optional[Address]:
        """Set an address as default for a user"""
        try:
            # First, unset all default addresses for the user
            self.db.query(Address).filter(
                Address.user_id == user_id,
                Address.is_default == True
            ).update({"is_default": False})

            # Then set the specified address as default
            address = self.get_by_id(address_id)
            if address and address.user_id == user_id:
                address.is_default = True
                self.db.commit()
                self.db.refresh(address)
                logger.info(f"Set address {address_id} as default for user {user_id}")
                return address
            else:
                logger.warning(f"Address {address_id} not found or doesn't belong to user {user_id}")
                return None
        except SQLAlchemyError as e:
            logger.error(f"Error setting default address {address_id} for user {user_id}: {e}")
            self.db.rollback()
            raise

    def get_addresses_by_city(self, city: str, skip: int = 0, limit: int = 100) -> List[Address]:
        """Get addresses by city"""
        try:
            return (
                self.db.query(Address)
                .filter(Address.city.ilike(f"%{city}%"))
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting addresses by city {city}: {e}")
            raise

    def get_addresses_by_state(self, state: str, skip: int = 0, limit: int = 100) -> List[Address]:
        """Get addresses by state"""
        try:
            return (
                self.db.query(Address)
                .filter(Address.state.ilike(f"%{state}%"))
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting addresses by state {state}: {e}")
            raise

    def get_addresses_by_postal_code(self, postal_code: str) -> List[Address]:
        """Get addresses by postal code"""
        try:
            return (
                self.db.query(Address)
                .filter(Address.postal_code == postal_code)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting addresses by postal code {postal_code}: {e}")
            raise

    def delete_user_address(self, user_id: int, address_id: int) -> bool:
        """Delete a specific address for a user"""
        try:
            address = self.get_by_id(address_id)
            if address and address.user_id == user_id:
                self.db.delete(address)
                self.db.commit()
                logger.info(f"Deleted address {address_id} for user {user_id}")
                return True
            else:
                logger.warning(f"Address {address_id} not found or doesn't belong to user {user_id}")
                return False
        except SQLAlchemyError as e:
            logger.error(f"Error deleting address {address_id} for user {user_id}: {e}")
            self.db.rollback()
            raise