from typing import Generic, TypeVar, Type, Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import Base
import logging

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository class with common CRUD operations"""

    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def create(self, obj_data: Dict[str, Any]) -> ModelType:
        """Create a new record"""
        try:
            db_obj = self.model(**obj_data)
            self.db.add(db_obj)
            self.db.commit()
            self.db.refresh(db_obj)
            logger.info(f"Created {self.model.__name__} with id: {db_obj.id}")
            return db_obj
        except SQLAlchemyError as e:
            logger.error(f"Error creating {self.model.__name__}: {e}")
            self.db.rollback()
            raise

    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get a record by ID"""
        try:
            return self.db.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error getting {self.model.__name__} by id {id}: {e}")
            raise

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all records with pagination"""
        try:
            return self.db.query(self.model).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting all {self.model.__name__}: {e}")
            raise

    def update(self, id: int, obj_data: Dict[str, Any]) -> Optional[ModelType]:
        """Update a record by ID"""
        try:
            db_obj = self.get_by_id(id)
            if not db_obj:
                return None
            
            for field, value in obj_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            
            self.db.commit()
            self.db.refresh(db_obj)
            logger.info(f"Updated {self.model.__name__} with id: {id}")
            return db_obj
        except SQLAlchemyError as e:
            logger.error(f"Error updating {self.model.__name__} with id {id}: {e}")
            self.db.rollback()
            raise

    def delete(self, id: int) -> bool:
        """Delete a record by ID"""
        try:
            db_obj = self.get_by_id(id)
            if not db_obj:
                return False
            
            self.db.delete(db_obj)
            self.db.commit()
            logger.info(f"Deleted {self.model.__name__} with id: {id}")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error deleting {self.model.__name__} with id {id}: {e}")
            self.db.rollback()
            raise

    def get_by_field(self, field: str, value: Any) -> Optional[ModelType]:
        """Get a record by a specific field"""
        try:
            return self.db.query(self.model).filter(getattr(self.model, field) == value).first()
        except SQLAlchemyError as e:
            logger.error(f"Error getting {self.model.__name__} by {field}: {e}")
            raise

    def get_many_by_field(self, field: str, value: Any, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get multiple records by a specific field"""
        try:
            return (
                self.db.query(self.model)
                .filter(getattr(self.model, field) == value)
                .offset(skip)
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting {self.model.__name__} by {field}: {e}")
            raise

    def count(self) -> int:
        """Count total records"""
        try:
            return self.db.query(self.model).count()
        except SQLAlchemyError as e:
            logger.error(f"Error counting {self.model.__name__}: {e}")
            raise

    def exists(self, id: int) -> bool:
        """Check if a record exists by ID"""
        try:
            return self.db.query(self.model).filter(self.model.id == id).first() is not None
        except SQLAlchemyError as e:
            logger.error(f"Error checking existence of {self.model.__name__} with id {id}: {e}")
            raise