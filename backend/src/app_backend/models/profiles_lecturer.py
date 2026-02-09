from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, text, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship

from app_backend.shared.database import Base


class ProfilesLecturer(Base):
    """ORM Model for profiles_lecturer table"""
    
    __tablename__ = 'profiles_lecturer'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='profiles_lecturer_pkey'),
        UniqueConstraint('nip', name='profiles_lecturer_nip_key')
    )

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE', name='profiles_lecturer_user_id_fkey'), primary_key=True)
    nip = Column(String(30), nullable=False)
    full_name = Column(String(150), nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey('master_departments.id', name='profiles_lecturer_department_id_fkey'))
    max_mentoring_slots = Column(Integer, server_default=text('10'))
    updated_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

    department = relationship('MasterDepartments', back_populates='profiles_lecturer')
    placements = relationship('Placements', back_populates='lecturer')
    sks_conversions = relationship('SksConversions', back_populates='profiles_lecturer')
