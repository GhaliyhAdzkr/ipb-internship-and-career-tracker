from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, String, Date, Text, DateTime, Enum, ForeignKey, text, PrimaryKeyConstraint, Index
from sqlalchemy.orm import relationship

from app_backend.shared.database import Base


class PlacementMilestones(Base):
    """ORM Model for placement_milestones table"""
    
    __tablename__ = 'placement_milestones'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='placement_milestones_pkey'),
        Index('idx_milestones_due', 'due_date')
    )

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    placement_id = Column(UUID(as_uuid=True), ForeignKey('placements.id', ondelete='CASCADE', name='placement_milestones_placement_id_fkey'))
    title = Column(String(100), nullable=False)
    category = Column(Enum('ADMINISTRATION', 'LOGBOOK', 'REPORT', 'PRESENTATION', name='milestone_category_enum'), nullable=False)
    due_date = Column(Date, nullable=False)
    is_completed = Column(Boolean, server_default=text('false'))
    submission_url = Column(Text)
    feedback = Column(Text)
    verified_by = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

    placement = relationship('Placements', back_populates='placement_milestones')
