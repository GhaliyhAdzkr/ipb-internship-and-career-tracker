import os
import uuid
from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app_backend.models.activity_logs import ActivityLogs
from app_backend.models.placements import Placements

UPLOAD_DIR = "uploads/activity_logs"


@dataclass
class UploadActivityLogAttachmentCommand:
    placement_id: uuid.UUID
    log_id: uuid.UUID
    student_id: uuid.UUID
    file: UploadFile


@dataclass
class UploadActivityLogAttachmentResult:
    attachment_url: Optional[str] = None
    message: Optional[str] = None
    error_message: Optional[str] = None
    error_code: HTTPStatus = HTTPStatus.BAD_REQUEST

    def got_error(self) -> bool:
        return self.error_message is not None


def upload_activity_log_attachment_command_handler(
    command: UploadActivityLogAttachmentCommand,
    session: Session,
) -> UploadActivityLogAttachmentResult:
    # Validasi placement exists & belongs to student
    placement = session.query(Placements).filter_by(id=command.placement_id, student_id=command.student_id).first()
    if not placement:
        return UploadActivityLogAttachmentResult(error_message="Placement tidak ditemukan")

    # Validasi log exists
    log = session.query(ActivityLogs).filter_by(id=command.log_id, placement_id=placement.id).first()
    if not log:
        return UploadActivityLogAttachmentResult(error_message="Activity log tidak ditemukan")

    file = command.file
    filename = file.filename.lower()

    # Read the first 8 bytes for magic bytes validation
    header = file.file.read(8)
    file.file.seek(0)  # Reset pointer

    is_jpeg = header.startswith(b"\xff\xd8\xff")
    is_png = header.startswith(b"\x89PNG\r\n\x1a\n")
    is_pdf = header.startswith(b"%PDF-")

    if not (is_jpeg or is_png or is_pdf):
        return UploadActivityLogAttachmentResult(
            error_message="Format file tidak didukung atau terdeteksi sebagai malware. Hanya JPEG, PNG, dan PDF yang diizinkan.",
            error_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
        )

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    ext = os.path.splitext(filename)[1]
    unique_filename = f"log_{command.log_id}_{uuid.uuid4().hex[:8]}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    try:
        MAX_SIZE = 15 * 1024 * 1024  # 15MB
        size = 0

        with open(file_path, "wb") as buffer:
            while chunk := file.file.read(1024 * 1024):  # 1MB iterasi
                size += len(chunk)
                if size > MAX_SIZE:
                    buffer.close()
                    os.remove(file_path)
                    return UploadActivityLogAttachmentResult(error_message="Ukuran file melebihi batas maksimal 15MB")
                buffer.write(chunk)

        attachment_url = f"/uploads/activity_logs/{unique_filename}"

        log.attachment_url = attachment_url
        session.commit()

        return UploadActivityLogAttachmentResult(attachment_url=attachment_url, message="Lampiran berhasil diunggah")

    except Exception as exc:
        session.rollback()
        return UploadActivityLogAttachmentResult(error_message=f"Upload gagal: {exc}")
