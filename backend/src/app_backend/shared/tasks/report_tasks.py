import datetime
import os
import io
import shutil
import tempfile
import zipfile
from typing import Dict
from xml.etree import ElementTree as ET

import pandas as pd
from celery import shared_task
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from sqlalchemy.orm import sessionmaker

from app_backend.models.activity_logs import ActivityLogs
from app_backend.models.document_requests import DocumentRequests
from app_backend.models.notification_queue import NotificationQueue
from app_backend.models.placements import Placements
from app_backend.shared.database import create_engine
from app_backend.shared.s3_storage import get_s3_client, upload_fileobj, generate_presigned_url
from app_backend.conf.settings import settings


def get_db_session():
    engine = create_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
ET.register_namespace("w", WORD_NS)


def _indonesian_date(value: datetime.datetime) -> str:
    months = [
        "Januari",
        "Februari",
        "Maret",
        "April",
        "Mei",
        "Juni",
        "Juli",
        "Agustus",
        "September",
        "Oktober",
        "November",
        "Desember",
    ]
    return f"{value.day} {months[value.month - 1]} {value.year}"


def _academic_period(value: datetime.datetime) -> tuple[str, str]:
    if value.month >= 8:
        return "Ganjil", f"{value.year}/{value.year + 1}"
    return "Genap", f"{value.year - 1}/{value.year}"


def _safe_text(value, fallback: str = "-") -> str:
    if value is None:
        return fallback
    text = str(value).strip()
    return text or fallback


def _docx_paragraph_text(paragraph: ET.Element) -> str:
    return "".join(node.text or "" for node in paragraph.findall(f".//{{{WORD_NS}}}t"))


def _set_paragraph_text(paragraph: ET.Element, text: str) -> None:
    text_nodes = paragraph.findall(f".//{{{WORD_NS}}}t")
    if not text_nodes:
        run = ET.SubElement(paragraph, f"{{{WORD_NS}}}r")
        text_node = ET.SubElement(run, f"{{{WORD_NS}}}t")
        text_nodes = [text_node]
    text_nodes[0].text = text
    if text.startswith(" ") or text.endswith(" "):
        text_nodes[0].set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    for node in text_nodes[1:]:
        node.text = ""


def _replace_after_label(paragraphs: list[ET.Element], label: str, value: str) -> bool:
    for paragraph in paragraphs:
        text = _docx_paragraph_text(paragraph)
        if text.strip().startswith(label):
            text_nodes = paragraph.findall(f".//{{{WORD_NS}}}t")
            for node in reversed(text_nodes):
                if "…" in (node.text or "") or "." in (node.text or ""):
                    node.text = value
                    return True
            if text_nodes:
                text_nodes[-1].text = value
                return True
    return False


def _build_cover_letter_context(req: DocumentRequests) -> dict[str, str]:
    now = datetime.datetime.now()
    student = req.student
    department = getattr(student, "department", None) if student else None
    vacancy = req.reference_vacancy
    company = getattr(vacancy, "company", None) if vacancy else None
    term, academic_year = _academic_period(now)

    purpose = _safe_text(req.purpose, "pendaftaran Magang Mandiri")
    company_name = _safe_text(getattr(company, "name", None), "perusahaan/instansi tujuan")

    return {
        "date": _indonesian_date(now),
        "department_name": _safe_text(getattr(department, "name", None), "Departemen"),
        "faculty_name": _safe_text(getattr(department, "faculty", None), "Fakultas"),
        "student_name": _safe_text(getattr(student, "full_name", None)),
        "nim": _safe_text(getattr(student, "nim", None)),
        "student_semester": _safe_text(getattr(student, "semester", None)),
        "purpose": purpose,
        "company_name": company_name,
        "academic_term": term,
        "academic_year": academic_year,
    }


