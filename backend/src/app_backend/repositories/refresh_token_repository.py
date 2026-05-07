from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app_backend.models.user_refresh_tokens import UserRefreshTokens
from app_backend.repositories.base import BaseRepository
from app_backend.shared.security import hash_token


class RefreshTokenRepository(BaseRepository[UserRefreshTokens]):
    def __init__(self, session: Session):
        super().__init__(UserRefreshTokens, session)

    def get_by_token(self, token: str) -> Optional[UserRefreshTokens]:
        token_hash = hash_token(token)
        query = select(UserRefreshTokens).where(
            UserRefreshTokens.token_hash == token_hash,
            not UserRefreshTokens.is_revoked,
        )
        return self.session.scalars(query).first()

    def revoke_all_for_user(self, user_id) -> None:
        query = select(UserRefreshTokens).where(
            UserRefreshTokens.user_id == user_id,
            not UserRefreshTokens.is_revoked,
        )
        tokens = self.session.scalars(query).all()
        for token in tokens:
            token.is_revoked = True
        self.session.flush()
