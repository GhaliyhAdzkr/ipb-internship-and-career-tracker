"""
Background tasks for generating PDF reports and documents.
"""

import datetime
import os
from typing import Dict

import pandas as pd
from celery import shared_task
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)
from sqlalchemy.orm import sessionmaker

from app_backend.models.activity_logs import ActivityLogs
from app_backend.models.document_requests import DocumentRequests
from app_backend.models.placements import Placements
from app_backend.shared.database import create_engine


def get_db_session():
    engine = create_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def generate_final_report(self, placement_id: str) -> Dict:
    """Generate final report PDF from activity logs using pandas and reportlab."""
    session = get_db_session()
    try:
        placement = (
            session.query(Placements).filter(Placements.id == placement_id).first()
        )
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
            data.append(
                {
                    "Date": log.activity_date,
                    "Duration": log.duration_minutes / 60.0,
                    "Description": log.description_raw,
                }
            )

        df = pd.DataFrame(data)
        df["Date"] = pd.to_datetime(df["Date"])

        # Aggregate data
        total_hours = df["Duration"].sum()
        _ = df.groupby(df["Date"].dt.isocalendar().week)["Duration"].sum().to_dict()

        # Generate PDF
        os.makedirs("uploads/reports", exist_ok=True)
        filename = f"report_{placement_id}.pdf"
        file_path = f"uploads/reports/{filename}"
        public_url = f"/uploads/reports/{filename}"

        doc = SimpleDocTemplate(str(file_path), pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        # Title
        title_style = ParagraphStyle(
            "TitleStyle", parent=styles["Heading1"], alignment=1
        )
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

        # Update Database
        placement.auto_generated_report_url = public_url
        placement.last_report_generated_at = datetime.datetime.now()
        session.commit()

        return {"status": "completed", "url": public_url, "total_hours": total_hours}

    except Exception as exc:
        session.rollback()
        raise self.retry(exc=exc)
    finally:
        session.close()


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def generate_cover_letter(self, request_id: str) -> Dict:
    """Generate cover letter PDF for document requests."""
    session = get_db_session()
    try:
        req = (
            session.query(DocumentRequests)
            .filter(DocumentRequests.id == request_id)
            .first()
        )
        if not req:
            return {"status": "failed", "error": "Request not found"}

        # Generate PDF
        os.makedirs("uploads/documents", exist_ok=True)
        filename = f"letter_{request_id}.pdf"
        file_path = f"uploads/documents/{filename}"
        public_url = f"/uploads/documents/{filename}"

        doc = SimpleDocTemplate(str(file_path), pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        # IPB Header mock
        header_style = ParagraphStyle(
            "HeaderStyle",
            parent=styles["Normal"],
            alignment=1,
            fontSize=14,
            fontName="Helvetica-Bold",
        )
        elements.append(Paragraph("INSTITUT PERTANIAN BOGOR", header_style))
        elements.append(
            Paragraph("Career Development and Assessment IPB", header_style)
        )
        elements.append(Spacer(1, 30))

        # Content
        elements.append(Paragraph("SURAT PENGANTAR / REKOMENDASI", styles["Heading2"]))
        elements.append(Spacer(1, 20))

        body_text = f"""
        Yang bertanda tangan di bawah ini menerangkan bahwa mahasiswa dengan ID <b>{req.student_id}</b> 
        adalah benar mahasiswa aktif Institut Pertanian Bogor.
        <br/><br/>
        Surat ini diberikan sebagai pengantar untuk keperluan: <b>{req.purpose}</b>.
        <br/><br/>
        Demikian surat pengantar ini dibuat untuk dapat dipergunakan sebagaimana mestinya.
        """
        elements.append(Paragraph(body_text, styles["Normal"]))
        elements.append(Spacer(1, 50))

        elements.append(
            Paragraph(
                "Bogor, " + datetime.datetime.now().strftime("%d %B %Y"),
                styles["Normal"],
            )
        )
        elements.append(Paragraph("Direktur Kemahasiswaan", styles["Normal"]))

        doc.build(elements)

        # Update Database
        req.generated_url = public_url
        req.status = "COMPLETED"
        session.commit()

        return {"status": "completed", "url": public_url}

    except Exception as exc:
        session.rollback()
        raise self.retry(exc=exc)
    finally:
        session.close()
