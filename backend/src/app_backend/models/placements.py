from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, text, PrimaryKeyConstraint, UniqueConstraint, Index
from sqlalchemy.orm import relationship

from app_backend.shared.database import Base


class Placements(Base):
    """ORM Model for placements table"""
    
    __tablename__ = 'placements'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='placements_pkey'),
        UniqueConstraint('application_id', name='placements_application_id_key'),
        Index('idx_placements_student', 'student_id')
    )

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    student_id = Column(UUID(as_uuid=True), ForeignKey('profiles_student.user_id', name='placements_student_id_fkey'), nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey('profiles_company.user_id', name='placements_company_id_fkey'), nullable=False)
    application_id = Column(UUID(as_uuid=True), ForeignKey('applications.id', name='placements_application_id_fkey'))
    lecturer_id = Column(UUID(as_uuid=True), ForeignKey('profiles_lecturer.user_id', name='placements_lecturer_id_fkey'))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(Enum('ACTIVE', 'COMPLETED', 'DROPPED', 'EXTENDED', name='placement_status_enum'), server_default=text("'ACTIVE'::placement_status_enum"))
    created_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

    application = relationship('Applications', back_populates='placements')
    company = relationship('ProfilesCompany', back_populates='placements')
    lecturer = relationship('ProfilesLecturer', back_populates='placements')
    student = relationship('ProfilesStudent', back_populates='placements')
    activity_logs = relationship('ActivityLogs', back_populates='placement')
    placement_milestones = relationship('PlacementMilestones', back_populates='placement')
    sks_conversions = relationship('SksConversions', back_populates='placement')
