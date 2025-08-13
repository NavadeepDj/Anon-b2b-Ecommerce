#!/usr/bin/env python3
"""
Verification script for Anon B2B E-commerce Platform setup
"""
import sys
import os
import importlib.util

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_dependencies():
    """Check if required packages can be imported"""
    print("\n📦 Checking dependencies...")
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'redis',
        'pydantic',
        'jose',
        'passlib',
        'alembic'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def check_project_structure():
    """Check if project structure is correct"""
    print("\n📁 Checking project structure...")
    required_dirs = [
        'app',
        'app/core',
        'app/models',
        'app/services',
        'app/routers',
        'app/utils',
        'alembic',
        'tests'
    ]
    
    required_files = [
        'app/__init__.py',
        'app/main.py',
        'app/core/config.py',
        'app/core/database.py',
        'app/core/redis_client.py',
        'app/core/security.py',
        'requirements.txt',
        '.env.example',
        'run.py',
        'README.md'
    ]
    
    missing_items = []
    
    # Check directories
    for directory in required_dirs:
        if os.path.isdir(directory):
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/")
            missing_items.append(directory)
    
    # Check files
    for file_path in required_files:
        if os.path.isfile(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_items.append(file_path)
    
    return len(missing_items) == 0

def check_configuration():
    """Check if configuration can be loaded"""
    print("\n⚙️  Checking configuration...")
    try:
        # Add current directory to path
        sys.path.insert(0, os.getcwd())
        
        from app.core.config import settings
        print(f"✅ Configuration loaded")
        print(f"   Project: {settings.PROJECT_NAME}")
        print(f"   Version: {settings.VERSION}")
        print(f"   Environment: {settings.ENVIRONMENT}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def check_fastapi_app():
    """Check if FastAPI app can be imported"""
    print("\n🚀 Checking FastAPI application...")
    try:
        from app.main import app
        print(f"✅ FastAPI app loaded")
        print(f"   Title: {app.title}")
        print(f"   Version: {app.version}")
        return True
    except Exception as e:
        print(f"❌ FastAPI app error: {e}")
        return False

def main():
    """Run all checks"""
    print("🔍 Anon B2B E-commerce Platform Setup Verification")
    print("=" * 50)
    
    checks = [
        check_python_version,
        check_dependencies,
        check_project_structure,
        check_configuration,
        check_fastapi_app
    ]
    
    results = []
    for check in checks:
        results.append(check())
    
    print("\n" + "=" * 50)
    if all(results):
        print("🎉 All checks passed! Setup is complete.")
        print("\nNext steps:")
        print("1. Copy .env.example to .env and configure your settings")
        print("2. Set up PostgreSQL and Redis databases")
        print("3. Run 'python run.py' to start the development server")
        print("4. Visit http://localhost:8000/docs for API documentation")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()