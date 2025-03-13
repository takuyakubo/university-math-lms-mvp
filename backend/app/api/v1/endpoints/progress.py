from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.user import User
from app.schemas.user_progress import UserAnswerCreate, UserAnswerResponse, UserProgressResponse
from app.services.auth import get_current_active_user
from app.services.problem import get_problem_by_id
from app.services.user_progress import (
    get_user_answers,
    get_user_progress,
    get_user_stats,
    submit_answer,
)

router = APIRouter()


@router.post("/submit", response_model=UserAnswerResponse)
def submit_problem_answer(
    answer_in: UserAnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    問題への回答を提出する
    """
    problem = get_problem_by_id(db, answer_in.problem_id)
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found",
        )
    
    try:
        user_answer = submit_answer(
            db, current_user, answer_in.problem_id, answer_in.selected_choice
        )
        return user_answer
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/answers", response_model=List[UserAnswerResponse])
def read_user_answer_history(
    problem_id: str = None,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    ユーザーの回答履歴を取得する
    """
    user_answers = get_user_answers(db, current_user, problem_id, limit)
    return user_answers


@router.get("/progress", response_model=List[UserProgressResponse])
def read_user_progress(
    problem_id: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    ユーザーの学習進捗を取得する
    """
    progress = get_user_progress(db, current_user, problem_id)
    return progress


@router.get("/stats", response_model=Dict)
def read_user_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    ユーザーの統計情報を取得する
    """
    stats = get_user_stats(db, current_user)
    return stats