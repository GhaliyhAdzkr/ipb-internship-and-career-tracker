from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, String, Text, Numeric, DateTime, Enum, ForeignKey, text, PrimaryKeyConstraint, Index
from sqlalchemy.orm import relationship

from app_backend.shared.database import Base


class Vacancies(Base):
    """ORM Model for vacancies table"""
    
    __tablename__ = 'vacancies'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='vacancies_pkey'),
        Index('idx_vacancies_active', 'open_date', 'close_date')
    )

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    company_id = Column(UUID(as_uuid=True), ForeignKey('profiles_company.user_id', name='vacancies_company_id_fkey'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    type = Column(Enum('INTERNSHIP_GENERAL', 'MBKM_INTERNSHIP', 'MBKM_STUDY_INDEPENDENT', 'FULL_TIME', name='vacancy_type_enum'), nullable=False)
    open_date = Column(DateTime(timezone=True), nullable=False)
    close_date = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(100))
    salary_min = Column(Numeric(15, 2))
    salary_max = Column(Numeric(15, 2))
    is_auto_close = Column(Boolean, server_default=text('true'))
    is_active = Column(Boolean, server_default=text('true'))
    created_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

    company = relationship('ProfilesCompany', back_populates='vacancies')
    applications = relationship('Applications', back_populates='vacancy')
    vacancy_skills = relationship('VacancySkills', back_populates='vacancy')
