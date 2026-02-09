from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, text, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship

from app_backend.shared.database import Base


class MasterDepartments(Base):
    """ORM Model for master_departments table"""
    
    __tablename__ = 'master_departments'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='master_departments_pkey'),
        UniqueConstraint('code', name='master_departments_code_key')
    )

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    code = Column(String(10), nullable=False)
    name = Column(String(100), nullable=False)
    faculty = Column(String(100), nullable=False)

    profiles_lecturer = relationship('ProfilesLecturer', back_populates='department')
    profiles_student = relationship('ProfilesStudent', back_populates='department')
