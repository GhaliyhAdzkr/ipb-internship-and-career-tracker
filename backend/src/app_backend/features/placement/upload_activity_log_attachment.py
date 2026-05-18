import os
import uuid
from dataclasses import dataclass
from http import HTTPStatus
from typing import Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app_backend.models.activity_logs import ActivityLogs
from app_backend.models.placements import Placements
from app_backend.shared.s3_storage import get_s3_client, upload_fileobj
from app_backend.conf.settings import settings

UPLOAD_DIR = "activity_logs"


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

    ext = os.path.splitext(filename)[1]
    unique_filename = f"log_{command.log_id}_{uuid.uuid4().hex[:8]}{ext}"
    s3_key = f"{UPLOAD_DIR}/{unique_filename}"

    try:
        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0)

        MAX_SIZE = 15 * 1024 * 1024  # 15MB
        if file_size > MAX_SIZE:
            return UploadActivityLogAttachmentResult(error_message="Ukuran file melebihi batas maksimal 15MB")

        if settings.storage_type == "s3":
            s3_client = get_s3_client()
            success = upload_fileobj(s3_client, file.file, settings.s3_bucket, s3_key, content_type=file.content_type)
            if not success:
                return UploadActivityLogAttachmentResult(error_message="Gagal mengunggah lampiran ke storage S3")

            if "storage.supabase.co/storage/v1/s3" in settings.s3_endpoint:
                public_endpoint = settings.s3_endpoint.replace("/storage/v1/s3", "/storage/v1/object/public")
                attachment_url = f"{public_endpoint}/{settings.s3_bucket}/{s3_key}"
            else:
                attachment_url = f"{settings.s3_endpoint}/{settings.s3_bucket}/{s3_key}"
        else:
            os.makedirs(f"uploads/{UPLOAD_DIR}", exist_ok=True)
            file_path = os.path.join(f"uploads/{UPLOAD_DIR}", unique_filename)
            with open(file_path, "wb") as buffer:
                buffer.write(file.file.read())
            attachment_url = f"/uploads/{UPLOAD_DIR}/{unique_filename}"

        log.attachment_url = attachment_url
        session.commit()

        return UploadActivityLogAttachmentResult(attachment_url=attachment_url, message="Lampiran berhasil diunggah")

    except Exception as exc:
        session.rollback()
        return UploadActivityLogAttachmentResult(error_message=f"Upload gagal: {exc}")
