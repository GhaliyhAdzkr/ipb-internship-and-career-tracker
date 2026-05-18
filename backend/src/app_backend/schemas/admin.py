from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

# Departments


class DepartmentCreate(BaseModel):
    code: str = Field(..., max_length=10, description="Kode unik prodi, contoh: ILK")
    name: str = Field(..., max_length=150, description="Nama program studi")
    faculty: str = Field(..., max_length=100, description="Nama fakultas")


class DepartmentUpdate(BaseModel):
    code: Optional[str] = Field(None, max_length=10)
    name: Optional[str] = Field(None, max_length=150)
    faculty: Optional[str] = Field(None, max_length=100)


class DepartmentResponse(BaseModel):
    id: UUID
    code: str
    name: str
    faculty: str

    model_config = {"from_attributes": True}


# Skills


class SkillCreate(BaseModel):
    name: str = Field(..., max_length=100, description="Nama skill, contoh: Python")
    category: Optional[str] = Field(None, max_length=50, description="Kategori skill, contoh: Programming Language")


class SkillUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=50)


class SkillResponse(BaseModel):
    id: UUID
    name: str
    category: Optional[str] = None

    model_config = {"from_attributes": True}


# External Companies


class CompanyCreate(BaseModel):
    name: str = Field(..., max_length=150, description="Nama perusahaan (unik)")
    industry: Optional[str] = Field(None, max_length=100, description="Bidang industri")
    website_url: Optional[str] = Field(None, description="URL situs resmi perusahaan")
    address: Optional[str] = Field(None, description="Alamat kantor")
    logo_url: Optional[str] = Field(None, description="URL logo perusahaan")


class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=150)
    industry: Optional[str] = Field(None, max_length=100)
    website_url: Optional[str] = None
    address: Optional[str] = None
    logo_url: Optional[str] = None


class CompanyResponse(BaseModel):
    id: UUID
    name: str
    industry: Optional[str] = None
    website_url: Optional[str] = None
    address: Optional[str] = None
    logo_url: Optional[str] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# Admin Profile


class AdminProfileResponse(BaseModel):
    """Response untuk GET /admin/profile/me"""

    user_id: UUID
    email: str
    role: str
    is_active: bool
    full_name: str
    unit_name: str
    nip: Optional[str] = None
    last_login_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class AdminProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=150)
    unit_name: Optional[str] = Field(None, max_length=150)
    nip: Optional[str] = Field(None, max_length=30)
