from fastapi import FastAPI
from routers import business
from config import engine, Base
from db_models import BusinessModel

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Business CRUD API", description="A complete CRUD API for business management")

# Include routers
app.include_router(business.router)


# Root endpoint
@app.get("/")
def root():
    """API root endpoint"""
    return {
        "message": "Business CRUD API",
        "version": "2.0.0",
        "database": "PostgreSQL",
        "endpoints": {
            "create": "POST /businesses/",
            "read_all": "GET /businesses/",
            "read_one": "GET /businesses/{business_id}",
            "update": "PUT /businesses/{business_id}",
            "partial_update": "PATCH /businesses/{business_id}",
            "delete": "DELETE /businesses/{business_id}",
            "statistics": "GET /businesses/stats/overview",
            "docs": "/docs",
            "redoc": "/redoc",
        },
    }
