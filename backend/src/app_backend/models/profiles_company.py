from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, String, Text, DateTime, ForeignKey, text, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from app_backend.shared.database import Base


class ProfilesCompany(Base):
    """ORM Model for profiles_company table"""
    
    __tablename__ = 'profiles_company'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='profiles_company_pkey'),
    )

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE', name='profiles_company_user_id_fkey'), primary_key=True)
    company_name = Column(String(150), nullable=False)
    industry = Column(String(100))
    website_url = Column(Text)
    address = Column(Text)
    is_verified = Column(Boolean, server_default=text('false'))
    updated_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

    vacancies = relationship('Vacancies', back_populates='company')
    placements = relationship('Placements', back_populates='company')
    
    def to_domain(self):
        """Convert ORM model to domain model"""
        from app_backend.domain.company import Company
        
        return Company(
            user_id=self.user_id,
            company_name=self.company_name,
            industry=self.industry,
            website_url=self.website_url,
            address=self.address,
            is_verified=self.is_verified if self.is_verified is not None else False,
            updated_at=self.updated_at
        )
    
    @staticmethod
    def from_domain(company):
        """Create ORM model from domain model"""
        return ProfilesCompany(
            user_id=company.user_id,
            company_name=company.company_name,
            industry=company.industry,
            website_url=company.website_url,
            address=company.address,
            is_verified=company.is_verified,
            updated_at=company.updated_at
        )
