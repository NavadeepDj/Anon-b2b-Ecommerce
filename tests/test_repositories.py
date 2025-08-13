import pytest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.user import User, BusinessType
from app.models.address import Address
from app.models.product import Product
from app.models.order import Order, OrderItem, OrderStatus
from app.repositories.user import UserRepository
from app.repositories.address import AddressRepository
from app.repositories.product import ProductRepository
from app.repositories.order import OrderRepository, OrderItemRepository


# Test database setup
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "phone": "+919876543210",
        "hashed_password": "hashed_password_123",
        "business_name": "Test Business",
        "gstin": "29ABCDE1234F1Z5",
        "business_type": BusinessType.RETAIL_STORE,
        "is_active": True,
        "is_verified": False
    }


@pytest.fixture
def sample_product_data():
    """Sample product data for testing"""
    return {
        "name": "Test Product",
        "description": "A test product",
        "sku": "TEST001",
        "retail_price": Decimal("100.00"),
        "company_price": Decimal("80.00"),
        "stock_quantity": 50,
        "is_active": True,
        "weight_kg": Decimal("1.500"),
        "category": "Electronics"
    }


class TestUserRepository:
    """Test UserRepository functionality"""

    def test_create_user(self, db_session, sample_user_data):
        """Test creating a new user"""
        user_repo = UserRepository(db_session)
        user = user_repo.create(sample_user_data)
        
        assert user.id is not None
        assert user.email == sample_user_data["email"]
        assert user.business_type == BusinessType.RETAIL_STORE
        assert user.is_active is True
        assert user.is_verified is False

    def test_get_user_by_email(self, db_session, sample_user_data):
        """Test getting user by email"""
        user_repo = UserRepository(db_session)
        created_user = user_repo.create(sample_user_data)
        
        found_user = user_repo.get_by_email(sample_user_data["email"])
        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.email == sample_user_data["email"]

    def test_get_user_by_gstin(self, db_session, sample_user_data):
        """Test getting user by GSTIN"""
        user_repo = UserRepository(db_session)
        created_user = user_repo.create(sample_user_data)
        
        found_user = user_repo.get_by_gstin(sample_user_data["gstin"])
        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.gstin == sample_user_data["gstin"]

    def test_verify_user(self, db_session, sample_user_data):
        """Test verifying a user"""
        user_repo = UserRepository(db_session)
        user = user_repo.create(sample_user_data)
        
        verified_user = user_repo.verify_user(user.id)
        assert verified_user is not None
        assert verified_user.is_verified is True

    def test_get_users_by_business_type(self, db_session, sample_user_data):
        """Test getting users by business type"""
        user_repo = UserRepository(db_session)
        user_repo.create(sample_user_data)
        
        # Create a company user
        company_data = sample_user_data.copy()
        company_data["email"] = "company@example.com"
        company_data["phone"] = "+919876543211"  # Different phone number
        company_data["gstin"] = "29ABCDE1234F2Z5"
        company_data["business_type"] = BusinessType.COMPANY
        user_repo.create(company_data)
        
        retail_users = user_repo.get_by_business_type(BusinessType.RETAIL_STORE)
        company_users = user_repo.get_by_business_type(BusinessType.COMPANY)
        
        assert len(retail_users) == 1
        assert len(company_users) == 1
        assert retail_users[0].business_type == BusinessType.RETAIL_STORE
        assert company_users[0].business_type == BusinessType.COMPANY


class TestProductRepository:
    """Test ProductRepository functionality"""

    def test_create_product(self, db_session, sample_product_data):
        """Test creating a new product"""
        product_repo = ProductRepository(db_session)
        product = product_repo.create(sample_product_data)
        
        assert product.id is not None
        assert product.name == sample_product_data["name"]
        assert product.sku == sample_product_data["sku"]
        assert product.retail_price == sample_product_data["retail_price"]
        assert product.company_price == sample_product_data["company_price"]

    def test_get_product_by_sku(self, db_session, sample_product_data):
        """Test getting product by SKU"""
        product_repo = ProductRepository(db_session)
        created_product = product_repo.create(sample_product_data)
        
        found_product = product_repo.get_by_sku(sample_product_data["sku"])
        assert found_product is not None
        assert found_product.id == created_product.id
        assert found_product.sku == sample_product_data["sku"]

    def test_update_stock(self, db_session, sample_product_data):
        """Test updating product stock"""
        product_repo = ProductRepository(db_session)
        product = product_repo.create(sample_product_data)
        
        # Increase stock
        updated_product = product_repo.update_stock(product.id, 10)
        assert updated_product.stock_quantity == 60  # 50 + 10
        
        # Decrease stock
        updated_product = product_repo.update_stock(product.id, -20)
        assert updated_product.stock_quantity == 40  # 60 - 20

    def test_get_in_stock_products(self, db_session, sample_product_data):
        """Test getting products that are in stock"""
        product_repo = ProductRepository(db_session)
        
        # Create in-stock product
        product_repo.create(sample_product_data)
        
        # Create out-of-stock product
        out_of_stock_data = sample_product_data.copy()
        out_of_stock_data["sku"] = "TEST002"
        out_of_stock_data["stock_quantity"] = 0
        product_repo.create(out_of_stock_data)
        
        in_stock_products = product_repo.get_in_stock_products()
        assert len(in_stock_products) == 1
        assert in_stock_products[0].stock_quantity > 0


