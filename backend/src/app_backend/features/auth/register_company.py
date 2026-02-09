"""
Register Company Feature - Command Handler
Fitur untuk registrasi perusahaan baru
"""
import uuid
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Session

from app_backend.domain.user import User as DomainUser, UserRole
from app_backend.domain.company import Company as DomainCompany
from app_backend.models.users import Users
from app_backend.models.profiles_company import ProfilesCompany
from app_backend.schemas.user import CompanyRegister
from app_backend.shared.security import hash_password


class RegisterCompanyException(Exception):
    """Exception yang terjadi saat registrasi perusahaan"""
    pass


@dataclass
class RegisterCompanyCommand:
    """Command untuk registrasi perusahaan baru"""
    payload: CompanyRegister


@dataclass
class RegisterCompanyResult:
    """Result dari proses registrasi perusahaan"""
    user: Optional[DomainUser] = None
    company: Optional[DomainCompany] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        """Cek apakah ada error"""
        return self.error_message is not None


def register_company_command_handler(
    command: RegisterCompanyCommand, 
    session: Session
) -> RegisterCompanyResult:
    """
    Handle registrasi perusahaan baru
    
    Business Rules:
    1. Email harus unik
    2. Password harus di-hash sebelum disimpan
    3. Role otomatis COMPANY (tidak bisa diubah dari client)
    4. Company profile dibuat dengan is_verified=False (perlu verifikasi admin)
    5. User dan profile company dibuat bersamaan dalam transaksi
    """
    
    # Cek apakah email sudah ada
    existing_email = session.query(Users).filter(
        Users.email == command.payload.email
    ).first()
    
    if existing_email:
        return RegisterCompanyResult(error_message="Email sudah terdaftar")
    
    try:
        # Generate user ID
        user_id = uuid.uuid4()
        
        # Buat domain user (ROLE HARDCODED KE COMPANY)
        domain_user = DomainUser(
            id=user_id,
            email=command.payload.email,
            password_hash=hash_password(command.payload.password),
            role=UserRole.COMPANY.value,  # HARDCODED - tidak dari input user
            is_active=True,
            last_login_at=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Buat domain company
        domain_company = DomainCompany(
            user_id=user_id,
            company_name=command.payload.company_name,
            industry=command.payload.industry,
            website_url=None,
            address=None,
            is_verified=False,  # Perlu verifikasi admin
            updated_at=datetime.utcnow()
        )
        
        # Convert ke ORM models
        user_model = Users.from_domain(domain_user)
        company_model = ProfilesCompany(
            user_id=domain_company.user_id,
            company_name=domain_company.company_name,
            industry=domain_company.industry,
            website_url=domain_company.website_url,
            address=domain_company.address,
            is_verified=domain_company.is_verified,
            updated_at=domain_company.updated_at
        )
        
        # Simpan dalam transaksi
        session.add(user_model)
        session.add(company_model)
        session.commit()
        session.refresh(user_model)
        session.refresh(company_model)
        
        # Return domain models
        return RegisterCompanyResult(
            user=user_model.to_domain(),
            company=domain_company
        )
        
    except ValueError as e:
        # Error validasi domain
        session.rollback()
        return RegisterCompanyResult(error_message=str(e))
    except Exception as e:
        session.rollback()
        return RegisterCompanyResult(error_message=f"Registrasi gagal: {str(e)}")
