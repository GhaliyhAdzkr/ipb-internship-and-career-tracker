from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, String, Integer, Numeric, Text, DateTime, ForeignKey, text, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship

from app_backend.shared.database import Base


class ProfilesStudent(Base):
    """ORM Model for profiles_student table"""
    
    __tablename__ = 'profiles_student'
    __table_args__ = (
        PrimaryKeyConstraint('user_id', name='profiles_student_pkey'),
        UniqueConstraint('nim', name='profiles_student_nim_key')
    )

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE', name='profiles_student_user_id_fkey'), primary_key=True)
    nim = Column(String(20), nullable=False)
    full_name = Column(String(150), nullable=False)
    semester = Column(Integer, nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey('master_departments.id', name='profiles_student_department_id_fkey'))
    gpa = Column(Numeric(3, 2))
    phone_number = Column(String(20))
    linkedin_url = Column(Text)
    cv_url = Column(Text)
    is_mbkm_eligible = Column(Boolean, server_default=text('false'))
    updated_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

    department = relationship('MasterDepartments', back_populates='profiles_student')
    document_requests = relationship('DocumentRequests', back_populates='student')
    student_skills = relationship('StudentSkills', back_populates='student')
    applications = relationship('Applications', back_populates='student')
    placements = relationship('Placements', back_populates='student')
    
    def to_domain(self):
        """Convert ORM model to domain model"""
        from app_backend.domain.student import Student
        from decimal import Decimal
        
        return Student(
            user_id=self.user_id,
            nim=self.nim,
            full_name=self.full_name,
            semester=self.semester,
            department_id=self.department_id,
            gpa=Decimal(str(self.gpa)) if self.gpa is not None else None,
            phone_number=self.phone_number,
            linkedin_url=self.linkedin_url,
            cv_url=self.cv_url,
            is_mbkm_eligible=self.is_mbkm_eligible if self.is_mbkm_eligible is not None else False,
            updated_at=self.updated_at
        )
    
    @staticmethod
    def from_domain(student):
        """Create ORM model from domain model"""
        return ProfilesStudent(
            user_id=student.user_id,
            nim=student.nim,
            full_name=student.full_name,
            semester=student.semester,
            department_id=student.department_id,
            gpa=student.gpa,
            phone_number=student.phone_number,
            linkedin_url=student.linkedin_url,
            cv_url=student.cv_url,
            is_mbkm_eligible=student.is_mbkm_eligible,
            updated_at=student.updated_at
        )
