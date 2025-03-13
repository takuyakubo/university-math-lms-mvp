from typing import List, Optional, Tuple, Dict, Any
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.problem import Problem, Choice, Tag, ProblemTag
from app.models.user import User
from app.schemas.problem import ProblemCreate, ProblemUpdate


def get_problem_by_id(db: Session, problem_id: UUID) -> Optional[Problem]:
    return db.query(Problem).filter(Problem.id == problem_id).first()


def get_problems(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    tag: Optional[str] = None,
    difficulty: Optional[int] = None,
    search: Optional[str] = None
) -> Tuple[List[Problem], int]:
    query = db.query(Problem)
    
    # タグでフィルタリング
    if tag:
        query = query.join(Problem.tags).join(ProblemTag.tag).filter(Tag.name == tag)
    
    # 難易度でフィルタリング
    if difficulty:
        query = query.filter(Problem.difficulty == difficulty)
    
    # タイトルまたは説明で検索
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            Problem.title.ilike(search_term) | Problem.description.ilike(search_term)
        )
    
    # 合計数を取得
    total = query.count()
    
    # 選択肢とタグを事前にロード
    query = query.options(joinedload(Problem.choices), joinedload(Problem.tags).joinedload(ProblemTag.tag))
    
    # ページネーション
    problems = query.offset(skip).limit(limit).all()
    
    return problems, total


def create_problem(
    db: Session, 
    problem_create: ProblemCreate, 
    creator: User
) -> Problem:
    # 問題の作成
    db_problem = Problem(
        title=problem_create.title,
        description=problem_create.description,
        problem_text=problem_create.problem_text,
        difficulty=problem_create.difficulty,
        created_by=creator.id,
    )
    db.add(db_problem)
    db.flush()  # IDを生成するためにフラッシュ
    
    # 選択肢の作成
    for choice_data in problem_create.choices:
        db_choice = Choice(
            problem_id=db_problem.id,
            text=choice_data.text,
            is_correct=choice_data.is_correct,
        )
        db.add(db_choice)
    
    # タグの処理
    if problem_create.tags:
        for tag_name in problem_create.tags:
            # タグが存在するか確認
            db_tag = db.query(Tag).filter(Tag.name == tag_name).first()
            
            # タグが存在しない場合は作成
            if not db_tag:
                db_tag = Tag(
                    name=tag_name,
                    created_by=creator.id,
                )
                db.add(db_tag)
                db.flush()
            
            # 問題とタグの関連付け
            db_problem_tag = ProblemTag(
                problem_id=db_problem.id,
                tag_id=db_tag.id,
            )
            db.add(db_problem_tag)
    
    db.commit()
    db.refresh(db_problem)
    return db_problem


def update_problem(
    db: Session, 
    problem: Problem, 
    problem_update: ProblemUpdate
) -> Problem:
    update_data = problem_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(problem, key, value)
    
    db.add(problem)
    db.commit()
    db.refresh(problem)
    return problem


def delete_problem(db: Session, problem: Problem) -> bool:
    db.delete(problem)
    db.commit()
    return True


def add_choice_to_problem(
    db: Session, 
    problem: Problem, 
    text: str, 
    is_correct: bool = False
) -> Choice:
    db_choice = Choice(
        problem_id=problem.id,
        text=text,
        is_correct=is_correct,
    )
    db.add(db_choice)
    db.commit()
    db.refresh(db_choice)
    return db_choice


def update_choice(
    db: Session, 
    choice: Choice, 
    text: Optional[str] = None, 
    is_correct: Optional[bool] = None
) -> Choice:
    if text is not None:
        choice.text = text
    
    if is_correct is not None:
        choice.is_correct = is_correct
    
    db.add(choice)
    db.commit()
    db.refresh(choice)
    return choice


def delete_choice(db: Session, choice: Choice) -> bool:
    db.delete(choice)
    db.commit()
    return True


def get_problem_stats(db: Session, problem_id: UUID) -> Dict[str, Any]:
    """問題の統計情報を取得する"""
    from app.models.user_progress import UserAnswer
    
    # 合計回答数
    total_answers = db.query(func.count(UserAnswer.id)).filter(
        UserAnswer.problem_id == problem_id
    ).scalar()
    
    # 正解率
    correct_answers = db.query(func.count(UserAnswer.id)).filter(
        UserAnswer.problem_id == problem_id,
        UserAnswer.is_correct == True
    ).scalar()
    
    correct_rate = 0
    if total_answers > 0:
        correct_rate = correct_answers / total_answers
    
    # 各選択肢の選択率
    choices = db.query(Choice).filter(Choice.problem_id == problem_id).all()
    choice_stats = []
    
    for choice in choices:
        choice_count = db.query(func.count(UserAnswer.id)).filter(
            UserAnswer.selected_choice == choice.id
        ).scalar()
        
        choice_rate = 0
        if total_answers > 0:
            choice_rate = choice_count / total_answers
        
        choice_stats.append({
            "id": choice.id,
            "text": choice.text,
            "is_correct": choice.is_correct,
            "count": choice_count,
            "rate": choice_rate,
        })
    
    return {
        "total_answers": total_answers,
        "correct_answers": correct_answers,
        "correct_rate": correct_rate,
        "choice_stats": choice_stats,
    }