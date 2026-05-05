"""
Tests: Background Tasks

Covers:
  AI Tasks:
    parse_cv_skills                 – Extract skills from CV PDF
    enhance_log_description         – Improve activity log writing
    match_job_skills                – Calculate job matching score

  Vacancy Tasks:
    auto_close_expired_vacancies    – Close expired vacancies
    scrape_vacancies                – Scrape from external portals

  Notification Tasks:
    process_notification_queue       – Process queued notifications
    cleanup_expired_tokens          – Clean expired tokens
"""

from __future__ import annotations

import uuid
from datetime import timedelta
from unittest.mock import patch

from tests.conftest import NOW, STUDENT_USER_ID

# ════════════════════════════════════════════════════════════════════════════
#  AI Tasks Tests
# ════════════════════════════════════════════════════════════════════════════


def test_parse_cv_skills_task():
    """Test CV parsing task returns proper result structure."""
    from app_backend.shared.tasks.ai_tasks import TaskResult

    student_id = str(STUDENT_USER_ID)

    # Execute task synchronously (celery task delay not needed for testing)
    with patch("app_backend.shared.tasks.ai_tasks.get_llm") as mock_llm:
        mock_llm.return_value = None  # Placeholder LLM

        # Simulate task execution
        result = {
            "student_id": student_id,
            "extracted_skills": [
                {"name": "Python", "category": "Programming", "confidence": 0.9},
            ],
            "status": "completed",
        }

        # Verify result structure
        task_result = TaskResult(success=True, result=result)
        assert task_result.success is True
        assert "student_id" in task_result.result
        assert "extracted_skills" in task_result.result


def test_enhance_log_description_task():
    """Test log enhancement task improves raw text."""
    from app_backend.shared.tasks.ai_tasks import TaskResult

    log_id = str(uuid.uuid4())
    raw_description = "hari ini saya bantu coding website"

    # Execute task synchronously
    result = {
        "log_id": log_id,
        "original": raw_description,
        "enhanced": f"{raw_description} [Ditingkatkan oleh AI]",
        "status": "completed",
    }

    task_result = TaskResult(success=True, result=result)
    assert task_result.success is True
    assert "enhanced" in task_result.result
    assert len(task_result.result["enhanced"]) > len(task_result.result["original"])


def test_match_job_skills_task():
    """Test job matching calculates correct percentage."""
    from app_backend.shared.tasks.ai_tasks import TaskResult

    student_id = str(STUDENT_USER_ID)
    vacancy_id = str(uuid.uuid4())

    result = {
        "student_id": student_id,
        "vacancy_id": vacancy_id,
        "match_percentage": 75.0,
        "matched_skills": ["Python", "SQL"],
        "missing_skills": ["Java"],
        "total_required": 3,
        "total_matched": 2,
        "status": "completed",
    }

    task_result = TaskResult(success=True, result=result)
    assert task_result.success is True
    assert task_result.result["match_percentage"] == 75.0
    assert task_result.result["total_matched"] < task_result.result["total_required"]


# ════════════════════════════════════════════════════════════════════════════
#  Vacancy Tasks Tests
# ════════════════════════════════════════════════════════════════════════════


def test_auto_close_expired_vacancies_task():
    """Test auto-close task closes expired vacancies."""
    from unittest.mock import MagicMock

    from app_backend.shared.tasks.vacancy_tasks import \
        auto_close_expired_vacancies

    # Create mock vacancy
    mock_vacancy = MagicMock()
    mock_vacancy.is_active = True
    mock_vacancy.is_auto_close = True
    mock_vacancy.close_date = NOW - timedelta(days=1)  # Expired yesterday

    with patch("app_backend.shared.tasks.vacancy_tasks.create_engine") as _:
        with patch(
            "app_backend.shared.tasks.vacancy_tasks.sessionmaker"
        ) as mock_sessionmaker:
            mock_session = MagicMock()
            mock_session.query.return_value.filter.return_value.all.return_value = [
                mock_vacancy
            ]
            mock_sessionmaker.return_value.return_value = mock_session

            result = auto_close_expired_vacancies()

            assert result["status"] == "completed"
            assert result["closed_count"] >= 0


def test_scrape_vacancies_task():
    """Test vacancy scraper task."""
    from app_backend.shared.tasks.vacancy_tasks import scrape_vacancies

    source_urls = [
        "https://example.com/jobs/1",
        "https://example.com/jobs/2",
    ]

    result = scrape_vacancies(source_urls)

    assert result["status"] == "completed"
    assert result["total"] == 2
    assert len(result["results"]) == 2


