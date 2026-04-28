"""
Tests for POST /api/v1/applications (Initialize External Apply)
"""

import uuid
from unittest.mock import MagicMock, patch

from tests.conftest import STUDENT_USER_ID, NOW

VACANCY_ID = uuid.UUID("11111111-1111-1111-1111-111111111111")
APPLICATION_ID = uuid.UUID("22222222-2222-2222-2222-222222222222")

APPLY_PAYLOAD = {
    "vacancy_id": str(VACANCY_ID),
}


# ─── Success ──────────────────────────────────────────────────────────────────


def test_initialize_apply_success(client_as_student):
    with patch(
        "app_backend.routers.api.application.initialize_apply_command_handler"
    ) as mock_handler:
        from app_backend.schemas.application import ApplicationResponse

        mock_handler.return_value = MagicMock(
            error_message=None,
            application=ApplicationResponse(
                id=APPLICATION_ID,
                vacancy_id=VACANCY_ID,
                student_id=STUDENT_USER_ID,
                cv_snapshot_url="https://example.com/cv.pdf",
                status="APPLIED",
            ),
        )
        resp = client_as_student.post("/api/v1/applications", json=APPLY_PAYLOAD)

    assert resp.status_code == 201
    data = resp.json()
    assert data["vacancy_id"] == str(VACANCY_ID)
    assert data["student_id"] == str(STUDENT_USER_ID)
    assert data["cv_snapshot_url"] == "https://example.com/cv.pdf"
    assert data["status"] == "APPLIED"


# ─── Business logic errors ────────────────────────────────────────────────────


def test_initialize_apply_no_cv(client_as_student):
    """Student has no CV uploaded yet."""
    with patch(
        "app_backend.routers.api.application.initialize_apply_command_handler"
    ) as mock_handler:
        mock_handler.return_value = MagicMock(
            error_message="You must upload a CV before applying to a vacancy.",
            application=None,
        )
        resp = client_as_student.post("/api/v1/applications", json=APPLY_PAYLOAD)

    assert resp.status_code == 400
    assert "CV" in resp.json()["detail"]


def test_initialize_apply_duplicate(client_as_student):
    """Student already applied to this vacancy."""
    with patch(
        "app_backend.routers.api.application.initialize_apply_command_handler"
    ) as mock_handler:
        mock_handler.return_value = MagicMock(
            error_message="You have already applied to this vacancy.",
            application=None,
        )
        resp = client_as_student.post("/api/v1/applications", json=APPLY_PAYLOAD)

    assert resp.status_code == 400
    assert "already applied" in resp.json()["detail"]


# ─── Validation errors ────────────────────────────────────────────────────────


def test_initialize_apply_missing_vacancy_id(client_as_student):
    """Request body is missing vacancy_id entirely."""
    resp = client_as_student.post("/api/v1/applications", json={})

    assert resp.status_code == 422


def test_initialize_apply_invalid_vacancy_id(client_as_student):
    """vacancy_id is not a valid UUID."""
    resp = client_as_student.post(
        "/api/v1/applications", json={"vacancy_id": "not-a-uuid"}
    )

    assert resp.status_code == 422


# ─── Authorization ────────────────────────────────────────────────────────────


def test_initialize_apply_as_admin_forbidden(client_as_admin_for_student_only):
    """Admin cannot access this student-only endpoint."""
    resp = client_as_admin_for_student_only.post(
        "/api/v1/applications", json=APPLY_PAYLOAD
    )

    assert resp.status_code == 403


def test_initialize_apply_unauthenticated(client_no_auth):
    """Request without a token is rejected."""
    resp = client_no_auth.post("/api/v1/applications", json=APPLY_PAYLOAD)

    assert resp.status_code == 401

# ─── Self-Reporting Pipeline ──────────────────────────────────────────────────

def test_update_application_status_success(client_as_student):
    with patch("app_backend.routers.api.application.update_application_status_command_handler") as mock_handler:
        from app_backend.schemas.application import ApplicationResponse
        mock_handler.return_value = MagicMock(
            got_error=lambda: False,
            application=ApplicationResponse(
                id=APPLICATION_ID,
                vacancy_id=VACANCY_ID,
                student_id=STUDENT_USER_ID,
                cv_snapshot_url="https://example.com/cv.pdf",
                status="INTERVIEW",
            )
        )
        resp = client_as_student.patch(f"/api/v1/applications/{APPLICATION_ID}/status", json={"status": "INTERVIEW"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "INTERVIEW"

def test_upload_application_proof_success(client_as_student):
    with patch("app_backend.routers.api.application.upload_application_proof_command_handler") as mock_handler:
        mock_handler.return_value = MagicMock(
            got_error=lambda: False,
            message="Bukti berhasil diunggah",
            proof_url="/uploads/proofs/test.pdf"
        )
        files = {"file": ("test.pdf", b"dummy content", "application/pdf")}
        resp = client_as_student.post(f"/api/v1/applications/{APPLICATION_ID}/proof", files=files)
    assert resp.status_code == 200
    assert resp.json()["proof_url"] == "/uploads/proofs/test.pdf"

def test_get_application_history_success(client_as_student):
    with patch("app_backend.routers.api.application.get_application_history_command_handler") as mock_handler:
        mock_handler.return_value = MagicMock(
            got_error=lambda: False,
            logs=[]
        )
        resp = client_as_student.get(f"/api/v1/applications/{APPLICATION_ID}/history")
    assert resp.status_code == 200
