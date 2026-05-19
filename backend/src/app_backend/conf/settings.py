import os
from functools import cached_property

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """Konfigurasi aplikasi"""

    # Environment (development, staging, production)
    environment: str = os.getenv("ENVIRONMENT", "development")

    db_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/internship_career_tracker",
    )
    db_test_url: str = os.getenv(
        "DATABASE_TEST_URL",
        "postgresql://user:password@localhost:5432/internship_career_tracker_test",
    )

    session_auto_commit: bool = False
    session_auto_flush: bool = False

    # JWT Settings
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production-09876543210987654321")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "32"))

    # Password Reset Settings
    reset_password_token_expire_minutes: int = int(os.getenv("RESET_PASSWORD_TOKEN_EXPIRE_MINUTES", "15"))

    # SMTP / Resend Settings
    smtp_host: str = os.getenv("SMTP_HOST", "smtp.resend.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "465"))
    smtp_user: str = os.getenv("SMTP_USER", "resend")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    smtp_from_email: str = os.getenv("SMTP_FROM_EMAIL", "noreply@yourdomain.com")
    smtp_from_name: str = os.getenv("SMTP_FROM_NAME", "IPB Career Tracker")
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    # API Versioning
    api_version: str = "v1"
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
    create_tables_on_startup: bool = os.getenv("CREATE_TABLES_ON_STARTUP", "false").lower() in ("1", "true", "yes")

    # S3 / Supabase Storage settings
    storage_type: str = os.getenv("STORAGE_TYPE", "local")
    s3_endpoint: str = os.getenv("S3_ENDPOINT", "")
    s3_region: str = os.getenv("S3_REGION", "")
    s3_access_key_id: str = os.getenv("S3_ACCESS_KEY_ID", "")
    s3_secret_access_key: str = os.getenv("S3_SECRET_ACCESS_KEY", "")
    s3_bucket: str | None = os.getenv("S3_BUCKET", None)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment.lower() in ("development", "dev", "local")

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment.lower() in ("production", "prod")

    @cached_property
    def cors_origin_list(self) -> list[str]:
        origins = [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
        return origins or ["http://localhost:5173", "https://larascareers.my.id"]


settings = Settings()
