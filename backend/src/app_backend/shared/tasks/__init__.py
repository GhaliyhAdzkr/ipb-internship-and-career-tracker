"""
Background Tasks Package.
Berisi task-task yang berjalan di background queue menggunakan Celery.
"""

# AI tasks
from app_backend.shared.tasks.ai_tasks import (  # noqa: F401
    enhance_log_description, match_job_skills, parse_cv_skills)
# Notification tasks
from app_backend.shared.tasks.notification_tasks import (  # noqa: F401
    cleanup_expired_tokens, send_email_notification)
# Vacancy tasks
from app_backend.shared.tasks.vacancy_tasks import (  # noqa: F401
    auto_close_expired_vacancies, scrape_vacancies)
