import pytest
from decimal import Decimal
from pydantic import ValidationError
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.schemas.address import AddressCreate, AddressUpdate
from app.schemas.product import ProductCreate, ProductUpdate
from app.schemas.order import OrderCreate, OrderItemCreate
from app.models.user import BusinessType


class TestUserSchemas:
    """Test user Pydantic model validation"""

    def test_user_create_valid(self):
        """Test valid user creation"""
        user_data = {
            "email": "test@example.com",
            "phone": "+919876543210",
            "business_name": "Test Business",
            "gstin": "29ABCDE1234F1Z5",
            "business_type": BusinessType.RETAIL_STORE,
            "password": "SecurePass123"
        }
        user = UserCreate(**user_data)
        assert user.email == "test@example.com"
        assert user.gstin == "29ABCDE1234F1Z5"
        assert user.business_type == BusinessType.RETAIL_STORE

    def test_user_create_invalid_email(self):
        """Test user creation with invalid email"""
        user_data = {
            "email": "invalid-email",
            "business_name": "Test Business",
            "gstin": "29ABCDE1234F1Z5",
            "business_type": BusinessType.RETAIL_STORE,
            "password": "SecurePass123"
        }
        with pytest.raises(ValidationError):
            UserCreate(**user_data)

    def test_user_create_invalid_gstin(self):
        """Test user creation with invalid GSTIN"""
        user_data = {
            "email": "test@example.com",
            "business_name": "Test Business",
            "gstin": "INVALID_GSTIN",
            "business_type": BusinessType.RETAIL_STORE,
            "password": "SecurePass123"
        }
        with pytest.raises(ValidationError):
            UserCreate(**user_data)

    def test_user_create_weak_password(self):
        """Test user creation with weak password"""
        user_data = {
            "email": "test@example.com",
            "business_name": "Test Business",
            "gstin": "29ABCDE1234F1Z5",
            "business_type": BusinessType.RETAIL_STORE,
            "password": "weak"
        }
        with pytest.raises(ValidationError):
            UserCreate(**user_data)

    def test_user_update_valid(self):
        """Test valid user update"""
        update_data = {
            "email": "newemail@example.com",
            "business_name": "Updated Business Name"
        }
        user_update = UserUpdate(**update_data)
        assert user_update.email == "newemail@example.com"
        assert user_update.business_name == "Updated Business Name"


class TestAddressSchemas:
    """Test address Pydantic model validation"""

    def test_address_create_valid(self):
        """Test valid address creation"""
        address_data = {
            "address_line_1": "123 Main Street",
            "city": "Nellore",
            "state": "Andhra Pradesh",
            "postal_code": "524001",
            "country": "India"
        }
        address = AddressCreate(**address_data)
        assert address.address_line_1 == "123 Main Street"
        assert address.city == "Nellore"
        assert address.postal_code == "524001"

    def test_address_create_invalid_postal_code(self):
        """Test address creation with invalid postal code"""
        address_data = {
            "address_line_1": "123 Main Street",
            "city": "Nellore",
            "state": "Andhra Pradesh",
            "postal_code": "12345",  # Invalid - should be 6 digits
            "country": "India"
        }
        with pytest.raises(ValidationError):
            AddressCreate(**address_data)

    def test_address_create_empty_city(self):
        """Test address creation with empty city"""
        address_data = {
            "address_line_1": "123 Main Street",
            "city": "",
            "state": "Andhra Pradesh",
            "postal_code": "524001",
            "country": "India"
        }
        with pytest.raises(ValidationError):
            AddressCreate(**address_data)


class TestProductSchemas:
    """Test product Pydantic model validation"""

    def test_product_create_valid(self):
        """Test valid product creation"""
        product_data = {
            "name": "Test Product",
            "description": "A test product",
            "sku": "TEST001",
            "retail_price": Decimal("100.00"),
            "company_price": Decimal("80.00"),
            "stock_quantity": 50,
            "weight_kg": Decimal("1.500"),
            "category": "Electronics"
        }
        product = ProductCreate(**product_data)
        assert product.name == "Test Product"
        assert product.sku == "TEST001"
        assert product.retail_price == Decimal("100.00")
        assert product.company_price == Decimal("80.00")

    def test_product_create_invalid_pricing(self):
        """Test product creation with company price >= retail price"""
        product_data = {
            "name": "Test Product",
            "sku": "TEST001",
            "retail_price": Decimal("100.00"),
            "company_price": Decimal("120.00"),  # Invalid - should be less than retail
            "stock_quantity": 50
        }
        with pytest.raises(ValidationError):
            ProductCreate(**product_data)

    def test_product_create_negative_stock(self):
        """Test product creation with negative stock"""
        product_data = {
            "name": "Test Product",
            "sku": "TEST001",
            "retail_price": Decimal("100.00"),
            "company_price": Decimal("80.00"),
            "stock_quantity": -5  # Invalid - should be >= 0
        }
        with pytest.raises(ValidationError):
            ProductCreate(**product_data)


class TestOrderSchemas:
    """Test order Pydantic model validation"""

    def test_order_create_valid(self):
        """Test valid order creation"""
        order_data = {
            "delivery_address_id": 1,
            "items": [
                {
                    "product_id": 1,
                    "quantity": 2
                },
                {
                    "product_id": 2,
                    "quantity": 1
                }
            ],
            "notes": "Test order"
        }
        order = OrderCreate(**order_data)
        assert order.delivery_address_id == 1
        assert len(order.items) == 2
        assert order.items[0].product_id == 1
        assert order.items[0].quantity == 2

    def test_order_create_empty_items(self):
        """Test order creation with empty items list"""
        order_data = {
            "delivery_address_id": 1,
            "items": [],  # Invalid - must have at least one item
            "notes": "Test order"
        }
        with pytest.raises(ValidationError):
            OrderCreate(**order_data)

    def test_order_item_create_invalid_quantity(self):
        """Test order item creation with invalid quantity"""
        item_data = {
            "product_id": 1,
            "quantity": 0  # Invalid - must be > 0
        }
        with pytest.raises(ValidationError):
            OrderItemCreate(**item_data)