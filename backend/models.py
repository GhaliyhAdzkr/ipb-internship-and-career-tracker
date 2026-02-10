from typing import Optional
import datetime
import decimal
import uuid

from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, Date, DateTime, Enum, ForeignKeyConstraint, Index, Integer, Numeric, PrimaryKeyConstraint, String, Table, Text, UniqueConstraint, Uuid, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class MasterDepartments(Base):
    __tablename__ = 'master_departments'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='master_departments_pkey'),
        UniqueConstraint('code', name='master_departments_code_key')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    code: Mapped[str] = mapped_column(String(10), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    faculty: Mapped[str] = mapped_column(String(100), nullable=False)

    master_courses: Mapped[list['MasterCourses']] = relationship('MasterCourses', back_populates='department')
    profiles_lecturer: Mapped[list['ProfilesLecturer']] = relationship('ProfilesLecturer', back_populates='department')
    profiles_student: Mapped[list['ProfilesStudent']] = relationship('ProfilesStudent', back_populates='department')


class MasterSkills(Base):
    __tablename__ = 'master_skills'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='master_skills_pkey'),
        UniqueConstraint('name', name='master_skills_name_key')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(50))

    student_skills: Mapped[list['StudentSkills']] = relationship('StudentSkills', back_populates='skill')
    vacancy_skills: Mapped[list['VacancySkills']] = relationship('VacancySkills', back_populates='skill')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(Enum('ADMIN', 'STUDENT', 'COMPANY', 'LECTURER', name='user_role_enum'), nullable=False)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    last_login_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    notification_queue: Mapped[list['NotificationQueue']] = relationship('NotificationQueue', back_populates='user')


t_view_student_sks_summary = Table(
    'view_student_sks_summary', Base.metadata,
    Column('student_id', Uuid),
    Column('placement_id', Uuid),
    Column('total_courses_mapped', BigInteger),
    Column('total_sks_potential', BigInteger),
    Column('total_sks_approved', BigInteger)
)


class MasterCourses(Base):
    __tablename__ = 'master_courses'
    __table_args__ = (
        CheckConstraint('sks_weight > 0', name='master_courses_sks_weight_check'),
        ForeignKeyConstraint(['department_id'], ['master_departments.id'], ondelete='CASCADE', name='master_courses_department_id_fkey'),
        PrimaryKeyConstraint('id', name='master_courses_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    sks_weight: Mapped[int] = mapped_column(Integer, nullable=False)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    learning_outcomes: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    department: Mapped[Optional['MasterDepartments']] = relationship('MasterDepartments', back_populates='master_courses')
    placement_course_conversions: Mapped[list['PlacementCourseConversions']] = relationship('PlacementCourseConversions', back_populates='course')


class NotificationQueue(Base):
    __tablename__ = 'notification_queue'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], name='notification_queue_user_id_fkey'),
        PrimaryKeyConstraint('id', name='notification_queue_pkey'),
        Index('idx_notif_pending', 'scheduled_at')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    channel: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'ALL'::character varying"))
    scheduled_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    sent_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    status: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'QUEUED'::character varying"))

    user: Mapped[Optional['Users']] = relationship('Users', back_populates='notification_queue')


class ProfilesCompany(Users):
    __tablename__ = 'profiles_company'
    __table_args__ = (
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='profiles_company_user_id_fkey'),
        PrimaryKeyConstraint('user_id', name='profiles_company_pkey')
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    company_name: Mapped[str] = mapped_column(String(150), nullable=False)
    industry: Mapped[Optional[str]] = mapped_column(String(100))
    website_url: Mapped[Optional[str]] = mapped_column(Text)
    address: Mapped[Optional[str]] = mapped_column(Text)
    is_verified: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    vacancies: Mapped[list['Vacancies']] = relationship('Vacancies', back_populates='company')
    placements: Mapped[list['Placements']] = relationship('Placements', back_populates='company')


