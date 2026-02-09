"""
Get Company Detail Feature - Command Handler
"""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app_backend.models.users import Users
from app_backend.models.profiles_company import ProfilesCompany
from app_backend.schemas.company import CompanyDetailResponse


@dataclass
class GetCompanyDetailCommand:
    """Command untuk mengambil detail perusahaan"""
    company_id: UUID


@dataclass
class GetCompanyDetailResult:
    """Result dari get company detail"""
    company: Optional[CompanyDetailResponse] = None
    error_message: Optional[str] = None

    def got_error(self) -> bool:
        """Cek apakah ada error"""
        return self.error_message is not None


def get_company_detail_command_handler(
    command: GetCompanyDetailCommand,
    session: Session
) -> GetCompanyDetailResult:
    """
    Handle get company detail
    
    Business Rules:
    1. Company harus ada
    2. User harus memiliki role COMPANY
    3. Data company bisa diakses public (untuk mahasiswa melihat info perusahaan)
    """
    
    try:
        # Query user
        user = session.query(Users).filter(
            Users.id == command.company_id
        ).first()
        
        if not user:
            return GetCompanyDetailResult(
                error_message="Perusahaan tidak ditemukan"
            )
        
        if user.role != "COMPANY":
            return GetCompanyDetailResult(
                error_message="User bukan perusahaan"
            )
        
        # Query profile company
        profile = session.query(ProfilesCompany).filter(
            ProfilesCompany.user_id == command.company_id
        ).first()
        
        if not profile:
            return GetCompanyDetailResult(
                error_message="Profile perusahaan belum dibuat"
            )
        
        # Build response
        response = CompanyDetailResponse(
            user_id=user.id,
            email=user.email,
            is_active=user.is_active,
            company_name=profile.company_name,
            industry=profile.industry,
            website_url=profile.website_url,
            address=profile.address,
            is_verified=profile.is_verified,
            updated_at=profile.updated_at
        )
        
        return GetCompanyDetailResult(company=response)
        
    except Exception as e:
        session.rollback()
        return GetCompanyDetailResult(
            error_message=f"Error mengambil detail perusahaan: {str(e)}"
        )
