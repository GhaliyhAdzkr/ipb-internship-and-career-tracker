from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, String, DateTime, Enum, text, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship

from app_backend.shared.database import Base


class Users(Base):
    """ORM Model for users table"""
    
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key')
    )

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum('ADMIN', 'STUDENT', 'COMPANY', 'LECTURER', name='user_role_enum'), nullable=False)
    is_active = Column(Boolean, server_default=text('true'))
    last_login_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'))

    notification_queue = relationship('NotificationQueue', back_populates='user')
    
    def to_domain(self):
        """Convert ORM model to domain model"""
        from app_backend.domain.user import User
        
        return User(
            id=self.id,
            email=self.email,
            password_hash=self.password_hash,
            role=self.role,
            is_active=self.is_active if self.is_active is not None else True,
            last_login_at=self.last_login_at,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @staticmethod
    def from_domain(user):
        """Create ORM model from domain model"""
        return Users(
            id=user.id,
            email=user.email,
            password_hash=user.password_hash,
            role=user.role,
            is_active=user.is_active,
            last_login_at=user.last_login_at,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
