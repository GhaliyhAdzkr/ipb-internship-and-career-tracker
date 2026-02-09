from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, text, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship

from app_backend.shared.database import Base


class MasterSkills(Base):
    """ORM Model for master_skills table"""
    
    __tablename__ = 'master_skills'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='master_skills_pkey'),
        UniqueConstraint('name', name='master_skills_name_key')
    )

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    name = Column(String(100), nullable=False)
    category = Column(String(50))

    student_skills = relationship('StudentSkills', back_populates='skill')
    vacancy_skills = relationship('VacancySkills', back_populates='skill')
