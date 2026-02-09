from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey, text, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from app_backend.shared.database import Base


class DocumentRequests(Base):
    """ORM Model for document_requests table"""
    
    __tablename__ = 'document_requests'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='document_requests_pkey'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    document_type = Column(String(50), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey('profiles_student.user_id', name='document_requests_student_id_fkey'))
    reference_id = Column(UUID(as_uuid=True))
    generated_url = Column(Text)
    status = Column(Enum('PENDING', 'APPROVED', 'REJECTED', 'REVISION', name='validation_status_enum'), server_default=text("'PENDING'::validation_status_enum"))
    created_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

    student = relationship('ProfilesStudent', back_populates='document_requests')
