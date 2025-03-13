from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.problem import Problem, Choice
from app.models.user import User
from app.models.user_progress import UserAnswer, UserProgress


def submit_answer(
    db: Session, 
    user: User, 
    problem_id: UUID, 
    choice_id: UUID
) -> UserAnswer:
    # 選択肢の取得
    choice = db.query(Choice).filter(Choice.id == choice_id).first()
    if not choice or choice.problem_id != problem_id:
        raise ValueError("Invalid choice for this problem")
    
    # 回答の記録
    user_answer = UserAnswer(
        user_id=user.id,
        problem_id=problem_id,
        selected_choice=choice_id,
        is_correct=choice.is_correct,
    )
    db.add(user_answer)
    
    # 進捗の更新
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user.id,
        UserProgress.problem_id == problem_id
    ).first()
    
    if not progress:
        # 初回の場合は新規作成
        progress = UserProgress(
            user_id=user.id,
            problem_id=problem_id,
            attempts=1,
            last_attempt_at=datetime.utcnow(),
            mastery_level=1.0 if choice.is_correct else 0.0,
        )
        db.add(progress)
    else:
        # 既存の場合は更新
        progress.attempts += 1
        progress.last_attempt_at = datetime.utcnow()
        
        # 習熟度の計算 (簡易版)
        if choice.is_correct:
            # 正解の場合は習熟度を上げる (最大1.0)
            progress.mastery_level = min(1.0, progress.mastery_level + 0.2)
        else:
            # 不正解の場合は習熟度を下げる (最小0.0)
            progress.mastery_level = max(0.0, progress.mastery_level - 0.1)
        
        db.add(progress)
    
    db.commit()
    db.refresh(user_answer)
    return user_answer


def get_user_progress(
    db: Session, 
    user: User, 
    problem_id: Optional[UUID] = None
) -> List[UserProgress]:
    query = db.query(UserProgress).filter(UserProgress.user_id == user.id)
    
    if problem_id:
        query = query.filter(UserProgress.problem_id == problem_id)
    
    return query.all()


def get_user_answers(
    db: Session, 
    user: User, 
    problem_id: Optional[UUID] = None,
    limit: int = 10
) -> List[UserAnswer]:
    query = db.query(UserAnswer).filter(UserAnswer.user_id == user.id)
    
    if problem_id:
        query = query.filter(UserAnswer.problem_id == problem_id)
    
    return query.order_by(UserAnswer.created_at.desc()).limit(limit).all()


def get_user_stats(db: Session, user: User) -> Dict:
    # 合計問題数
    total_problems = db.query(func.count(Problem.id)).scalar()
    
    # 挑戦した問題数
    attempted_problems = db.query(func.count(UserProgress.problem_id.distinct())).filter(
        UserProgress.user_id == user.id
    ).scalar()
    
    # 習得した問題数 (習熟度0.8以上を習得とみなす)
    mastered_problems = db.query(func.count(UserProgress.problem_id.distinct())).filter(
        UserProgress.user_id == user.id,
        UserProgress.mastery_level >= 0.8
    ).scalar()
    
    # 合計回答数
    total_answers = db.query(func.count(UserAnswer.id)).filter(
        UserAnswer.user_id == user.id
    ).scalar()
    
    # 正解数
    correct_answers = db.query(func.count(UserAnswer.id)).filter(
        UserAnswer.user_id == user.id,
        UserAnswer.is_correct == True
    ).scalar()
    
    # 正解率
    correct_rate = 0
    if total_answers > 0:
        correct_rate = correct_answers / total_answers
    
    return {
        "total_problems": total_problems,
        "attempted_problems": attempted_problems,
        "mastered_problems": mastered_problems,
        "completion_rate": attempted_problems / total_problems if total_problems > 0 else 0,
        "mastery_rate": mastered_problems / total_problems if total_problems > 0 else 0,
        "total_answers": total_answers,
        "correct_answers": correct_answers,
        "correct_rate": correct_rate,
    }