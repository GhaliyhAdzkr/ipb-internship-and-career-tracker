from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class DepartmentInfo(BaseModel):
    """Info singkat department"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    code: str
    name: str
    faculty: str


class SkillInfo(BaseModel):
    """Info skill dengan level"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(alias="skill_id")
    skill_name: str
    skill_category: Optional[str] = None
    level: int = Field(..., ge=1, le=5, description="Level keahlian 1-5")


class StudentProfileResponse(BaseModel):
    """Response untuk GET /profile/me - Data lengkap mahasiswa"""

    # User data
    user_id: UUID
    email: str
    role: str
    is_active: bool

    # Academic data
    nim: str
    full_name: str
    semester: int
    department: Optional[DepartmentInfo] = None
    gpa: Optional[Decimal] = Field(None, ge=0, le=4, description="IPK mahasiswa")
    is_mbkm_eligible: bool

    # CV data
    phone_number: Optional[str] = None
    linkedin_url: Optional[str] = None
    cv_url: Optional[str] = None
    avatar_url: Optional[str] = None

    # Skills
    skills: List[SkillInfo] = []

    # Metadata
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class SkillUpdate(BaseModel):
    """Schema untuk update skill"""

    skill_id: UUID
    level: int = Field(..., ge=1, le=5, description="Level keahlian 1-5 (1=Beginner, 5=Expert)")


class CVDataUpdate(BaseModel):
    """Schema untuk PUT /profile/cv-data - Update data CV"""

    phone_number: Optional[str] = Field(None, max_length=20, description="Nomor telepon")
    linkedin_url: Optional[HttpUrl] = Field(None, description="URL profil LinkedIn")
    cv_url: Optional[HttpUrl] = Field(None, description="URL file CV (Wajib Google Drive shareable link)")
    skills: Optional[List[SkillUpdate]] = Field(default=None, description="Daftar skills dengan level")

    @field_validator("cv_url")
    @classmethod
    def validate_cv_url(cls, v: Optional[HttpUrl]) -> Optional[HttpUrl]:
        if v is None:
            return v

        url_str = str(v)
        # Check if Google Drive url
        if "drive.google.com" not in url_str:
            raise ValueError("URL CV wajib berupa link Google Drive (drive.google.com)")

        # Check if it contains /file/d/ and /view
        if "/file/d/" not in url_str or "/view" not in url_str:
            raise ValueError(
                "URL Google Drive wajib dalam format shareable link view (contoh: https://drive.google.com/file/d/.../view)"
            )

        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "phone_number": "+6281234567890",
                "linkedin_url": "https://linkedin.com/in/johndoe",
                "cv_url": "https://drive.google.com/file/d/abc123/view",
                "skills": [
                    {"skill_id": "550e8400-e29b-41d4-a716-446655440000", "level": 4},
                    {"skill_id": "660e8400-e29b-41d4-a716-446655440001", "level": 3},
                ],
            }
        }
    )
