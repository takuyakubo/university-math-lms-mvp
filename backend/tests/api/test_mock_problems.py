import json
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_read_problems(client):
    """問題一覧取得APIのテスト（モック版）"""
    # 認証関連のモック
    with patch("app.services.auth.jwt.decode") as mock_decode:
        # JWTトークンのデコード結果をモック
        mock_decode.return_value = {
            "sub": "user_id",
            "exp": 999999999999,
            "role": "student"
        }
        
        # ユーザー取得をモック
        with patch("app.services.auth.get_db") as mock_get_db:
            # DBセッションをモック
            mock_db = MagicMock()
            mock_get_db.return_value.__next__.return_value = mock_db
            
            # クエリ結果をモック
            mock_user = MagicMock()
            mock_user.id = "user_id"
            mock_user.role = "student"
            mock_user.is_active = True
            mock_db.query.return_value.filter.return_value.first.return_value = mock_user
            
            # モック問題データ
            mock_problems = [
                MagicMock(
                    id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    title="積分の基本公式",
                    description="x^nの不定積分を求める問題",
                    problem_text="\\int x dx",
                    difficulty=3,
                    created_by="3fa85f64-5717-4562-b3fc-2c963f66afa7",
                    created_at="2023-01-01T00:00:00",
                    choices=[
                        MagicMock(
                            id="3fa85f64-5717-4562-b3fc-2c963f66afa8",
                            problem_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            text="\\frac{x^2}{2} + C",
                            is_correct=True,
                        ),
                        MagicMock(
                            id="3fa85f64-5717-4562-b3fc-2c963f66afa9",
                            problem_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            text="x^2 + C",
                            is_correct=False,
                        ),
                    ],
                    tags=[
                        MagicMock(tag=MagicMock(name="微分積分学")),
                        MagicMock(tag=MagicMock(name="不定積分")),
                    ],
                )
            ]
            
            # get_problems関数の戻り値
            mock_result = (mock_problems, 1)
            
            # 問題取得関数をモック
            with patch("app.api.v1.endpoints.problems.get_problems", return_value=mock_result):
                
                # APIリクエスト実行（認証を通すためのヘッダー付き）
                response = client.get(
                    "/api/v1/problems", 
                    headers={"Authorization": "Bearer fake_token"}
                )
                
                # レスポンスの検証
                assert response.status_code == 200
                result = response.json()
                assert "items" in result
                assert "total" in result
                assert result["total"] == 1
                assert len(result["items"]) == 1
                
                # 問題データの検証
                problem = result["items"][0]
                assert "id" in problem
                assert "title" in problem
                assert "problem_text" in problem
                assert "choices" in problem
                assert len(problem["choices"]) == 2


def test_create_problem(client):
    """問題作成APIのテスト（モック版）"""
    # 認証関連のモック
    with patch("app.services.auth.jwt.decode") as mock_decode:
        # JWTトークンのデコード結果をモック（教員権限）
        mock_decode.return_value = {
            "sub": "teacher_id",
            "exp": 999999999999,
            "role": "teacher"
        }
        
        # ユーザー取得をモック
        with patch("app.services.auth.get_db") as mock_get_db:
            # DBセッションをモック
            mock_db = MagicMock()
            mock_get_db.return_value.__next__.return_value = mock_db
            
            # クエリ結果をモック（教員ユーザー）
            mock_teacher = MagicMock()
            mock_teacher.id = "teacher_id"
            mock_teacher.role = "teacher"
            mock_teacher.is_active = True
            mock_db.query.return_value.filter.return_value.first.return_value = mock_teacher
            
            # テストデータ
            problem_data = {
                "title": "新しい問題",
                "description": "問題の説明",
                "problem_text": "\\int x^2 dx",
                "difficulty": 4,
                "choices": [
                    {
                        "text": "\\frac{x^3}{3} + C",
                        "is_correct": True
                    },
                    {
                        "text": "\\frac{x^2}{2} + C",
                        "is_correct": False
                    }
                ],
                "tags": ["微分積分学", "不定積分"]
            }
            
            # モック問題
            mock_problem = MagicMock(
                id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
                title=problem_data["title"],
                description=problem_data["description"],
                problem_text=problem_data["problem_text"],
                difficulty=problem_data["difficulty"],
                created_by="teacher_id",
                created_at="2023-01-01T00:00:00",
                choices=[
                    MagicMock(
                        id="3fa85f64-5717-4562-b3fc-2c963f66afa8",
                        problem_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        text=problem_data["choices"][0]["text"],
                        is_correct=problem_data["choices"][0]["is_correct"],
                    ),
                    MagicMock(
                        id="3fa85f64-5717-4562-b3fc-2c963f66afa9",
                        problem_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        text=problem_data["choices"][1]["text"],
                        is_correct=problem_data["choices"][1]["is_correct"],
                    ),
                ],
                tags=[
                    MagicMock(tag=MagicMock(name="微分積分学")),
                    MagicMock(tag=MagicMock(name="不定積分")),
                ],
            )
            
            # 問題作成関数をモック
            with patch("app.api.v1.endpoints.problems.create_problem", return_value=mock_problem):
                
                # APIリクエスト実行
                response = client.post(
                    "/api/v1/problems",
                    headers={"Authorization": "Bearer fake_token"},
                    json=problem_data
                )
                
                # レスポンスの検証
                assert response.status_code == 201
                result = response.json()
                assert result["title"] == problem_data["title"]
                assert result["problem_text"] == problem_data["problem_text"]
                assert result["difficulty"] == problem_data["difficulty"]
                assert len(result["choices"]) == 2