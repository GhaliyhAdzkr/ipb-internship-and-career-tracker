from http import HTTPStatus
import uuid
from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from app_backend.models.placements import Placements


@dataclass
class GetReportCommand:
    placement_id: uuid.UUID
    student_id: uuid.UUID


@dataclass
class GetReportResult:
    auto_generated_report_url: Optional[str] = None
    status: Optional[str] = None
    error_message: Optional[str] = None
    error_status_code: HTTPStatus = HTTPStatus.BAD_REQUEST

    def got_error(self) -> bool:
        return self.error_message is not None


def get_report_command_handler(
    command: GetReportCommand, session: Session
) -> GetReportResult:
    placement = (
        session.query(Placements)
        .filter(
            Placements.id == command.placement_id,
            Placements.student_id == command.student_id,
        )
        .first()
    )

    if not placement:
        return GetReportResult(error_message="Placement tidak ditemukan")

    if placement.auto_generated_report_url:
        return GetReportResult(
            auto_generated_report_url=placement.auto_generated_report_url,
            status="generated",
        )
    else:
        return GetReportResult(status="not_generated")
