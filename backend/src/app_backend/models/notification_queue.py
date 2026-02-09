from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, text, PrimaryKeyConstraint, Index
from sqlalchemy.orm import relationship

from app_backend.shared.database import Base


class NotificationQueue(Base):
    """ORM Model for notification_queue table"""
    
    __tablename__ = 'notification_queue'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='notification_queue_pkey'),
        Index('idx_notif_pending', 'scheduled_at')
    )

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', name='notification_queue_user_id_fkey'))
    channel = Column(String(20), server_default=text("'ALL'::character varying"))
    scheduled_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))
    sent_at = Column(DateTime(timezone=True))
    status = Column(String(20), server_default=text("'QUEUED'::character varying"))

    user = relationship('Users', back_populates='notification_queue')
