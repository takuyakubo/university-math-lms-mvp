from sqlalchemy import Column, ForeignKey, Boolean, Integer, Float, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class UserAnswer(BaseModel):
    """ユーザー回答モデル - ユーザーの問題回答履歴を管理"""
    __tablename__ = "user_answers"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.id", ondelete="CASCADE"), nullable=False)
    selected_choice = Column(UUID(as_uuid=True), ForeignKey("choices.id", ondelete="CASCADE"), nullable=False)
    is_correct = Column(Boolean, nullable=False)

    # リレーションシップ
    user = relationship("User", back_populates="answers")
    problem = relationship("Problem", back_populates="user_answers")
    choice = relationship("Choice", back_populates="user_answers")
    
    # インデックス
    __table_args__ = (
        Index("idx_user_answer_user_problem", user_id, problem_id),
    )

    def __repr__(self):
        return f"<UserAnswer(id={self.id}, user_id={self.user_id}, problem_id={self.problem_id}, is_correct={self.is_correct})>"


class UserProgress(BaseModel):
    """ユーザー進捗モデル - ユーザーの問題ごとの学習進捗を管理"""
    __tablename__ = "user_progress"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.id", ondelete="CASCADE"), nullable=False)
    attempts = Column(Integer, nullable=False, default=0)
    last_attempt_at = Column(DateTime, nullable=True)
    mastery_level = Column(Float, default=0)

    # リレーションシップ
    user = relationship("User", back_populates="progress")
    problem = relationship("Problem", back_populates="user_progress")

    # インデックス
    __table_args__ = (
        Index("idx_user_progress_user", user_id),
        Index("idx_user_progress_problem", problem_id),
        Index("idx_user_progress_user_problem", user_id, problem_id, unique=True),
    )

    def __repr__(self):
        return f"<UserProgress(user_id={self.user_id}, problem_id={self.problem_id}, attempts={self.attempts}, mastery_level={self.mastery_level})>"