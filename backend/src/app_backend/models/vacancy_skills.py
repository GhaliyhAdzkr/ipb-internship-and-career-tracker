from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, ForeignKey, text, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from app_backend.shared.database import Base


class VacancySkills(Base):
    """ORM Model for vacancy_skills table"""
    
    __tablename__ = 'vacancy_skills'
    __table_args__ = (
        PrimaryKeyConstraint('vacancy_id', 'skill_id', name='vacancy_skills_pkey'),
    )

    vacancy_id = Column(UUID(as_uuid=True), ForeignKey('vacancies.id', ondelete='CASCADE', name='vacancy_skills_vacancy_id_fkey'), primary_key=True)
    skill_id = Column(UUID(as_uuid=True), ForeignKey('master_skills.id', ondelete='CASCADE', name='vacancy_skills_skill_id_fkey'), primary_key=True)
    is_mandatory = Column(Boolean, server_default=text('true'))

    skill = relationship('MasterSkills', back_populates='vacancy_skills')
    vacancy = relationship('Vacancies', back_populates='vacancy_skills')
