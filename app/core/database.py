from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Create SQLAlchemy engine with connection pooling
# Note: Using postgresql+asyncpg for async support, fallback to sqlite for development
try:
    # Convert postgresql:// to postgresql+asyncpg:// for asyncpg driver
    database_url = settings.DATABASE_URL
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    
    engine = create_engine(
        database_url,
        poolclass=QueuePool,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=settings.DEBUG
    )
except Exception as e:
    logger.warning(f"Failed to create PostgreSQL engine: {e}")
    logger.info("Falling back to SQLite for development")
    engine = create_engine(
        "sqlite:///./anon_b2b.db",
        connect_args={"check_same_thread": False},
        echo=settings.DEBUG
    )

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """
    Initialize database tables
    """
    try:
        # Import models to ensure they're registered with Base
        from app.models import User, Address, Product, Order, OrderItem
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise