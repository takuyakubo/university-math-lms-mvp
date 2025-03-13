from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.problem import Choice, Problem
from app.models.user import User
from app.schemas.problem import (
    ChoiceCreate, 
    ChoiceResponse, 
    ProblemCreate, 
    ProblemList, 
    ProblemResponse, 
    ProblemUpdate
)
from app.services.auth import get_current_active_user, get_current_teacher
from app.services.problem import (
    add_choice_to_problem,
    create_problem,
    delete_choice,
    delete_problem,
    get_problem_by_id,
    get_problem_stats,
    get_problems,
    update_choice,
    update_problem,
)

router = APIRouter()


@router.get("", response_model=ProblemList)
def read_problems(
    skip: int = 0,
    limit: int = 20,
    tag: Optional[str] = None,
    difficulty: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    問題一覧を取得する
    """
    problems, total = get_problems(
        db, skip=skip, limit=limit, tag=tag, difficulty=difficulty, search=search
    )
    
    # レスポンス形式に変換
    problem_list = []
    for problem in problems:
        # タグの取得
        tags = [pt.tag.name for pt in problem.tags]
        
        # 問題データの構築
        problem_data = ProblemResponse(
            id=problem.id,
            title=problem.title,
            description=problem.description,
            problem_text=problem.problem_text,
            difficulty=problem.difficulty,
            created_by=problem.created_by,
            created_at=problem.created_at.isoformat(),
            choices=[
                ChoiceResponse(
                    id=choice.id,
                    problem_id=choice.problem_id,
                    text=choice.text,
                    is_correct=choice.is_correct,
                )
                for choice in problem.choices
            ],
            tags=tags,
        )
        problem_list.append(problem_data)
    
    return {"items": problem_list, "total": total}


@router.post("", response_model=ProblemResponse, status_code=status.HTTP_201_CREATED)
def create_new_problem(
    problem_in: ProblemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher),
) -> Any:
    """
    新しい問題を作成する (教員のみ)
    """
    problem = create_problem(db, problem_in, current_user)
    
    # タグの取得
    tags = [pt.tag.name for pt in problem.tags]
    
    # レスポンスの構築
    return ProblemResponse(
        id=problem.id,
        title=problem.title,
        description=problem.description,
        problem_text=problem.problem_text,
        difficulty=problem.difficulty,
        created_by=problem.created_by,
        created_at=problem.created_at.isoformat(),
        choices=[
            ChoiceResponse(
                id=choice.id,
                problem_id=choice.problem_id,
                text=choice.text,
                is_correct=choice.is_correct,
            )
            for choice in problem.choices
        ],
        tags=tags,
    )


@router.get("/{problem_id}", response_model=ProblemResponse)
def read_problem(
    problem_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    問題の詳細情報を取得する
    """
    problem = get_problem_by_id(db, problem_id)
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found",
        )
    
    # タグの取得
    tags = [pt.tag.name for pt in problem.tags]
    
    # レスポンスの構築
    return ProblemResponse(
        id=problem.id,
        title=problem.title,
        description=problem.description,
        problem_text=problem.problem_text,
        difficulty=problem.difficulty,
        created_by=problem.created_by,
        created_at=problem.created_at.isoformat(),
        choices=[
            ChoiceResponse(
                id=choice.id,
                problem_id=choice.problem_id,
                text=choice.text,
                is_correct=choice.is_correct,
            )
            for choice in problem.choices
        ],
        tags=tags,
    )


@router.put("/{problem_id}", response_model=ProblemResponse)
def update_problem_by_id(
    problem_id: str,
    problem_in: ProblemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher),
) -> Any:
    """
    問題を更新する (教員のみ)
    """
    problem = get_problem_by_id(db, problem_id)
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found",
        )
    
    problem = update_problem(db, problem, problem_in)
    
    # タグの取得
    tags = [pt.tag.name for pt in problem.tags]
    
    # レスポンスの構築
    return ProblemResponse(
        id=problem.id,
        title=problem.title,
        description=problem.description,
        problem_text=problem.problem_text,
        difficulty=problem.difficulty,
        created_by=problem.created_by,
        created_at=problem.created_at.isoformat(),
        choices=[
            ChoiceResponse(
                id=choice.id,
                problem_id=choice.problem_id,
                text=choice.text,
                is_correct=choice.is_correct,
            )
            for choice in problem.choices
        ],
        tags=tags,
    )


@router.delete("/{problem_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_problem_by_id(
    problem_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher),
) -> None:
    """
    問題を削除する (教員のみ)
    """
    problem = get_problem_by_id(db, problem_id)
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found",
        )
    
    delete_problem(db, problem)


@router.post("/{problem_id}/choices", response_model=ChoiceResponse)
def add_choice(
    problem_id: str,
    choice_in: ChoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher),
) -> Any:
    """
    問題に選択肢を追加する (教員のみ)
    """
    problem = get_problem_by_id(db, problem_id)
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found",
        )
    
    choice = add_choice_to_problem(
        db, problem, text=choice_in.text, is_correct=choice_in.is_correct
    )
    
    return ChoiceResponse(
        id=choice.id,
        problem_id=choice.problem_id,
        text=choice.text,
        is_correct=choice.is_correct,
    )


@router.put("/{problem_id}/choices/{choice_id}", response_model=ChoiceResponse)
def update_choice_by_id(
    problem_id: str,
    choice_id: str,
    choice_in: ChoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher),
) -> Any:
    """
    選択肢を更新する (教員のみ)
    """
    problem = get_problem_by_id(db, problem_id)
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found",
        )
    
    choice = db.query(Choice).filter(Choice.id == choice_id, Choice.problem_id == problem_id).first()
    if not choice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Choice not found",
        )
    
    choice = update_choice(
        db, choice, text=choice_in.text, is_correct=choice_in.is_correct
    )
    
    return ChoiceResponse(
        id=choice.id,
        problem_id=choice.problem_id,
        text=choice.text,
        is_correct=choice.is_correct,
    )


@router.delete("/{problem_id}/choices/{choice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_choice_by_id(
    problem_id: str,
    choice_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher),
) -> None:
    """
    選択肢を削除する (教員のみ)
    """
    problem = get_problem_by_id(db, problem_id)
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found",
        )
    
    choice = db.query(Choice).filter(Choice.id == choice_id, Choice.problem_id == problem_id).first()
    if not choice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Choice not found",
        )
    
    delete_choice(db, choice)


@router.get("/{problem_id}/stats", response_model=Dict)
def get_problem_statistics(
    problem_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_teacher),
) -> Any:
    """
    問題の統計情報を取得する (教員のみ)
    """
    problem = get_problem_by_id(db, problem_id)
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found",
        )
    
    stats = get_problem_stats(db, problem_id)
    return stats