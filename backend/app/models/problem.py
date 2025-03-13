from sqlalchemy import Column, String, ForeignKey, Boolean, Text, Integer, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class Problem(BaseModel):
    """問題モデル - 数学問題を管理"""
    __tablename__ = "problems"

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    problem_text = Column(Text, nullable=False)
    difficulty = Column(Integer, default=3)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # リレーションシップ
    creator = relationship("User", back_populates="created_problems")
    choices = relationship("Choice", back_populates="problem", cascade="all, delete-orphan")
    tags = relationship("ProblemTag", back_populates="problem", cascade="all, delete-orphan")
    user_answers = relationship("UserAnswer", back_populates="problem", cascade="all, delete-orphan")
    user_progress = relationship("UserProgress", back_populates="problem", cascade="all, delete-orphan")

    # インデックス
    __table_args__ = (
        Index("idx_problem_created_by", created_by),
    )

    def __repr__(self):
        return f"<Problem(id={self.id}, title={self.title}, difficulty={self.difficulty})>"


class Choice(BaseModel):
    """選択肢モデル - 問題の選択肢を管理"""
    __tablename__ = "choices"

    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.id", ondelete="CASCADE"), nullable=False)
    text = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)
    
    # リレーションシップ
    problem = relationship("Problem", back_populates="choices")
    user_answers = relationship("UserAnswer", back_populates="choice")

    def __repr__(self):
        return f"<Choice(id={self.id}, problem_id={self.problem_id}, is_correct={self.is_correct})>"


class Tag(BaseModel):
    """タグモデル - 問題のカテゴリ分類のためのタグを管理"""
    __tablename__ = "tags"

    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # リレーションシップ
    creator = relationship("User", back_populates="created_tags")
    problems = relationship("ProblemTag", back_populates="tag", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Tag(id={self.id}, name={self.name})>"


class ProblemTag(BaseModel):
    """問題タグ関連モデル - 問題とタグの多対多関連を管理"""
    __tablename__ = "problem_tags"

    problem_id = Column(UUID(as_uuid=True), ForeignKey("problems.id", ondelete="CASCADE"), nullable=False)
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), nullable=False)

    # リレーションシップ
    problem = relationship("Problem", back_populates="tags")
    tag = relationship("Tag", back_populates="problems")

    # インデックスと制約
    __table_args__ = (
        UniqueConstraint('problem_id', 'tag_id', name='uq_problem_tag'),
        Index("idx_problem_tag_problem", problem_id),
        Index("idx_problem_tag_tag", tag_id),
    )

    def __repr__(self):
        return f"<ProblemTag(problem_id={self.problem_id}, tag_id={self.tag_id})>"