class ProfilesLecturer(Users):
    __tablename__ = 'profiles_lecturer'
    __table_args__ = (
        ForeignKeyConstraint(['department_id'], ['master_departments.id'], name='profiles_lecturer_department_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='profiles_lecturer_user_id_fkey'),
        PrimaryKeyConstraint('user_id', name='profiles_lecturer_pkey'),
        UniqueConstraint('nip', name='profiles_lecturer_nip_key')
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    nip: Mapped[str] = mapped_column(String(30), nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    max_mentoring_slots: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('10'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    department: Mapped[Optional['MasterDepartments']] = relationship('MasterDepartments', back_populates='profiles_lecturer')
    placements: Mapped[list['Placements']] = relationship('Placements', back_populates='lecturer')
    placement_course_conversions: Mapped[list['PlacementCourseConversions']] = relationship('PlacementCourseConversions', back_populates='profiles_lecturer')


class ProfilesStudent(Users):
    __tablename__ = 'profiles_student'
    __table_args__ = (
        ForeignKeyConstraint(['department_id'], ['master_departments.id'], name='profiles_student_department_id_fkey'),
        ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE', name='profiles_student_user_id_fkey'),
        PrimaryKeyConstraint('user_id', name='profiles_student_pkey'),
        UniqueConstraint('nim', name='profiles_student_nim_key')
    )

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    nim: Mapped[str] = mapped_column(String(20), nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    semester: Mapped[int] = mapped_column(Integer, nullable=False)
    department_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    gpa: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(3, 2))
    phone_number: Mapped[Optional[str]] = mapped_column(String(20))
    linkedin_url: Mapped[Optional[str]] = mapped_column(Text)
    cv_url: Mapped[Optional[str]] = mapped_column(Text)
    is_mbkm_eligible: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    department: Mapped[Optional['MasterDepartments']] = relationship('MasterDepartments', back_populates='profiles_student')
    document_requests: Mapped[list['DocumentRequests']] = relationship('DocumentRequests', back_populates='student')
    student_skills: Mapped[list['StudentSkills']] = relationship('StudentSkills', back_populates='student')
    applications: Mapped[list['Applications']] = relationship('Applications', back_populates='student')
    placements: Mapped[list['Placements']] = relationship('Placements', back_populates='student')


class DocumentRequests(Base):
    __tablename__ = 'document_requests'
    __table_args__ = (
        ForeignKeyConstraint(['student_id'], ['profiles_student.user_id'], name='document_requests_student_id_fkey'),
        PrimaryKeyConstraint('id', name='document_requests_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    document_type: Mapped[str] = mapped_column(String(50), nullable=False)
    student_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    reference_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    generated_url: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[Optional[str]] = mapped_column(Enum('PENDING', 'APPROVED', 'REJECTED', 'REVISION', name='validation_status_enum'), server_default=text("'PENDING'::validation_status_enum"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    student: Mapped[Optional['ProfilesStudent']] = relationship('ProfilesStudent', back_populates='document_requests')


class StudentSkills(Base):
    __tablename__ = 'student_skills'
    __table_args__ = (
        CheckConstraint('level >= 1 AND level <= 5', name='student_skills_level_check'),
        ForeignKeyConstraint(['skill_id'], ['master_skills.id'], ondelete='CASCADE', name='student_skills_skill_id_fkey'),
        ForeignKeyConstraint(['student_id'], ['profiles_student.user_id'], ondelete='CASCADE', name='student_skills_student_id_fkey'),
        PrimaryKeyConstraint('student_id', 'skill_id', name='student_skills_pkey'),
        Index('idx_skills_matching', 'skill_id')
    )

    student_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    skill_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    level: Mapped[Optional[int]] = mapped_column(Integer)

    skill: Mapped['MasterSkills'] = relationship('MasterSkills', back_populates='student_skills')
    student: Mapped['ProfilesStudent'] = relationship('ProfilesStudent', back_populates='student_skills')


class Vacancies(Base):
    __tablename__ = 'vacancies'
    __table_args__ = (
        ForeignKeyConstraint(['company_id'], ['profiles_company.user_id'], name='vacancies_company_id_fkey'),
        PrimaryKeyConstraint('id', name='vacancies_pkey'),
        Index('idx_vacancies_active', 'open_date', 'close_date')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    company_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(Enum('INTERNSHIP_GENERAL', 'MBKM_INTERNSHIP', 'MBKM_STUDY_INDEPENDENT', 'FULL_TIME', name='vacancy_type_enum'), nullable=False)
    open_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    close_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(100))
    salary_min: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(15, 2))
    salary_max: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(15, 2))
    is_auto_close: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    company: Mapped['ProfilesCompany'] = relationship('ProfilesCompany', back_populates='vacancies')
    applications: Mapped[list['Applications']] = relationship('Applications', back_populates='vacancy')
    vacancy_skills: Mapped[list['VacancySkills']] = relationship('VacancySkills', back_populates='vacancy')


class Applications(Base):
    __tablename__ = 'applications'
    __table_args__ = (
        ForeignKeyConstraint(['student_id'], ['profiles_student.user_id'], name='applications_student_id_fkey'),
        ForeignKeyConstraint(['vacancy_id'], ['vacancies.id'], name='applications_vacancy_id_fkey'),
        PrimaryKeyConstraint('id', name='applications_pkey'),
        UniqueConstraint('vacancy_id', 'student_id', name='applications_vacancy_id_student_id_key'),
        Index('idx_apps_student', 'student_id', 'status')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    vacancy_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    student_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    status: Mapped[Optional[str]] = mapped_column(Enum('APPLIED', 'SCREENING', 'INTERVIEW', 'OFFERED', 'ACCEPTED', 'REJECTED', 'WITHDRAWN', name='app_status_enum'), server_default=text("'APPLIED'::app_status_enum"))
    match_percentage: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))
    cv_snapshot_url: Mapped[Optional[str]] = mapped_column(Text)
    applied_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    student: Mapped['ProfilesStudent'] = relationship('ProfilesStudent', back_populates='applications')
    vacancy: Mapped['Vacancies'] = relationship('Vacancies', back_populates='applications')
    application_logs: Mapped[list['ApplicationLogs']] = relationship('ApplicationLogs', back_populates='application')
    placements: Mapped[Optional['Placements']] = relationship('Placements', uselist=False, back_populates='application')


class VacancySkills(Base):
    __tablename__ = 'vacancy_skills'
    __table_args__ = (
        ForeignKeyConstraint(['skill_id'], ['master_skills.id'], ondelete='CASCADE', name='vacancy_skills_skill_id_fkey'),
        ForeignKeyConstraint(['vacancy_id'], ['vacancies.id'], ondelete='CASCADE', name='vacancy_skills_vacancy_id_fkey'),
        PrimaryKeyConstraint('vacancy_id', 'skill_id', name='vacancy_skills_pkey')
    )

    vacancy_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    skill_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    is_mandatory: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('true'))

    skill: Mapped['MasterSkills'] = relationship('MasterSkills', back_populates='vacancy_skills')
    vacancy: Mapped['Vacancies'] = relationship('Vacancies', back_populates='vacancy_skills')


class ApplicationLogs(Base):
    __tablename__ = 'application_logs'
    __table_args__ = (
        ForeignKeyConstraint(['application_id'], ['applications.id'], ondelete='CASCADE', name='application_logs_application_id_fkey'),
        PrimaryKeyConstraint('id', name='application_logs_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    new_status: Mapped[str] = mapped_column(Enum('APPLIED', 'SCREENING', 'INTERVIEW', 'OFFERED', 'ACCEPTED', 'REJECTED', 'WITHDRAWN', name='app_status_enum'), nullable=False)
    application_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    previous_status: Mapped[Optional[str]] = mapped_column(Enum('APPLIED', 'SCREENING', 'INTERVIEW', 'OFFERED', 'ACCEPTED', 'REJECTED', 'WITHDRAWN', name='app_status_enum'))
    changed_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    reason: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    application: Mapped[Optional['Applications']] = relationship('Applications', back_populates='application_logs')


class Placements(Base):
    __tablename__ = 'placements'
    __table_args__ = (
        ForeignKeyConstraint(['application_id'], ['applications.id'], name='placements_application_id_fkey'),
        ForeignKeyConstraint(['company_id'], ['profiles_company.user_id'], name='placements_company_id_fkey'),
        ForeignKeyConstraint(['lecturer_id'], ['profiles_lecturer.user_id'], name='placements_lecturer_id_fkey'),
        ForeignKeyConstraint(['student_id'], ['profiles_student.user_id'], name='placements_student_id_fkey'),
        PrimaryKeyConstraint('id', name='placements_pkey'),
        UniqueConstraint('application_id', name='placements_application_id_key'),
        Index('idx_placements_student', 'student_id')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    student_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    company_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    application_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    lecturer_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    status: Mapped[Optional[str]] = mapped_column(Enum('ACTIVE', 'COMPLETED', 'DROPPED', 'EXTENDED', name='placement_status_enum'), server_default=text("'ACTIVE'::placement_status_enum"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    application: Mapped[Optional['Applications']] = relationship('Applications', back_populates='placements')
    company: Mapped['ProfilesCompany'] = relationship('ProfilesCompany', back_populates='placements')
    lecturer: Mapped[Optional['ProfilesLecturer']] = relationship('ProfilesLecturer', back_populates='placements')
    student: Mapped['ProfilesStudent'] = relationship('ProfilesStudent', back_populates='placements')
    activity_logs: Mapped[list['ActivityLogs']] = relationship('ActivityLogs', back_populates='placement')
    placement_course_conversions: Mapped[list['PlacementCourseConversions']] = relationship('PlacementCourseConversions', back_populates='placement')
    placement_milestones: Mapped[list['PlacementMilestones']] = relationship('PlacementMilestones', back_populates='placement')


class ActivityLogs(Base):
    __tablename__ = 'activity_logs'
    __table_args__ = (
        ForeignKeyConstraint(['placement_id'], ['placements.id'], ondelete='CASCADE', name='activity_logs_placement_id_fkey'),
        PrimaryKeyConstraint('id', name='activity_logs_pkey')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    activity_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    placement_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    duration_hours: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(4, 2))
    status: Mapped[Optional[str]] = mapped_column(Enum('PENDING', 'APPROVED', 'REJECTED', 'REVISION', name='validation_status_enum'), server_default=text("'PENDING'::validation_status_enum"))
    mentor_comment: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    placement: Mapped[Optional['Placements']] = relationship('Placements', back_populates='activity_logs')


class PlacementCourseConversions(Base):
    __tablename__ = 'placement_course_conversions'
    __table_args__ = (
        ForeignKeyConstraint(['approved_by'], ['profiles_lecturer.user_id'], name='placement_course_conversions_approved_by_fkey'),
        ForeignKeyConstraint(['course_id'], ['master_courses.id'], name='placement_course_conversions_course_id_fkey'),
        ForeignKeyConstraint(['placement_id'], ['placements.id'], ondelete='CASCADE', name='placement_course_conversions_placement_id_fkey'),
        PrimaryKeyConstraint('id', name='placement_course_conversions_pkey'),
        UniqueConstraint('placement_id', 'course_id', name='placement_course_conversions_placement_id_course_id_key')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    placement_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    course_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    status: Mapped[Optional[str]] = mapped_column(Enum('PENDING', 'APPROVED', 'REJECTED', 'REVISION', name='validation_status_enum'), server_default=text("'PENDING'::validation_status_enum"))
    relevance_score: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(5, 2))
    evidence_url: Mapped[Optional[str]] = mapped_column(Text)
    approved_sks: Mapped[Optional[int]] = mapped_column(Integer)
    approved_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    profiles_lecturer: Mapped[Optional['ProfilesLecturer']] = relationship('ProfilesLecturer', back_populates='placement_course_conversions')
    course: Mapped['MasterCourses'] = relationship('MasterCourses', back_populates='placement_course_conversions')
    placement: Mapped['Placements'] = relationship('Placements', back_populates='placement_course_conversions')


class PlacementMilestones(Base):
    __tablename__ = 'placement_milestones'
    __table_args__ = (
        ForeignKeyConstraint(['placement_id'], ['placements.id'], ondelete='CASCADE', name='placement_milestones_placement_id_fkey'),
        PrimaryKeyConstraint('id', name='placement_milestones_pkey'),
        Index('idx_milestones_due', 'due_date')
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=text('gen_random_uuid()'))
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(Enum('ADMINISTRATION', 'LOGBOOK', 'REPORT', 'PRESENTATION', name='milestone_category_enum'), nullable=False)
    due_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    placement_id: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    is_completed: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    submission_url: Mapped[Optional[str]] = mapped_column(Text)
    feedback: Mapped[Optional[str]] = mapped_column(Text)
    verified_by: Mapped[Optional[uuid.UUID]] = mapped_column(Uuid)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('CURRENT_TIMESTAMP'))

    placement: Mapped[Optional['Placements']] = relationship('Placements', back_populates='placement_milestones')
