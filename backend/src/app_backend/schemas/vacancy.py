"""
Pydantic schemas untuk validasi request/response API vacancy
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class VacancyType(str, Enum):
    """Enum untuk tipe lowongan"""

    INTERNSHIP_GENERAL = "INTERNSHIP_GENERAL"
    MBKM_INTERNSHIP = "MBKM_INTERNSHIP"
    MBKM_STUDY_INDEPENDENT = "MBKM_STUDY_INDEPENDENT"
    FULL_TIME = "FULL_TIME"


class PaymentType(str, Enum):
    """Enum untuk tipe pembayaran/kompensasi"""

    PAID = "PAID"
    UNPAID = "UNPAID"
    ALLOWANCE_ONLY = "ALLOWANCE_ONLY"


# ─────────────────────────────────────────────
# Nested Schemas
# ─────────────────────────────────────────────


class CompanyInfo(BaseModel):
    """Info singkat perusahaan"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    industry: Optional[str] = None
    website_url: Optional[str] = None


class SkillRequirement(BaseModel):
    """Kebutuhan skill untuk vacancy"""

    skill_id: UUID
    skill_name: str
    is_mandatory: bool = True


# ─────────────────────────────────────────────
# Create Schemas
# ─────────────────────────────────────────────


class VacancySkillCreate(BaseModel):
    """Schema untuk menambahkan skill ke vacancy"""

    skill_id: UUID
    is_mandatory: bool = Field(True, description="Apakah skill wajib")


class VacancyCreate(BaseModel):
    """Payload untuk membuat lowongan baru"""

    company_id: UUID
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=20)
    type: VacancyType
    open_date: datetime
    close_date: datetime
    location: Optional[str] = Field(None, max_length=150)
    payment_type: PaymentType = PaymentType.UNPAID
    compensation_min: Optional[Decimal] = Field(
        None, ge=0, description="Kompensasi minimum"
    )
    compensation_max: Optional[Decimal] = Field(
        None, ge=0, description="Kompensasi maksimum"
    )
    compensation_note: Optional[str] = None
    source_url: Optional[HttpUrl] = None
    skills: Optional[List[VacancySkillCreate]] = Field(
        default_factory=list, description="Daftar skills yang diperlukan"
    )


# ─────────────────────────────────────────────
# Update Schemas
# ─────────────────────────────────────────────


class VacancySkillUpdate(BaseModel):
    """Schema untuk update skill requirement"""

    skill_id: UUID
    is_mandatory: Optional[bool] = None


class VacancyUpdate(BaseModel):
    """Payload untuk update lowongan"""

    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, min_length=20)
    type: Optional[VacancyType] = None
    open_date: Optional[datetime] = None
    close_date: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=150)
    payment_type: Optional[PaymentType] = None
    compensation_min: Optional[Decimal] = Field(None, ge=0)
    compensation_max: Optional[Decimal] = Field(None, ge=0)
    compensation_note: Optional[str] = None
    source_url: Optional[HttpUrl] = None
    is_active: Optional[bool] = None
    is_auto_close: Optional[bool] = None
    skills: Optional[List[VacancySkillUpdate]] = None


# ─────────────────────────────────────────────
# Response Schemas
# ─────────────────────────────────────────────


class VacancyResponse(BaseModel):
    """Response untuk data vacancy"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    company_id: UUID
    title: str
    description: str
    type: str
    open_date: datetime
    close_date: datetime
    location: Optional[str] = None
    payment_type: Optional[str] = None
    compensation_min: Optional[Decimal] = None
    compensation_max: Optional[Decimal] = None
    compensation_note: Optional[str] = None
    source_url: Optional[str] = None
    is_scraped: bool
    is_auto_close: bool
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class VacancyDetailResponse(BaseModel):
    """Response detail vacancy dengan company dan skills"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    company: CompanyInfo
    title: str
    description: str
    type: str
    open_date: datetime
    close_date: datetime
    location: Optional[str] = None
    payment_type: Optional[str] = None
    compensation_min: Optional[Decimal] = None
    compensation_max: Optional[Decimal] = None
    compensation_note: Optional[str] = None
    source_url: Optional[str] = None
    is_scraped: bool
    is_auto_close: bool
    is_active: bool
    skills: List[SkillRequirement] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class VacancyListResponse(BaseModel):
    """Response untuk list vacancy dengan pagination"""

    items: List[VacancyDetailResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


# ─────────────────────────────────────────────
# Search/Filter Schemas
# ─────────────────────────────────────────────


class VacancySearchFilter(BaseModel):
    """Filter untuk pencarian vacancy"""

    model_config = ConfigDict(populate_by_name=True, validate_by_name=True)

    query: Optional[str] = Field(None, description="Kata kunci pencarian")
    location: Optional[str] = Field(None, description="Filter lokasi")
    vacancy_type: Optional[VacancyType] = Field(None, alias="type")
    payment_type: Optional[PaymentType] = Field(None, alias="payment_type")
    is_active: bool = Field(True, description="Hanya lowongan aktif")


# ─────────────────────────────────────────────
# Job Matching
# ─────────────────────────────────────────────


class JobMatchResult(BaseModel):
    """Hasil matching job dengan profil student"""

    vacancy_id: UUID
    vacancy_title: str
    company_name: str
    match_percentage: float = Field(
        ..., ge=0, le=100, description="Persentase kecocokan"
    )
    matched_skills: List[str] = []
    missing_mandatory_skills: List[str] = []
    total_required_skills: int
    total_matched_skills: int
