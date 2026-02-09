from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Text, DateTime, Enum, ForeignKey, text, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from app_backend.shared.database import Base


class ApplicationLogs(Base):
    """ORM Model for application_logs table"""
    
    __tablename__ = 'application_logs'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='application_logs_pkey'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    application_id = Column(UUID(as_uuid=True), ForeignKey('applications.id', ondelete='CASCADE', name='application_logs_application_id_fkey'))
    previous_status = Column(Enum('APPLIED', 'SCREENING', 'INTERVIEW', 'OFFERED', 'ACCEPTED', 'REJECTED', 'WITHDRAWN', name='app_status_enum'))
    new_status = Column(Enum('APPLIED', 'SCREENING', 'INTERVIEW', 'OFFERED', 'ACCEPTED', 'REJECTED', 'WITHDRAWN', name='app_status_enum'), nullable=False)
    changed_by = Column(UUID(as_uuid=True))
    reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

    application = relationship('Applications', back_populates='application_logs')
