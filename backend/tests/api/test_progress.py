from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.problem import Problem, Choice
from app.models.user import User


def test_submit_answer(
    client: TestClient, student_token_headers: dict, test_problem: Problem, db: Session
) -> None:
    """問題に回答を提出できることを確認"""
    # 問題の選択肢を取得
    choices = db.query(Choice).filter(Choice.problem_id == test_problem.id).all()
    correct_choice = next(c for c in choices if c.is_correct)
    
    # 回答を提出
    data = {
        "problem_id": str(test_problem.id),
        "selected_choice": str(correct_choice.id)
    }
    response = client.post("/api/v1/progress/submit", headers=student_token_headers, json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["problem_id"] == str(test_problem.id)
    assert result["selected_choice"] == str(correct_choice.id)
    assert result["is_correct"] is True
    assert "id" in result
    assert "user_id" in result
    assert "created_at" in result


def test_submit_answer_wrong_choice(
    client: TestClient, student_token_headers: dict, test_problem: Problem, db: Session
) -> None:
    """不正解の回答を提出できることを確認"""
    # 問題の選択肢を取得
    choices = db.query(Choice).filter(Choice.problem_id == test_problem.id).all()
    wrong_choice = next(c for c in choices if not c.is_correct)
    
    # 回答を提出
    data = {
        "problem_id": str(test_problem.id),
        "selected_choice": str(wrong_choice.id)
    }
    response = client.post("/api/v1/progress/submit", headers=student_token_headers, json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["is_correct"] is False


def test_submit_answer_invalid_choice(
    client: TestClient, student_token_headers: dict, test_problem: Problem
) -> None:
    """無効な選択肢で回答を提出するとエラーになることを確認"""
    data = {
        "problem_id": str(test_problem.id),
        "selected_choice": "00000000-0000-0000-0000-000000000000"  # 存在しないID
    }
    response = client.post("/api/v1/progress/submit", headers=student_token_headers, json=data)
    assert response.status_code == 400


def test_get_user_answers(
    client: TestClient, student_token_headers: dict, test_problem: Problem, db: Session,
    normal_user: User
) -> None:
    """ユーザーの回答履歴を取得できることを確認"""
    # まず回答を提出
    choices = db.query(Choice).filter(Choice.problem_id == test_problem.id).all()
    choice = choices[0]
    
    data = {
        "problem_id": str(test_problem.id),
        "selected_choice": str(choice.id)
    }
    client.post("/api/v1/progress/submit", headers=student_token_headers, json=data)
    
    # 回答履歴を取得
    response = client.get("/api/v1/progress/answers", headers=student_token_headers)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) > 0
    
    # 最新の回答が返されていることを確認
    latest_answer = result[0]
    assert latest_answer["problem_id"] == str(test_problem.id)
    assert latest_answer["user_id"] == str(normal_user.id)
    assert "selected_choice" in latest_answer
    assert "is_correct" in latest_answer
    assert "created_at" in latest_answer


def test_get_user_progress(
    client: TestClient, student_token_headers: dict, test_problem: Problem, db: Session,
    normal_user: User
) -> None:
    """ユーザーの学習進捗を取得できることを確認"""
    # まず回答を提出
    choices = db.query(Choice).filter(Choice.problem_id == test_problem.id).all()
    choice = choices[0]
    
    data = {
        "problem_id": str(test_problem.id),
        "selected_choice": str(choice.id)
    }
    client.post("/api/v1/progress/submit", headers=student_token_headers, json=data)
    
    # 学習進捗を取得
    response = client.get("/api/v1/progress/progress", headers=student_token_headers)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) > 0
    
    # 進捗が記録されていることを確認
    progress = result[0]
    assert progress["problem_id"] == str(test_problem.id)
    assert progress["user_id"] == str(normal_user.id)
    assert "attempts" in progress
    assert progress["attempts"] > 0
    assert "mastery_level" in progress
    assert "last_attempt_at" in progress


def test_get_user_stats(
    client: TestClient, student_token_headers: dict, test_problem: Problem, db: Session
) -> None:
    """ユーザーの統計情報を取得できることを確認"""
    # まず回答を提出
    choices = db.query(Choice).filter(Choice.problem_id == test_problem.id).all()
    choice = choices[0]
    
    data = {
        "problem_id": str(test_problem.id),
        "selected_choice": str(choice.id)
    }
    client.post("/api/v1/progress/submit", headers=student_token_headers, json=data)
    
    # 統計情報を取得
    response = client.get("/api/v1/progress/stats", headers=student_token_headers)
    assert response.status_code == 200
    result = response.json()
    
    # 統計情報の構造をチェック
    assert "total_problems" in result
    assert "attempted_problems" in result
    assert "mastered_problems" in result
    assert "completion_rate" in result
    assert "mastery_rate" in result
    assert "total_answers" in result
    assert "correct_answers" in result
    assert "correct_rate" in result
    
    # 少なくとも1問は挑戦済みであることを確認
    assert result["attempted_problems"] > 0
    assert result["total_answers"] > 0