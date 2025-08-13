import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "message" in data
    assert "version" in data


def test_cors_middleware_configured():
    """Test CORS middleware is configured"""
    from app.main import app
    from starlette.middleware.cors import CORSMiddleware
    
    # Check if CORS middleware is configured
    middleware_classes = [middleware.cls for middleware in app.user_middleware]
    assert CORSMiddleware in middleware_classes


def test_security_headers():
    """Test security headers are present"""
    response = client.get("/health")
    assert response.status_code == 200
    
    # Check security headers
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("X-XSS-Protection") == "1; mode=block"
    assert "Strict-Transport-Security" in response.headers
    assert "Referrer-Policy" in response.headers