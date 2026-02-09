from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey, text, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from app_backend.shared.database import Base


class SksConversions(Base):
    """ORM Model for sks_conversions table"""
    
    __tablename__ = 'sks_conversions'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sks_conversions_pkey'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    placement_id = Column(UUID(as_uuid=True), ForeignKey('placements.id', ondelete='CASCADE', name='sks_conversions_placement_id_fkey'))
    total_credits_proposed = Column(Integer)
    total_credits_approved = Column(Integer)
    status = Column(Enum('PENDING', 'APPROVED', 'REJECTED', 'REVISION', name='validation_status_enum'), server_default=text("'PENDING'::validation_status_enum"))
    approved_by = Column(UUID(as_uuid=True), ForeignKey('profiles_lecturer.user_id', name='sks_conversions_approved_by_fkey'))
    created_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

    profiles_lecturer = relationship('ProfilesLecturer', back_populates='sks_conversions')
    placement = relationship('Placements', back_populates='sks_conversions')