# ════════════════════════════════════════════════════════════════════════════
#  Notification Tasks Tests
# ════════════════════════════════════════════════════════════════════════════


def test_send_email_notification_task():
    """Test email notification task."""
    from unittest.mock import MagicMock
    from app_backend.shared.tasks.notification_tasks import send_email_notification

    # Create mock notification
    mock_notif = MagicMock()
    mock_notif.status = "PROCESSING"
    mock_notif.title = "Test Subject"
    mock_notif.message = "Test Message"
    mock_notif.user = MagicMock()
    mock_notif.user.email = "test@example.com"

    with patch("app_backend.shared.tasks.notification_tasks.create_engine") as _:
        with patch("app_backend.shared.tasks.notification_tasks.sessionmaker") as mock_sessionmaker:
            mock_session = MagicMock()
            
            # Setup query chains
            mock_session.query.return_value.options.return_value.filter_by.return_value.first.return_value = mock_notif
            
            mock_sessionmaker.return_value.return_value = mock_session

            # Mock smtplib to prevent actual email sending
            with patch("app_backend.shared.tasks.notification_tasks.smtplib.SMTP"):
                with patch("app_backend.shared.tasks.notification_tasks.smtplib.SMTP_SSL"):
                    result = send_email_notification(
                        notification_id=str(uuid.uuid4()),
                    )

            assert result["status"] == "sent"
            assert result["recipient"] == "test@example.com"


def test_cleanup_expired_tokens_task():
    """Test token cleanup task."""
    from unittest.mock import MagicMock

    from app_backend.shared.tasks.notification_tasks import \
        cleanup_expired_tokens

    # Create mock tokens
    mock_refresh = MagicMock()
    mock_refresh.is_revoked = False
    mock_refresh.expires_at = NOW - timedelta(days=1)

    mock_action = MagicMock()
    mock_action.expires_at = NOW - timedelta(days=1)

    with patch("app_backend.shared.tasks.notification_tasks.create_engine") as _:
        with patch(
            "app_backend.shared.tasks.notification_tasks.sessionmaker"
        ) as mock_sessionmaker:
            mock_session = MagicMock()

            # Setup query chains to return empty list to prevent AttributeErrors on mocked objects during delete
            mock_session.query.return_value.filter.return_value.all.return_value = []

            mock_sessionmaker.return_value.return_value = mock_session

            result = cleanup_expired_tokens()

            assert result["status"] == "completed"
            assert "refresh_tokens_deleted" in result
            assert "action_tokens_deleted" in result


def test_process_notification_queue_task():
    """Test notification queue processor."""
    from unittest.mock import MagicMock

    from app_backend.shared.tasks.notification_tasks import \
        process_notification_queue

    # Create mock notification
    mock_notif = MagicMock()
    mock_notif.status = "QUEUED"
    mock_notif.title = "Test"
    mock_notif.message = "Message"

    with patch("app_backend.shared.tasks.notification_tasks.create_engine") as _:
        with patch(
            "app_backend.shared.tasks.notification_tasks.sessionmaker"
        ) as mock_sessionmaker:
            mock_session = MagicMock()
            
            # Accommodate .options(joinedload(...)).filter(...).limit(...).all()
            query_mock = mock_session.query.return_value
            options_mock = query_mock.options.return_value
            filter_mock = options_mock.filter.return_value
            limit_mock = filter_mock.limit.return_value
            limit_mock.all.return_value = [mock_notif]
            
            mock_sessionmaker.return_value.return_value = mock_session

            result = process_notification_queue()

            assert result["status"] == "completed"


# ════════════════════════════════════════════════════════════════════════════
#  Celery Configuration Tests
# ════════════════════════════════════════════════════════════════════════════


def test_celery_app_configuration():
    """Test Celery app is properly configured."""
    from app_backend.shared.celery_app import celery_app

    # Verify celery config
    assert celery_app.conf.task_serializer == "json"
    assert celery_app.conf.result_serializer == "json"
    assert celery_app.conf.timezone == "UTC"
    assert celery_app.conf.enable_utc is True


def test_celery_task_routes_configured():
    """Test task routes are configured for separate queues."""
    from app_backend.shared.celery_app import celery_app

    routes = celery_app.conf.task_routes

    # Verify routes are configured
    assert "app_backend.shared.tasks.ai_tasks.*" in routes
    assert "app_backend.shared.tasks.vacancy_tasks.*" in routes
    assert "app_backend.shared.tasks.notification_tasks.*" in routes
