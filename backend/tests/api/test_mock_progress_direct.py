"""
データベースに依存しないエンドポイントの直接テスト
"""
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import status, HTTPException
from pydantic import TypeAdapter

from app.api.v1.endpoints.progress import submit_problem_answer, read_user_answer_history, read_user_progress, read_user_statistics
from app.schemas.user_progress import UserAnswerCreate, UserAnswerResponse, UserProgressResponse


@pytest.fixture
def mock_uuid():
    return "123e4567-e89b-12d3-a456-426614174000"


@pytest.fixture
def mock_user():
    """モックユーザー"""
    user = MagicMock()
    user.id = UUID("123e4567-e89b-12d3-a456-426614174000")
    user.email = "test@example.com"
    user.role = "student"
    user.is_active = True
    return user


@pytest.fixture
def mock_problem():
    """モック問題"""
    problem = MagicMock()
    problem.id = UUID("123e4567-e89b-12d3-a456-426614174001")
    problem.title = "テスト問題"
    problem.problem_text = "\\int x dx"
    return problem


@pytest.fixture
def mock_choice_id():
    return "123e4567-e89b-12d3-a456-426614174002"


@pytest.fixture
def mock_db():
    """モックデータベースセッション"""
    return MagicMock()


def test_submit_problem_answer(mock_user, mock_db, mock_problem, mock_choice_id):
    """回答提出エンドポイントのテスト"""
    # 回答データ
    answer_in = UserAnswerCreate(
        problem_id=str(mock_problem.id),
        selected_choice=mock_choice_id
    )
    
    # get_problem_by_idのモック
    with patch("app.api.v1.endpoints.progress.get_problem_by_id", return_value=mock_problem):
        # submit_answerのモック
        with patch("app.api.v1.endpoints.progress.submit_answer") as mock_submit:
            # 戻り値のモック
            mock_answer = MagicMock()
            mock_answer.id = UUID("123e4567-e89b-12d3-a456-426614174003")
            mock_answer.user_id = mock_user.id
            mock_answer.problem_id = mock_problem.id
            mock_answer.selected_choice = UUID(mock_choice_id)
            mock_answer.is_correct = True
            mock_answer.created_at = datetime.now()
            
            # dictへの変換をサポート
            mock_answer.dict = lambda: {
                "id": str(mock_answer.id),
                "user_id": str(mock_answer.user_id),
                "problem_id": str(mock_answer.problem_id),
                "selected_choice": str(mock_answer.selected_choice),
                "is_correct": mock_answer.is_correct,
                "created_at": mock_answer.created_at.isoformat()
            }
            
            mock_submit.return_value = mock_answer
            
            # エンドポイント関数を直接呼び出し
            result = submit_problem_answer(answer_in, mock_db, mock_user)
            
            # 結果の検証
            assert hasattr(result, "id")
            assert hasattr(result, "problem_id")
            assert hasattr(result, "user_id")
            assert hasattr(result, "selected_choice")
            assert hasattr(result, "is_correct")
            assert result.is_correct is True


def test_submit_problem_answer_not_found(mock_user, mock_db, mock_problem, mock_choice_id):
    """存在しない問題への回答提出のテスト"""
    # 回答データ
    answer_in = UserAnswerCreate(
        problem_id=str(mock_problem.id),
        selected_choice=mock_choice_id
    )
    
    # 問題が見つからない場合
    with patch("app.api.v1.endpoints.progress.get_problem_by_id", return_value=None):
        # 例外が発生することを確認
        with pytest.raises(HTTPException) as exc_info:
            submit_problem_answer(answer_in, mock_db, mock_user)
        
        # 例外の詳細をチェック
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Problem not found" in exc_info.value.detail


def test_read_user_answer_history(mock_user, mock_db, mock_uuid, mock_problem, mock_choice_id):
    """ユーザーの回答履歴取得エンドポイントのテスト"""
    # get_user_answersのモック
    with patch("app.api.v1.endpoints.progress.get_user_answers") as mock_get_answers:
        # 回答データのモック
        answer_time = datetime.now()
        mock_answers = [
            {
                "id": mock_uuid,
                "user_id": str(mock_user.id),
                "problem_id": str(mock_problem.id),
                "selected_choice": mock_choice_id,
                "is_correct": True,
                "created_at": answer_time.isoformat()
            }
        ]
        
        user_answer_adapter = TypeAdapter(List[UserAnswerResponse])
        mock_get_answers.return_value = user_answer_adapter.validate_python(mock_answers)
        
        # エンドポイント関数を直接呼び出し
        result = read_user_answer_history(None, 10, mock_db, mock_user)
        
        # 結果の検証
        assert isinstance(result, list)
        assert len(result) > 0
        answer = result[0]
        assert hasattr(answer, "id")
        assert hasattr(answer, "user_id")
        assert hasattr(answer, "problem_id")
        assert hasattr(answer, "selected_choice")
        assert hasattr(answer, "is_correct")
        assert hasattr(answer, "created_at")


def test_read_user_progress(mock_user, mock_db, mock_uuid, mock_problem):
    """ユーザーの学習進捗取得エンドポイントのテスト"""
    # get_user_progressのモック
    with patch("app.api.v1.endpoints.progress.get_user_progress") as mock_get_progress:
        # 進捗データのモック
        last_attempt = datetime.now()
        mock_progress = [
            {
                "user_id": str(mock_user.id),
                "problem_id": str(mock_problem.id),
                "attempts": 3,
                "correct_attempts": 2,
                "mastery_level": 0.67,
                "last_attempt_at": last_attempt.isoformat()
            }
        ]
        
        user_progress_adapter = TypeAdapter(List[UserProgressResponse])
        mock_get_progress.return_value = user_progress_adapter.validate_python(mock_progress)
        
        # エンドポイント関数を直接呼び出し
        result = read_user_progress(None, mock_db, mock_user)
        
        # 結果の検証
        assert isinstance(result, list)
        assert len(result) > 0
        progress = result[0]
        # UserProgressResponseにidフィールドはない
        assert hasattr(progress, "user_id")
        assert hasattr(progress, "problem_id")
        assert hasattr(progress, "attempts")
        assert hasattr(progress, "mastery_level")
        assert hasattr(progress, "last_attempt_at")
        assert progress.attempts == 3
        assert progress.mastery_level == 0.67


def test_read_user_stats(mock_user, mock_db):
    """ユーザーの統計情報取得エンドポイントのテスト"""
    # get_user_statsのモック
    with patch("app.api.v1.endpoints.progress.get_user_stats") as mock_get_stats:
        # 統計情報のモック
        mock_stats = {
            "total_problems": 10,
            "attempted_problems": 5,
            "mastered_problems": 3,
            "completion_rate": 0.5,
            "mastery_rate": 0.3,
            "total_answers": 15,
            "correct_answers": 10,
            "correct_rate": 0.67
        }
        
        mock_get_stats.return_value = mock_stats
        
        # エンドポイント関数を直接呼び出し
        result = read_user_statistics(mock_db, mock_user)
        
        # 結果の検証
        assert isinstance(result, dict)
        assert "total_problems" in result
        assert "attempted_problems" in result
        assert "mastered_problems" in result
        assert "completion_rate" in result
        assert "mastery_rate" in result
        assert "total_answers" in result
        assert "correct_answers" in result
        assert "correct_rate" in result
        assert result["total_problems"] == 10
        assert result["attempted_problems"] == 5
        assert result["correct_answers"] == 10
        assert result["correct_rate"] == 0.67