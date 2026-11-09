from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes.aqi import router as aqi_router
from app.db.base import Base
from app.db.session import engine
from app import models


app = FastAPI(
    title="LIVE AQI INDIA",
    description="Real-time air quality monitoring API for Indian cities",
    version="1.0.0",
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API Routes
app.include_router(aqi_router, prefix="/api/v1")


# Create Database Tables
@app.on_event("startup")
def create_dev_tables():
    Base.metadata.create_all(bind=engine)


# Root Endpoint
@app.get("/")
def home():
    return {
        "project": "LIVE AQI INDIA",
        "message": "Backend is running successfully!",
    }


# Health Check Endpoint
@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed",
        ) from exc