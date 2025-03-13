from sqlalchemy import Column, String, ForeignKey, UniqueConstraint, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class User(BaseModel):
    """ユーザーモデル - アプリケーションのユーザー情報を管理"""
    __tablename__ = "users"

    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)

    # リレーションシップ
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    created_problems = relationship("Problem", back_populates="creator", cascade="all, delete-orphan")
    created_tags = relationship("Tag", back_populates="creator")
    answers = relationship("UserAnswer", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")

    # インデックス
    __table_args__ = (
        Index("idx_user_email", email),
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"


class UserProfile(BaseModel):
    """ユーザープロファイルモデル - ユーザーの追加情報を管理"""
    __tablename__ = "user_profiles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    avatar_url = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    organization = Column(String(100), nullable=True)

    # リレーションシップ
    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile(id={self.id}, user_id={self.user_id})>"