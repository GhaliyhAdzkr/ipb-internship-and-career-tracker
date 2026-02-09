from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text, Numeric, DateTime, Enum, ForeignKey, text, PrimaryKeyConstraint, UniqueConstraint, Index
from sqlalchemy.orm import relationship

from app_backend.shared.database import Base


class Applications(Base):
    """ORM Model for applications table"""
    
    __tablename__ = 'applications'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='applications_pkey'),
        UniqueConstraint('vacancy_id', 'student_id', name='applications_vacancy_id_student_id_key'),
        Index('idx_apps_student', 'student_id', 'status')
    )

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    vacancy_id = Column(UUID(as_uuid=True), ForeignKey('vacancies.id', name='applications_vacancy_id_fkey'), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey('profiles_student.user_id', name='applications_student_id_fkey'), nullable=False)
    status = Column(Enum('APPLIED', 'SCREENING', 'INTERVIEW', 'OFFERED', 'ACCEPTED', 'REJECTED', 'WITHDRAWN', name='app_status_enum'), server_default=text("'APPLIED'::app_status_enum"))
    match_percentage = Column(Numeric(5, 2))
    cv_snapshot_url = Column(Text)
    applied_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

    student = relationship('ProfilesStudent', back_populates='applications')
    vacancy = relationship('Vacancies', back_populates='applications')
    application_logs = relationship('ApplicationLogs', back_populates='application')
    placements = relationship('Placements', uselist=False, back_populates='application')
