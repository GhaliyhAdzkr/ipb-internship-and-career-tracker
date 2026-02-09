from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, ForeignKey, CheckConstraint, PrimaryKeyConstraint, Index
from sqlalchemy.orm import relationship

from app_backend.shared.database import Base


class StudentSkills(Base):
    """ORM Model for student_skills table"""
    
    __tablename__ = 'student_skills'
    __table_args__ = (
        PrimaryKeyConstraint('student_id', 'skill_id', name='student_skills_pkey'),
        CheckConstraint('level >= 1 AND level <= 5', name='student_skills_level_check'),
        Index('idx_skills_matching', 'skill_id')
    )

    student_id = Column(UUID(as_uuid=True), ForeignKey('profiles_student.user_id', ondelete='CASCADE', name='student_skills_student_id_fkey'), primary_key=True)
    skill_id = Column(UUID(as_uuid=True), ForeignKey('master_skills.id', ondelete='CASCADE', name='student_skills_skill_id_fkey'), primary_key=True)
    level = Column(Integer)

    skill = relationship('MasterSkills', back_populates='student_skills')
    student = relationship('ProfilesStudent', back_populates='student_skills')
