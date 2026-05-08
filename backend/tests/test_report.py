import uuid
from datetime import date, timedelta
from unittest.mock import patch

from app_backend.models.placements import Placements

STUDENT_ID = uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")


def test_generate_report_success(client_as_student, mock_session):
    placement_id = uuid.uuid4()
    mock_placement = Placements(
        id=placement_id,
        student_id=STUDENT_ID,
        end_date=date.today() - timedelta(days=1),  # Sudah berakhir
        status="COMPLETED",
    )
    # mock_session.query(Placements).filter(...).first() returns mock_placement
    mock_session.query.return_value.filter.return_value.first.return_value = mock_placement

    with patch("app_backend.features.placement.generate_report.generate_final_report.delay") as mock_delay:
        resp = client_as_student.post(f"/api/v1/placements/{placement_id}/report/generate")

        assert resp.status_code == 202
        assert resp.json()["message"] == "Proses pembuatan laporan sedang berjalan di background"
        mock_delay.assert_called_once_with(str(placement_id))


def test_generate_report_ongoing_placement(client_as_student, mock_session):
    placement_id = uuid.uuid4()
    mock_placement = Placements(
        id=placement_id,
        student_id=STUDENT_ID,
        end_date=date.today() + timedelta(days=30),  # Belum berakhir
        status="ACTIVE",
    )
    mock_session.query.return_value.filter.return_value.first.return_value = mock_placement

    with patch("app_backend.features.placement.generate_report.generate_final_report.delay") as mock_delay:
        resp = client_as_student.post(f"/api/v1/placements/{placement_id}/report/generate")

        assert resp.status_code == 400
        assert "setelah masa magang selesai" in resp.json()["detail"]
        mock_delay.assert_not_called()


def test_get_report_status(client_as_student, mock_session):
    placement_id = uuid.uuid4()
    mock_placement = Placements(
        id=placement_id,
        student_id=STUDENT_ID,
        auto_generated_report_url="/uploads/reports/test.pdf",
    )
    mock_session.query.return_value.filter.return_value.first.return_value = mock_placement

    resp = client_as_student.get(f"/api/v1/placements/{placement_id}/report")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "generated"
    assert data["auto_generated_report_url"] == "/uploads/reports/test.pdf"


def test_get_report_status_not_generated(client_as_student, mock_session):
    placement_id = uuid.uuid4()
    mock_placement = Placements(id=placement_id, student_id=STUDENT_ID, auto_generated_report_url=None)
    mock_session.query.return_value.filter.return_value.first.return_value = mock_placement

    resp = client_as_student.get(f"/api/v1/placements/{placement_id}/report")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "not_generated"
    assert data["auto_generated_report_url"] is None


def test_generate_report_no_logs(mock_session):
    # Test task logic when no logs found
    placement_id = uuid.uuid4()
    mock_placement = Placements(id=placement_id, student_id=STUDENT_ID)

    with patch(
        "app_backend.shared.tasks.report_tasks.get_db_session",
        return_value=mock_session,
    ):
        # mock_session.query.filter.first() returns placement
        mock_session.query.return_value.filter.return_value.first.return_value = mock_placement
        # mock_session.query.filter.order_by.all() returns empty list (no logs)
        mock_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = []

        from app_backend.shared.tasks.report_tasks import generate_final_report

        result = generate_final_report(str(placement_id))

        assert result["status"] == "failed"
        assert result["error"] == "No activity logs found"


def test_generate_final_report_task_updates_url(mock_session):
    placement_id = uuid.uuid4()
    mock_placement = Placements(
        id=placement_id,
        student_id=STUDENT_ID,
        company_id=uuid.uuid4(),
        start_date=date.today() - timedelta(days=30),
        end_date=date.today(),
        auto_generated_report_url=None,
    )

    class MockLog:
        activity_date = date.today()
        duration_minutes = 120
        description_raw = "Mock description"

    with patch(
        "app_backend.shared.tasks.report_tasks.get_db_session",
        return_value=mock_session,
    ):
        with patch("app_backend.shared.tasks.report_tasks.SimpleDocTemplate.build"):
            mock_session.query.return_value.filter.return_value.first.return_value = mock_placement
            mock_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = [MockLog()]

            from app_backend.shared.tasks.report_tasks import generate_final_report

            result = generate_final_report(str(placement_id))

            assert result["status"] == "completed"
            assert result["url"] == f"/uploads/reports/report_{placement_id}.pdf"
            assert mock_placement.auto_generated_report_url == result["url"]
            assert mock_placement.last_report_generated_at is not None
            mock_session.commit.assert_called()
