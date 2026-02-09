"""Pydantic schemas untuk validasi request/response API.

Berisi schema untuk validasi data user
"""
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from enum import Enum


class UserRole(str, Enum):
    """Enum untuk role user"""
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"
    COMPANY = "COMPANY"
    LECTURER = "LECTURER"


class UserBase(BaseModel):
    """Schema dasar untuk user"""
    email: EmailStr


class UserCreate(UserBase):
    """Schema untuk registrasi user
    
    SECURITY: Role TIDAK dikirim dari client, tapi ditentukan dari endpoint yang dipanggil
    """
    password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError('Password harus mengandung minimal satu angka')
        if not any(char.isupper() for char in v):
            raise ValueError('Password harus mengandung minimal satu huruf besar')
        if not any(char.islower() for char in v):
            raise ValueError('Password harus mengandung minimal satu huruf kecil')
        return v


class StudentRegister(UserBase):
    """Schema untuk registrasi mahasiswa"""
    password: str = Field(..., min_length=8, max_length=100)
    nim: str = Field(..., min_length=6, max_length=20)
    full_name: str = Field(..., min_length=3, max_length=150)
    semester: int = Field(..., ge=1, le=14)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError('Password harus mengandung minimal satu angka')
        if not any(char.isupper() for char in v):
            raise ValueError('Password harus mengandung minimal satu huruf besar')
        if not any(char.islower() for char in v):
            raise ValueError('Password harus mengandung minimal satu huruf kecil')
        return v


class CompanyRegister(UserBase):
    """Schema untuk registrasi perusahaan"""
    password: str = Field(..., min_length=8, max_length=100)
    company_name: str = Field(..., min_length=3, max_length=150)
    industry: Optional[str] = Field(None, max_length=100)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError('Password harus mengandung minimal satu angka')
        if not any(char.isupper() for char in v):
            raise ValueError('Password harus mengandung minimal satu huruf besar')
        if not any(char.islower() for char in v):
            raise ValueError('Password harus mengandung minimal satu huruf kecil')
        return v


class LecturerRegister(UserBase):
    """Schema untuk registrasi dosen"""
    password: str = Field(..., min_length=8, max_length=100)
    nip: str = Field(..., min_length=9, max_length=30, description="NIP Dosen")
    full_name: str = Field(..., min_length=3, max_length=150)
    department_id: Optional[uuid.UUID] = Field(None, description="ID Departemen")
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError('Password harus mengandung minimal satu angka')
        if not any(char.isupper() for char in v):
            raise ValueError('Password harus mengandung minimal satu huruf besar')
        if not any(char.islower() for char in v):
            raise ValueError('Password harus mengandung minimal satu huruf kecil')
        return v


class AdminCreateUser(UserBase):
    """Schema untuk admin membuat user (dengan role)"""
    password: str = Field(..., min_length=8, max_length=100)
    role: UserRole = Field(..., description="Role user: ADMIN, STUDENT, COMPANY, LECTURER")


class UserResponse(UserBase):
    """Schema untuk response user"""
    id: uuid.UUID
    role: str
    is_active: bool
    last_login_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema untuk login user"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema untuk response JWT token"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenWithRefresh(BaseModel):
    """Schema untuk response JWT token dengan refresh token"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    """Schema untuk request refresh token"""
    refresh_token: str = Field(..., description="Refresh token yang valid")


class TokenData(BaseModel):
    """Schema untuk payload token"""
    user_id: Optional[uuid.UUID] = None
    email: Optional[str] = None
    role: Optional[str] = None


class RequestResetPassword(BaseModel):
    """Schema untuk request reset password"""
    email: EmailStr = Field(..., description="Email akun yang akan direset")


class ResetPassword(BaseModel):
    """Schema untuk reset password dengan token"""
    token: str = Field(..., description="Reset password token dari email")
    new_password: str = Field(..., min_length=8, max_length=100, description="Password baru")
    
    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError('Password harus mengandung minimal satu angka')
        if not any(char.isupper() for char in v):
            raise ValueError('Password harus mengandung minimal satu huruf besar')
        if not any(char.islower() for char in v):
            raise ValueError('Password harus mengandung minimal satu huruf kecil')
        return v


class ChangePassword(BaseModel):
    """Schema untuk change password (user sudah login)"""
    current_password: str = Field(..., description="Password saat ini")
    new_password: str = Field(..., min_length=8, max_length=100, description="Password baru")
    
    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError('Password harus mengandung minimal satu angka')
        if not any(char.isupper() for char in v):
            raise ValueError('Password harus mengandung minimal satu huruf besar')
        if not any(char.islower() for char in v):
            raise ValueError('Password harus mengandung minimal satu huruf kecil')
        return v
