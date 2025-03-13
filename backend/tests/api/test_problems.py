from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.problem import Problem


def test_read_problems(client: TestClient, student_token_headers: dict, test_problem: Problem) -> None:
    """問題一覧を取得できることを確認"""
    response = client.get("/api/v1/problems", headers=student_token_headers)
    assert response.status_code == 200
    result = response.json()
    assert "items" in result
    assert "total" in result
    assert result["total"] > 0
    items = result["items"]
    assert len(items) > 0
    
    # 問題の詳細をチェック
    problem = items[0]
    assert "id" in problem
    assert "title" in problem
    assert "problem_text" in problem
    assert "choices" in problem
    assert "tags" in problem
    
    # 選択肢の詳細をチェック
    choices = problem["choices"]
    assert len(choices) > 0
    choice = choices[0]
    assert "id" in choice
    assert "text" in choice
    assert "is_correct" in choice


def test_read_problem_detail(
    client: TestClient, student_token_headers: dict, test_problem: Problem
) -> None:
    """問題の詳細情報を取得できることを確認"""
    response = client.get(f"/api/v1/problems/{test_problem.id}", headers=student_token_headers)
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == str(test_problem.id)
    assert result["title"] == test_problem.title
    assert result["problem_text"] == test_problem.problem_text
    assert "choices" in result
    assert len(result["choices"]) == 2  # テスト問題には2つの選択肢がある


def test_create_problem_teacher(client: TestClient, teacher_token_headers: dict) -> None:
    """教員が問題を作成できることを確認"""
    data = {
        "title": "New Problem",
        "description": "Description of new problem",
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
        "tags": ["calculus", "integration"]
    }
    response = client.post("/api/v1/problems", headers=teacher_token_headers, json=data)
    assert response.status_code == 201
    result = response.json()
    assert result["title"] == data["title"]
    assert result["problem_text"] == data["problem_text"]
    assert result["difficulty"] == data["difficulty"]
    assert len(result["choices"]) == 2
    assert "calculus" in result["tags"]
    assert "integration" in result["tags"]


def test_create_problem_student(client: TestClient, student_token_headers: dict) -> None:
    """学生は問題を作成できないことを確認（権限エラー）"""
    data = {
        "title": "Student Problem",
        "problem_text": "Problem text",
        "difficulty": 3,
        "choices": [
            {
                "text": "Choice 1",
                "is_correct": True
            },
            {
                "text": "Choice 2",
                "is_correct": False
            }
        ]
    }
    response = client.post("/api/v1/problems", headers=student_token_headers, json=data)
    assert response.status_code == 403


def test_update_problem_teacher(
    client: TestClient, teacher_token_headers: dict, test_problem: Problem
) -> None:
    """教員が問題を更新できることを確認"""
    data = {
        "title": "Updated Problem Title",
        "difficulty": 2
    }
    response = client.put(
        f"/api/v1/problems/{test_problem.id}", headers=teacher_token_headers, json=data
    )
    assert response.status_code == 200
    result = response.json()
    assert result["title"] == data["title"]
    assert result["difficulty"] == data["difficulty"]
    # 更新していない項目は維持されていることを確認
    assert result["problem_text"] == test_problem.problem_text


def test_update_problem_student(
    client: TestClient, student_token_headers: dict, test_problem: Problem
) -> None:
    """学生は問題を更新できないことを確認（権限エラー）"""
    data = {
        "title": "Student Update",
    }
    response = client.put(
        f"/api/v1/problems/{test_problem.id}", headers=student_token_headers, json=data
    )
    assert response.status_code == 403


def test_add_choice_to_problem(
    client: TestClient, teacher_token_headers: dict, test_problem: Problem
) -> None:
    """教員が問題に選択肢を追加できることを確認"""
    data = {
        "text": "New choice",
        "is_correct": False
    }
    response = client.post(
        f"/api/v1/problems/{test_problem.id}/choices",
        headers=teacher_token_headers,
        json=data
    )
    assert response.status_code == 200
    result = response.json()
    assert result["text"] == data["text"]
    assert result["is_correct"] == data["is_correct"]
    assert result["problem_id"] == str(test_problem.id)


def test_nonexistent_problem(client: TestClient, student_token_headers: dict) -> None:
    """存在しない問題へのアクセスはエラーになることを確認"""
    response = client.get(
        "/api/v1/problems/00000000-0000-0000-0000-000000000000",
        headers=student_token_headers
    )
    assert response.status_code == 404