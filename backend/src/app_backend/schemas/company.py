"""
Company Schemas - Pydantic models untuk company endpoints
"""
from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


# ============ Response Schemas ============

class CompanyDetailResponse(BaseModel):
    """Response untuk GET /companies/{id} - Detail perusahaan"""
    
    # User data
    user_id: UUID
    email: str
    is_active: bool
    
    # Company data
    company_name: str
    industry: Optional[str] = None
    website_url: Optional[str] = None
    address: Optional[str] = None
    is_verified: bool
    
    # Metadata
    updated_at: datetime

    class Config:
        from_attributes = True


# ============ Review Schemas (Future Feature) ============

class CompanyReviewCreate(BaseModel):
    """Schema untuk POST /companies/review - Buat review anonim"""
    company_id: UUID
    rating: int = Field(..., ge=1, le=5, description="Rating 1-5 bintang")
    review_text: Optional[str] = Field(None, max_length=1000, description="Teks review")
    work_environment_rating: Optional[int] = Field(None, ge=1, le=5)
    learning_opportunity_rating: Optional[int] = Field(None, ge=1, le=5)
    mentor_quality_rating: Optional[int] = Field(None, ge=1, le=5)
    
    class Config:
        json_schema_extra = {
            "example": {
                "company_id": "550e8400-e29b-41d4-a716-446655440000",
                "rating": 4,
                "review_text": "Pengalaman magang yang sangat baik, banyak belajar hal baru",
                "work_environment_rating": 5,
                "learning_opportunity_rating": 4,
                "mentor_quality_rating": 4
            }
        }


class CompanyReviewResponse(BaseModel):
    """Response untuk review perusahaan"""
    id: UUID
    company_id: UUID
    rating: int
    review_text: Optional[str] = None
    work_environment_rating: Optional[int] = None
    learning_opportunity_rating: Optional[int] = None
    mentor_quality_rating: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
