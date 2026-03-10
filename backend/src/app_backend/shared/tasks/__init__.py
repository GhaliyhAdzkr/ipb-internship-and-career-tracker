"""
Background Tasks Package.
Berisi task-task yang berjalan di background queue menggunakan Celery.
"""

# AI tasks
from app_backend.shared.tasks.ai_tasks import (  # noqa: F401
    enhance_log_description,
    parse_cv_skills,
    match_job_skills,
)

# Vacancy tasks
from app_backend.shared.tasks.vacancy_tasks import (  # noqa: F401
    auto_close_expired_vacancies,
    scrape_vacancies,
)

# Notification tasks
from app_backend.shared.tasks.notification_tasks import (  # noqa: F401
    send_email_notification,
    cleanup_expired_tokens,
)
