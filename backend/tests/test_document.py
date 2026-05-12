import uuid
from datetime import datetime
from unittest.mock import patch

from app_backend.models.document_requests import DocumentRequests

STUDENT_ID = uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")


def test_request_document_success(client_as_student, mock_session):
    payload = {
        "document_type": "COVER_LETTER",
        "purpose": "Melamar posisi Data Analyst di PT Sejahtera",
    }

    # Mocking the session returning the object after add/commit/refresh is not strictly needed
    # since we just delay on doc_req.id, but we need to assign it an ID.
    def mock_refresh(obj):
        obj.id = uuid.uuid4()
        obj.created_at = datetime.now()

    mock_session.refresh.side_effect = mock_refresh

    with patch("app_backend.features.document.request_document.generate_cover_letter.delay") as mock_delay:
        resp = client_as_student.post("/api/v1/document-requests", json=payload)

        assert resp.status_code == 201
        data = resp.json()
        assert "document_id" in data
        assert data["message"] == "Permohonan surat berhasil diajukan dan sedang diproses"
        mock_delay.assert_called_once()


def test_list_documents(client_as_student, mock_session):
    doc_id = uuid.uuid4()
    mock_doc = DocumentRequests(
        id=doc_id,
        student_id=STUDENT_ID,
        document_type="COVER_LETTER",
        purpose="Testing List",
        status="COMPLETED",
        generated_url="/uploads/documents/test.pdf",
        created_at=datetime.now(),
    )
    mock_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = [mock_doc]

    resp = client_as_student.get("/api/v1/document-requests")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["document_type"] == "COVER_LETTER"
    assert data[0]["purpose"] == "Testing List"
    assert data[0]["generated_url"] == "/uploads/documents/test.pdf"


def test_get_document(client_as_student, mock_session):
    doc_id = uuid.uuid4()
    mock_doc = DocumentRequests(
        id=doc_id,
        student_id=STUDENT_ID,
        document_type="COVER_LETTER",
        purpose="Testing Get",
        status="PENDING",
        created_at=datetime.now(),
    )
    mock_session.query.return_value.filter.return_value.first.return_value = mock_doc

    resp = client_as_student.get(f"/api/v1/document-requests/{doc_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["document_type"] == "COVER_LETTER"
    assert data["purpose"] == "Testing Get"
    assert data["status"] == "PENDING"


def test_generate_cover_letter_task_updates_db(mock_session):
    doc_id = uuid.uuid4()
    mock_doc = DocumentRequests(
        id=doc_id,
        student_id=STUDENT_ID,
        purpose="Melamar kerja",
        status="PENDING",
        generated_url=None,
    )

    with patch(
        "app_backend.shared.tasks.report_tasks.get_db_session",
        return_value=mock_session,
    ):
        with patch("app_backend.shared.tasks.report_tasks.SimpleDocTemplate.build") as mock_build:
            mock_session.query.return_value.filter.return_value.first.return_value = mock_doc

            from app_backend.shared.tasks.report_tasks import generate_cover_letter

            result = generate_cover_letter(str(doc_id))

            assert result["status"] == "completed"
            assert f"letter_{doc_id}.pdf" in result["url"]
            assert mock_doc.generated_url == result["url"]
            assert mock_doc.status == "COMPLETED"

            # Memastikan fungsi render PDF terpanggil (menghasilkan file PDF dengan kop)
            mock_build.assert_called()
            mock_session.commit.assert_called()
