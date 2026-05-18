import datetime
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKeyConstraint, Index, String, Text, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app_backend.models.base import Base

if TYPE_CHECKING:
    from app_backend.models.users import Users


class UserRefreshTokens(Base):
    __tablename__ = "user_refresh_tokens"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
            name="user_refresh_tokens_user_id_fkey",
        ),
        Index("idx_refresh_tokens_user", "user_id"),
        Index("idx_refresh_tokens_hash", "token_hash"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    device_info: Mapped[Optional[str]] = mapped_column(Text)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)
    is_revoked: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text("false"))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text("CURRENT_TIMESTAMP"))

    # Relationships
    user: Mapped["Users"] = relationship("Users", back_populates="refresh_tokens")

    def is_valid(self) -> bool:
        # Cek apakah token masih valid (belum expired dan belum direvoke)
        import datetime as dt

        now = dt.datetime.now(dt.timezone.utc)
        expires = self.expires_at.replace(tzinfo=dt.timezone.utc) if self.expires_at.tzinfo is None else self.expires_at
        return not self.is_revoked and now < expires

    def revoke(self) -> None:
        # Revoke token ini
        self.is_revoked = True
