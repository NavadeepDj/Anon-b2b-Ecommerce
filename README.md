# Anon B2B E-commerce Platform

A comprehensive business-to-business e-commerce platform built with FastAPI, designed for Anon company to serve retail stores and companies across India with location-based delivery and tiered pricing.

## Features

- **GST-based Authentication**: Automatic business verification using GSTIN
- **Tiered Pricing**: Different pricing for retail stores vs companies
- **Location-based Delivery**: Optimized delivery scheduling based on proximity to Nellore
- **Secure Payment Processing**: Multiple payment gateway integration
- **Real-time Inventory Management**: Live stock tracking and updates
- **Admin Dashboard**: Comprehensive management interface
- **Notification System**: Email and SMS notifications for order updates

## Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis for sessions and caching
- **Authentication**: JWT tokens with refresh mechanism
- **API Documentation**: Automatic OpenAPI/Swagger documentation

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Redis 6+
- Docker & Docker Compose (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd anon-b2b-ecommerce
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   # Create database
   createdb anon_b2b_db
   
   # Run migrations
   alembic upgrade head
   ```

6. **Start the application**
   ```bash
   python run.py
   ```

### Using Docker

1. **Start services**
   ```bash
   docker-compose up -d
   ```

2. **Run migrations**
   ```bash
   docker-compose exec app alembic upgrade head
   ```

## API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
anon-b2b-ecommerce/
├── app/
│   ├── core/           # Core configuration and utilities
│   │   ├── config.py   # Application settings
│   │   ├── database.py # Database configuration
│   │   ├── redis_client.py # Redis client
│   │   └── security.py # Security utilities
│   ├── models/         # SQLAlchemy models
│   ├── routers/        # FastAPI route handlers
│   ├── services/       # Business logic services
│   ├── utils/          # Utility functions
│   └── main.py         # FastAPI application
├── alembic/            # Database migrations
├── requirements.txt    # Python dependencies
├── docker-compose.yml  # Docker services
├── Dockerfile         # Application container
└── run.py             # Development server
```

## Environment Variables

Key environment variables (see `.env.example` for complete list):

```bash
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/anon_b2b_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here

# External Services
GST_API_BASE_URL=https://api.gst.gov.in
PAYMENT_GATEWAY_URL=https://api.razorpay.com
```

## Development

### Running Tests
```bash
pytest
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Code Quality
```bash
# Format code
black app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

## Health Check

The application provides a health check endpoint:
```bash
curl http://localhost:8000/health
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is proprietary software owned by Anon Company.