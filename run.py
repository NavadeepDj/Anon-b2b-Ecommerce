#!/usr/bin/env python3
"""
Development server runner for Anon B2B E-commerce Platform
"""
import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    print("🚀 Starting Anon B2B E-commerce Platform...")
    print(f"📍 Server will be available at:")
    print(f"   • http://localhost:8000/")
    print(f"   • http://127.0.0.1:8000/")
    if settings.DEBUG:
        print(f"📚 API Documentation:")
        print(f"   • Swagger UI: http://localhost:8000/docs")
        print(f"   • ReDoc: http://localhost:8000/redoc")
    print(f"💡 Press CTRL+C to stop the server")
    print("-" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )