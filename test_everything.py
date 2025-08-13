#!/usr/bin/env python3
"""
Interactive test script to demonstrate models, schemas, and repositories
Run this with: python test_everything.py
"""

from decimal import Decimal
from pydantic import ValidationError
from sqlalchemy.orm import sessionmaker
from app.core.database import engine, init_db
from app.models.user import BusinessType
from app.schemas.user import UserCreate, UserResponse
from app.schemas.product import ProductCreate
from app.schemas.address import AddressCreate
from app.repositories.user import UserRepository
from app.repositories.product import ProductRepository
from app.repositories.address import AddressRepository

# Create database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_schema_validation():
    """Test Pydantic schema validation"""
    print("🔍 TESTING SCHEMA VALIDATION")
    print("=" * 50)
    
    # Test 1: Valid user data
    print("\n✅ Test 1: Valid User Data")
    try:
        valid_user = UserCreate(
            email="test@example.com",
            phone="+919876543210",
            business_name="Test Business",
            gstin="29ABCDE1234F1Z5",
            business_type=BusinessType.RETAIL_STORE,
            password="SecurePass123"
        )
        print(f"   ✓ User created successfully: {valid_user.email}")
        print(f"   ✓ Business Type: {valid_user.business_type.value}")
        print(f"   ✓ GSTIN: {valid_user.gstin}")
    except ValidationError as e:
        print(f"   ❌ Validation failed: {e}")
    
    # Test 2: Invalid email
    print("\n❌ Test 2: Invalid Email")
    try:
        invalid_user = UserCreate(
            email="not-an-email",
            business_name="Test Business",
            gstin="29ABCDE1234F1Z5",
            business_type=BusinessType.RETAIL_STORE,
            password="SecurePass123"
        )
        print("   ❌ This should have failed!")
    except ValidationError as e:
        print(f"   ✓ Correctly caught invalid email: {e.errors()[0]['msg']}")
    
    # Test 3: Invalid GSTIN
    print("\n❌ Test 3: Invalid GSTIN")
    try:
        invalid_gstin = UserCreate(
            email="test@example.com",
            business_name="Test Business",
            gstin="INVALID_GSTIN",
            business_type=BusinessType.RETAIL_STORE,
            password="SecurePass123"
        )
        print("   ❌ This should have failed!")
    except ValidationError as e:
        print(f"   ✓ Correctly caught invalid GSTIN: {e.errors()[0]['msg']}")
    
    # Test 4: Weak password
    print("\n❌ Test 4: Weak Password")
    try:
        weak_password = UserCreate(
            email="test@example.com",
            business_name="Test Business",
            gstin="29ABCDE1234F1Z5",
            business_type=BusinessType.RETAIL_STORE,
            password="weak"
        )
        print("   ❌ This should have failed!")
    except ValidationError as e:
        print(f"   ✓ Correctly caught weak password: {e.errors()[0]['msg']}")
    
    # Test 5: Product validation
    print("\n✅ Test 5: Valid Product")
    try:
        valid_product = ProductCreate(
            name="Test Product",
            sku="TEST001",
            retail_price=Decimal("100.00"),
            company_price=Decimal("80.00"),
            stock_quantity=50,
            category="Electronics"
        )
        print(f"   ✓ Product created: {valid_product.name}")
        print(f"   ✓ Retail Price: ₹{valid_product.retail_price}")
        print(f"   ✓ Company Price: ₹{valid_product.company_price}")
    except ValidationError as e:
        print(f"   ❌ Validation failed: {e}")
    
    # Test 6: Invalid product pricing
    print("\n❌ Test 6: Invalid Product Pricing")
    try:
        invalid_pricing = ProductCreate(
            name="Test Product",
            sku="TEST001",
            retail_price=Decimal("80.00"),
            company_price=Decimal("100.00"),  # Company price higher than retail
            stock_quantity=50
        )
        print("   ❌ This should have failed!")
    except ValidationError as e:
        print(f"   ✓ Correctly caught pricing error: {e.errors()[0]['msg']}")


