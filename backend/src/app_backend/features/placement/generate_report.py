import uuid
from dataclasses import dataclass
from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.models.placements import Placements
from app_backend.shared.tasks.report_tasks import generate_final_report


@dataclass
class GenerateReportCommand:
    placement_id: uuid.UUID
    student_id: uuid.UUID


@dataclass
class GenerateReportResult:
    message: Optional[str] = None
    error_message: Optional[str] = None
    error_status_code: int = 400

    def got_error(self) -> bool:
        return self.error_message is not None


def generate_report_command_handler(
    command: GenerateReportCommand, session: Session
) -> GenerateReportResult:
    placement = (
        session.query(Placements)
        .filter(
            Placements.id == command.placement_id,
            Placements.student_id == command.student_id,
        )
        .first()
    )

    if not placement:
        return GenerateReportResult(
            error_message="Placement tidak ditemukan", error_status_code=404
        )

    if placement.end_date > date.today():
        return GenerateReportResult(
            error_message="Laporan hanya bisa di-generate setelah masa magang selesai",
            error_status_code=400,
        )

    # Trigger Celery Task
    generate_final_report.delay(str(placement.id))

    return GenerateReportResult(
        message="Proses pembuatan laporan sedang berjalan di background"
    )
