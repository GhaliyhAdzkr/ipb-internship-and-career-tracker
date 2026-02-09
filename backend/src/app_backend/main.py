"""
FastAPI Application
Entry point aplikasi FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app_backend.shared.database import engine, Base
from app_backend.routers.api import auth, profile, company

# Buat semua tabel database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IPB Internship and Career Tracker API",
    description="IPB Internship and Career Tracker API | V1.0.0",
    version="1.0.0"
)

# Konfigurasi CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(company.router)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint"""
    return {
        "message": "IPB Internship and Career Tracker API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