def test_database_operations():
    """Test database operations using repositories"""
    print("\n\n🗄️  TESTING DATABASE OPERATIONS")
    print("=" * 50)
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    try:
        # Test User Repository
        print("\n👤 Testing User Repository")
        user_repo = UserRepository(db)
        
        # Create a user
        user_data = {
            "email": "testuser@example.com",
            "phone": "+919876543210",
            "hashed_password": "hashed_password_here",
            "business_name": "Test Retail Store",
            "gstin": "29ABCDE1234F1Z5",
            "business_type": BusinessType.RETAIL_STORE,
            "is_active": True,
            "is_verified": False
        }
        
        user = user_repo.create(user_data)
        print(f"   ✓ Created user: {user.email} (ID: {user.id})")
        
        # Find user by email
        found_user = user_repo.get_by_email("testuser@example.com")
        print(f"   ✓ Found user by email: {found_user.business_name}")
        
        # Verify user
        verified_user = user_repo.verify_user(user.id)
        print(f"   ✓ User verified: {verified_user.is_verified}")
        
        # Test Product Repository
        print("\n📦 Testing Product Repository")
        product_repo = ProductRepository(db)
        
        product_data = {
            "name": "Test Smartphone",
            "description": "A great smartphone for testing",
            "sku": "PHONE001",
            "retail_price": Decimal("25000.00"),
            "company_price": Decimal("20000.00"),
            "stock_quantity": 100,
            "is_active": True,
            "category": "Electronics"
        }
        
        product = product_repo.create(product_data)
        print(f"   ✓ Created product: {product.name} (SKU: {product.sku})")
        
        # Update stock
        updated_product = product_repo.update_stock(product.id, -10)
        print(f"   ✓ Updated stock: {updated_product.stock_quantity} units")
        
        # Search products
        search_results = product_repo.search_products("smartphone")
        print(f"   ✓ Search results: {len(search_results)} products found")
        
        # Test Address Repository
        print("\n🏠 Testing Address Repository")
        address_repo = AddressRepository(db)
        
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
        print(f"   ✓ Created address: {address.city}, {address.state}")
        
        # Get user addresses
        user_addresses = address_repo.get_user_addresses(user.id)
        print(f"   ✓ User has {len(user_addresses)} addresses")
        
        print("\n🎉 All database operations completed successfully!")
        
    except Exception as e:
        print(f"   ❌ Database operation failed: {e}")
        db.rollback()
    finally:
        db.close()


def test_business_logic():
    """Test business logic scenarios"""
    print("\n\n🧠 TESTING BUSINESS LOGIC")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        user_repo = UserRepository(db)
        product_repo = ProductRepository(db)
        
        # Test business type pricing logic
        print("\n💰 Testing Business Type Pricing")
        
        # Get a product
        product = product_repo.get_by_sku("PHONE001")
        if product:
            print(f"   📱 Product: {product.name}")
            print(f"   💵 Retail Store Price: ₹{product.retail_price}")
            print(f"   🏢 Company Price: ₹{product.company_price}")
            print(f"   💡 Company saves: ₹{product.retail_price - product.company_price}")
        
        # Test user verification workflow
        print("\n✅ Testing User Verification Workflow")
        unverified_users = user_repo.get_by_field("is_verified", False)
        print(f"   📊 Unverified users: {len(unverified_users)}")
        
        verified_users = user_repo.get_verified_users()
        print(f"   📊 Verified users: {len(verified_users)}")
        
        # Test stock management
        print("\n📦 Testing Stock Management")
        low_stock_products = product_repo.get_low_stock_products(threshold=50)
        print(f"   ⚠️  Low stock products: {len(low_stock_products)}")
        
        in_stock_products = product_repo.get_in_stock_products()
        print(f"   ✅ In stock products: {len(in_stock_products)}")
        
    except Exception as e:
        print(f"   ❌ Business logic test failed: {e}")
    finally:
        db.close()


def main():
    """Run all tests"""
    print("🧪 TESTING ANON B2B E-COMMERCE PLATFORM")
    print("=" * 60)
    print("This script tests our Models, Schemas, and Repositories")
    print("=" * 60)
    
    # Test schema validation
    test_schema_validation()
    
    # Test database operations
    test_database_operations()
    
    # Test business logic
    test_business_logic()
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS COMPLETED!")
    print("=" * 60)
    print("\n💡 What you just saw:")
    print("   • Schema validation catching invalid data")
    print("   • Repository pattern managing database operations")
    print("   • Business logic working with real data")
    print("   • Models storing data in the database")
    print("\n🚀 Next: Run 'python run.py' to start the API server!")


if __name__ == "__main__":
    main()