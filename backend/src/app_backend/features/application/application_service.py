import uuid
from datetime import datetime, timezone
from typing import List, Optional, Protocol

from sqlalchemy import select

from app_backend.models.application_logs import ApplicationLogs
from app_backend.models.applications import Applications
from app_backend.repositories.application_log_repository import ApplicationLogRepository
from app_backend.repositories.application_repository import ApplicationRepository
from app_backend.repositories.placement_repository import PlacementRepository
from app_backend.repositories.student_repository import StudentRepository
from app_backend.schemas.application import (
    ApplicationCreate,
    ApplicationLogResponse,
    ApplicationResponse,
    ApplicationUpdateStatus,
    ApplicationDetailResponse,
)


class IApplicationService(Protocol):
    def apply(self, student_id: uuid.UUID, data: ApplicationCreate) -> ApplicationResponse: ...
    def get_application(self, application_id: uuid.UUID) -> Optional[ApplicationResponse]: ...
    def update_status(
        self,
        application_id: uuid.UUID,
        student_id: uuid.UUID,
        data: ApplicationUpdateStatus,
    ) -> ApplicationResponse: ...
    def get_history(self, application_id: uuid.UUID, student_id: Optional[uuid.UUID] = None) -> List[ApplicationLogResponse]: ...


class ApplicationService:
    def __init__(
        self,
        application_repo: ApplicationRepository,
        application_log_repo: ApplicationLogRepository,
        student_repo: StudentRepository,
        placement_repo: PlacementRepository,
    ):
        self.application_repo = application_repo
        self.application_log_repo = application_log_repo
        self.student_repo = student_repo
        self.placement_repo = placement_repo

    def apply(self, student_id: uuid.UUID, data: ApplicationCreate) -> ApplicationResponse:
        student = self.student_repo.get_by_id(student_id)
        if not student:
            raise ValueError("Profil mahasiswa tidak ditemukan")
        if not student.cv_url:
            raise ValueError("Anda harus mengunggah CV sebelum melamar lowongan. Buka bagian Profil untuk mengunggah CV.")

        query = select(Applications).where(
            Applications.vacancy_id == data.vacancy_id,
            Applications.student_id == student_id,
        )
        existing = self.application_repo.session.scalars(query).first()
        if existing:
            raise ValueError("Anda sudah melamar ke lowongan ini")

        try:
            application = Applications(
                id=uuid.uuid4(),
                vacancy_id=data.vacancy_id,
                student_id=student_id,
                cv_snapshot_url=student.cv_url,
                status="APPLIED",
            )
            self.application_repo.create(application)
            self.application_repo.save_changes()
            return ApplicationResponse.model_validate(application)
        except Exception as exc:
            self.application_repo.rollback()
            raise exc

    def get_application(self, application_id: uuid.UUID) -> Optional[ApplicationResponse]:
        app = self.application_repo.get_by_id(application_id)
        return ApplicationResponse.model_validate(app) if app else None

    def update_status(
        self,
        application_id: uuid.UUID,
        student_id: uuid.UUID,
        data: ApplicationUpdateStatus,
    ) -> ApplicationResponse:
        app = self.application_repo.get_by_id(application_id)
        if not app:
            raise ValueError("Lamaran tidak ditemukan")
        if app.student_id != student_id:
            raise PermissionError("Bukan pemilik lamaran")

        old_status = app.status
        app.status = data.status
        app.updated_at = datetime.now(timezone.utc)

        log = ApplicationLogs(
            id=uuid.uuid4(),
            application_id=app.id,
            old_status=old_status,
            new_status=data.status,
            proof_url=data.proof_url,
            reason=data.reason,
            changed_at=datetime.now(timezone.utc),
        )
        self.application_log_repo.create(log)
        self.application_repo.save_changes()
        return ApplicationResponse.model_validate(app)

    def get_history(self, application_id: uuid.UUID, student_id: Optional[uuid.UUID] = None) -> List[ApplicationLogResponse]:
        app = self.application_repo.get_by_id(application_id)
        if not app:
            raise ValueError("Lamaran tidak ditemukan")
        if student_id and app.student_id != student_id:
            raise PermissionError("Bukan pemilik lamaran")

        query = (
            select(ApplicationLogs)
            .where(ApplicationLogs.application_id == application_id)
            .order_by(ApplicationLogs.changed_at.desc())
        )
        logs = self.application_log_repo.session.scalars(query).all()
        return [ApplicationLogResponse.model_validate(log) for log in logs]

    def list_pending_verification(self) -> List[ApplicationResponse]:
        query = select(Applications).where(Applications.status == "ACCEPTED")
        apps = self.application_repo.session.scalars(query).all()
        return [ApplicationResponse.model_validate(a) for a in apps]

    def get_my_applications(self, student_id: uuid.UUID) -> List[ApplicationDetailResponse]:
        from sqlalchemy.orm import joinedload
        from app_backend.models.vacancies import Vacancies

        query = (
            select(Applications)
            .options(joinedload(Applications.vacancy).joinedload(Vacancies.company))
            .where(Applications.student_id == student_id)
        )
        apps = self.application_repo.session.scalars(query).all()
        return [ApplicationDetailResponse.model_validate(a) for a in apps]
