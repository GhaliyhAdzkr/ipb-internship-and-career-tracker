"""
Domain Model untuk User
Model domain yang berisi business logic untuk pengguna
"""
import uuid
from datetime import datetime
from typing import Optional, Literal
from dataclasses import dataclass, field
from enum import Enum


class UserRole(str, Enum):
    """Enum untuk role user"""
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"
    COMPANY = "COMPANY"
    LECTURER = "LECTURER"


@dataclass
class User:
    """Pure domain model untuk User - berisi business logic"""
    
    id: uuid.UUID
    email: str
    password_hash: str
    role: str  # ADMIN, STUDENT, COMPANY, LECTURER
    is_active: bool = True
    last_login_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validasi domain rules"""
        if not self.email or '@' not in self.email:
            raise ValueError("Alamat email tidak valid")
        
        if self.role not in [UserRole.ADMIN.value, UserRole.STUDENT.value, 
                             UserRole.COMPANY.value, UserRole.LECTURER.value]:
            raise ValueError(f"Role tidak valid: {self.role}")
        
        # Set timestamps jika belum ada
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
    
    def activate(self):
        """Aktifkan akun user"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def deactivate(self):
        """Nonaktifkan akun user"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def update_last_login(self):
        """Update waktu login terakhir"""
        self.last_login_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def is_student(self) -> bool:
        """Cek apakah user adalah student"""
        return self.role == UserRole.STUDENT.value
    
    def is_company(self) -> bool:
        """Cek apakah user adalah company"""
        return self.role == UserRole.COMPANY.value
    
    def is_lecturer(self) -> bool:
        """Cek apakah user adalah lecturer"""
        return self.role == UserRole.LECTURER.value
    
    def is_admin(self) -> bool:
        """Cek apakah user adalah admin"""
        return self.role == UserRole.ADMIN.value
        """Update profil user"""
        if full_name:
            self.full_name = full_name
        if username:
            if len(username) < 3:
                raise ValueError("Username harus minimal 3 karakter")
            self.username = username
        self.updated_at = datetime.utcnow()