def _render_cover_letter_docx(req: DocumentRequests) -> io.BytesIO:
    template_path = os.path.join(os.path.dirname(__file__), "..", "templates", "surat_base.docx")
    template_path = os.path.abspath(template_path)
    context = _build_cover_letter_context(req)

    with tempfile.TemporaryDirectory() as temp_dir:
        extracted_dir = os.path.join(temp_dir, "docx")
        output_path = os.path.join(temp_dir, "letter.docx")
        with zipfile.ZipFile(template_path, "r") as source_zip:
            source_zip.extractall(extracted_dir)

        document_path = os.path.join(extracted_dir, "word", "document.xml")
        tree = ET.parse(document_path)
        root = tree.getroot()
        paragraphs = root.findall(f".//{{{WORD_NS}}}p")

        for paragraph in paragraphs:
            text = _docx_paragraph_text(paragraph)
            if text.startswith("Bogor,"):
                _set_paragraph_text(paragraph, f"Bogor, {context['date']}")
                break

        for paragraph in paragraphs:
            text = _docx_paragraph_text(paragraph).strip()
            if text.startswith("Ketua "):
                _set_paragraph_text(paragraph, f"Ketua {context['department_name']}")
            elif text.startswith("Fakultas "):
                _set_paragraph_text(paragraph, context["faculty_name"])

        _replace_after_label(paragraphs, "Nama", context["student_name"])
        _replace_after_label(paragraphs, "NIM", context["nim"])
        _replace_after_label(paragraphs, "Semester", context["student_semester"])

        body_text = (
            "Mengajukan permohonan pembuatan Surat Keterangan Aktif Kuliah "
            f"untuk keperluan {context['purpose']} di {context['company_name']} "
            f"pada periode semester {context['academic_term']} TA {context['academic_year']}."
        )
        for paragraph in paragraphs:
            text = _docx_paragraph_text(paragraph)
            if "Mengajukan permohonan" in text or "engajukan permohonan" in text:
                _set_paragraph_text(paragraph, body_text)
                break

        signature_fields = [p for p in paragraphs if _docx_paragraph_text(p).strip().startswith("NIM")]
        if signature_fields:
            _set_paragraph_text(signature_fields[-1], f"NIM {context['nim']}")
        underline_fields = [p for p in paragraphs if ".........................................." in _docx_paragraph_text(p)]
        if underline_fields:
            _set_paragraph_text(underline_fields[-1], context["student_name"])

        tree.write(document_path, encoding="UTF-8", xml_declaration=True)

        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as output_zip:
            for folder, _, files in os.walk(extracted_dir):
                for filename in files:
                    file_path = os.path.join(folder, filename)
                    arcname = os.path.relpath(file_path, extracted_dir)
                    output_zip.write(file_path, arcname)

        buffer = io.BytesIO()
        with open(output_path, "rb") as generated_docx:
            shutil.copyfileobj(generated_docx, buffer)
        buffer.seek(0)
        return buffer


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def generate_final_report(self, placement_id: str) -> Dict:
    """Generate final report PDF from activity logs using pandas and reportlab."""
    session = get_db_session()
    try:
        placement = session.query(Placements).filter(Placements.id == placement_id).first()
        if not placement:
            return {"status": "failed", "error": "Placement not found"}

        logs = (
            session.query(ActivityLogs)
            .filter(ActivityLogs.placement_id == placement_id)
            .order_by(ActivityLogs.activity_date.asc())
            .all()
        )

        if not logs:
            return {"status": "failed", "error": "No activity logs found"}

        # Prepare data for pandas
        data = []
        for log in logs:
            duration_hours = getattr(log, "duration_hours", None)
            if duration_hours is None:
                duration_hours = float(getattr(log, "duration_minutes", 0)) / 60.0
            data.append(
                {
                    "Date": log.activity_date,
                    "Duration": float(duration_hours),
                    "Description": getattr(log, "description_ai_enhanced", None) or log.description_raw,
                }
            )

        df = pd.DataFrame(data)
        df["Date"] = pd.to_datetime(df["Date"])

        # Aggregate data
        total_hours = df["Duration"].sum()
        _ = df.groupby(df["Date"].dt.isocalendar().week)["Duration"].sum().to_dict()

        # Generate PDF
        filename = f"report_{placement_id}.pdf"

        # Use a BytesIO buffer instead of a file path
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        # Title
        title_style = ParagraphStyle("TitleStyle", parent=styles["Heading1"], alignment=1)
        elements.append(Paragraph("Laporan Akhir Magang (Format PPKI)", title_style))
        elements.append(Spacer(1, 20))

        # Student Info
        student_info = f"Mahasiswa ID: {placement.student_id}<br/>"
        student_info += f"Perusahaan ID: {placement.company_id}<br/>"
        student_info += f"Periode: {placement.start_date} s/d {placement.end_date}<br/>"
        student_info += f"Total Jam Magang: {total_hours:.2f} Jam"
        elements.append(Paragraph(student_info, styles["Normal"]))
        elements.append(Spacer(1, 20))

        # Logbook Table
        table_data = [["Tanggal", "Durasi (Jam)", "Kegiatan"]]
        for _, row in df.iterrows():
            date_str = row["Date"].strftime("%Y-%m-%d")
            table_data.append(
                [
                    date_str,
                    f"{row['Duration']:.2f}",
                    Paragraph(row["Description"], styles["Normal"]),
                ]
            )

        t = Table(table_data, colWidths=[80, 80, 300])
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )
        elements.append(t)

        doc.build(elements)

        # Seek back to beginning of buffer
        pdf_buffer.seek(0)

        # Determine upload path (PRIVATE)
        s3_key = f"reports/{filename}"

        if settings.storage_type == "s3":
            s3_client = get_s3_client()
            success = upload_fileobj(s3_client, pdf_buffer, settings.s3_bucket, s3_key, content_type="application/pdf")
            if not success:
                return {"status": "failed", "error": "Failed to upload to S3"}

            # Generate Presigned URL (Valid for 1 week)
            public_url = generate_presigned_url(s3_client, settings.s3_bucket, s3_key, expiration=604800)
        else:
            # Fallback to local
            os.makedirs("uploads/reports", exist_ok=True)
            file_path = f"uploads/reports/{filename}"
            with open(file_path, "wb") as f:
                f.write(pdf_buffer.read())
            public_url = f"/uploads/reports/{filename}"

        # Update Database
        placement.auto_generated_report_url = public_url
        placement.last_report_generated_at = datetime.datetime.now()

        # Trigger Notification
        notif = NotificationQueue(
            title="Laporan Akhir Siap",
            message="Laporan akhir magang Anda telah selesai di-generate. Silakan unduh dari dashboard.",
            user_id=(placement.student.user_id if hasattr(placement, "student") and placement.student else placement.student_id),
            channel="ALL",
            status="QUEUED",
        )
        session.add(notif)

        session.commit()

        return {"status": "completed", "url": public_url, "total_hours": total_hours}

    except Exception as exc:
        session.rollback()
        raise self.retry(exc=exc)
    finally:
        session.close()


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def generate_cover_letter(self, request_id: str) -> Dict:
    """Generate cover letter DOCX from the official department template."""
    session = get_db_session()
    try:
        req = session.query(DocumentRequests).filter(DocumentRequests.id == request_id).first()
        if not req:
            return {"status": "failed", "error": "Request not found"}

        filename = f"letter_{request_id}.docx"
        docx_buffer = _render_cover_letter_docx(req)
        s3_key = f"documents/{filename}"
        content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        if settings.storage_type == "s3":
            s3_client = get_s3_client()
            success = upload_fileobj(s3_client, docx_buffer, settings.s3_bucket, s3_key, content_type=content_type)
            if not success:
                return {"status": "failed", "error": "Failed to upload to S3"}

            # Generate Presigned URL (Valid for 1 week)
            public_url = generate_presigned_url(s3_client, settings.s3_bucket, s3_key, expiration=604800)
        else:
            # Fallback to local
            os.makedirs("uploads/documents", exist_ok=True)
            file_path = f"uploads/documents/{filename}"
            with open(file_path, "wb") as f:
                f.write(docx_buffer.read())
            public_url = f"/uploads/documents/{filename}"

        # Update Database
        req.generated_url = public_url
        req.status = "COMPLETED"

        # Trigger Notification
        notif = NotificationQueue(
            title="Surat Pengantar Selesai",
            message=f"Surat pengantar untuk keperluan '{req.purpose}' telah diterbitkan.",
            user_id=(req.student.user_id if hasattr(req, "student") and req.student else req.student_id),
            channel="ALL",
            status="QUEUED",
        )
        session.add(notif)

        session.commit()

        return {"status": "completed", "url": public_url}

    except Exception as exc:
        session.rollback()
        raise self.retry(exc=exc)
    finally:
        session.close()