class TestAddressRepository:
    """Test AddressRepository functionality"""

    def test_create_address(self, db_session, sample_user_data):
        """Test creating a new address"""
        user_repo = UserRepository(db_session)
        user = user_repo.create(sample_user_data)
        
        address_repo = AddressRepository(db_session)
        address_data = {
            "user_id": user.id,
            "address_line_1": "123 Main Street",
            "city": "Nellore",
            "state": "Andhra Pradesh",
            "postal_code": "524001",
            "country": "India",
            "is_default": True
        }
        
        address = address_repo.create(address_data)
        assert address.id is not None
        assert address.user_id == user.id
        assert address.city == "Nellore"
        assert address.is_default is True

    def test_get_user_addresses(self, db_session, sample_user_data):
        """Test getting addresses for a user"""
        user_repo = UserRepository(db_session)
        user = user_repo.create(sample_user_data)
        
        address_repo = AddressRepository(db_session)
        
        # Create multiple addresses
        for i in range(3):
            address_data = {
                "user_id": user.id,
                "address_line_1": f"Address {i+1}",
                "city": "Nellore",
                "state": "Andhra Pradesh",
                "postal_code": "524001",
                "country": "India",
                "is_default": i == 0  # First address is default
            }
            address_repo.create(address_data)
        
        addresses = address_repo.get_user_addresses(user.id)
        assert len(addresses) == 3
        assert addresses[0].is_default is True  # Default address should be first


class TestOrderRepository:
    """Test OrderRepository functionality"""

    def test_create_order(self, db_session, sample_user_data, sample_product_data):
        """Test creating a new order"""
        # Create user and product first
        user_repo = UserRepository(db_session)
        user = user_repo.create(sample_user_data)
        
        product_repo = ProductRepository(db_session)
        product = product_repo.create(sample_product_data)
        
        # Create address
        address_repo = AddressRepository(db_session)
        address_data = {
            "user_id": user.id,
            "address_line_1": "123 Main Street",
            "city": "Nellore",
            "state": "Andhra Pradesh",
            "postal_code": "524001",
            "country": "India",
            "is_default": True
        }
        address = address_repo.create(address_data)
        
        # Create order
        order_repo = OrderRepository(db_session)
        order_data = {
            "order_number": "ORD001",
            "user_id": user.id,
            "delivery_address_id": address.id,
            "status": OrderStatus.PENDING,
            "total_amount": Decimal("200.00"),
            "tax_amount": Decimal("20.00"),
            "shipping_cost": Decimal("10.00")
        }
        
        order = order_repo.create(order_data)
        assert order.id is not None
        assert order.order_number == "ORD001"
        assert order.user_id == user.id
        assert order.status == OrderStatus.PENDING

    def test_update_order_status(self, db_session, sample_user_data, sample_product_data):
        """Test updating order status"""
        # Setup data
        user_repo = UserRepository(db_session)
        user = user_repo.create(sample_user_data)
        
        address_repo = AddressRepository(db_session)
        address_data = {
            "user_id": user.id,
            "address_line_1": "123 Main Street",
            "city": "Nellore",
            "state": "Andhra Pradesh",
            "postal_code": "524001",
            "country": "India"
        }
        address = address_repo.create(address_data)
        
        order_repo = OrderRepository(db_session)
        order_data = {
            "order_number": "ORD001",
            "user_id": user.id,
            "delivery_address_id": address.id,
            "status": OrderStatus.PENDING,
            "total_amount": Decimal("200.00")
        }
        order = order_repo.create(order_data)
        
        # Update status
        updated_order = order_repo.update_status(order.id, OrderStatus.CONFIRMED)
        assert updated_order.status == OrderStatus.CONFIRMED
        
        # Update to delivered should set actual delivery date
        delivered_order = order_repo.update_status(order.id, OrderStatus.DELIVERED)
        assert delivered_order.status == OrderStatus.DELIVERED
        assert delivered_order.actual_delivery_date is not None