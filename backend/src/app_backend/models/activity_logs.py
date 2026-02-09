from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Date, Text, Numeric, DateTime, Enum, ForeignKey, text, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from app_backend.shared.database import Base


class ActivityLogs(Base):
    """ORM Model for activity_logs table"""
    
    __tablename__ = 'activity_logs'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='activity_logs_pkey'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    placement_id = Column(UUID(as_uuid=True), ForeignKey('placements.id', ondelete='CASCADE', name='activity_logs_placement_id_fkey'))
    activity_date = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    duration_hours = Column(Numeric(4, 2))
    status = Column(Enum('PENDING', 'APPROVED', 'REJECTED', 'REVISION', name='validation_status_enum'), server_default=text("'PENDING'::validation_status_enum"))
    mentor_comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

    placement = relationship('Placements', back_populates='activity_logs')
