from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User


def test_read_users_teacher(client: TestClient, teacher_token_headers: dict) -> None:
    """教員がユーザー一覧を取得できることを確認"""
    response = client.get("/api/v1/users", headers=teacher_token_headers)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) > 0
    for user in result:
        assert "id" in user
        assert "email" in user
        assert "role" in user


def test_read_users_student(client: TestClient, student_token_headers: dict) -> None:
    """学生はユーザー一覧を取得できないことを確認（権限エラー）"""
    response = client.get("/api/v1/users", headers=student_token_headers)
    assert response.status_code == 403


def test_read_user_me(client: TestClient, student_token_headers: dict, normal_user: User) -> None:
    """自分自身のユーザー情報を取得できることを確認"""
    response = client.get("/api/v1/users/me", headers=student_token_headers)
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == str(normal_user.id)
    assert result["email"] == normal_user.email
    assert result["first_name"] == normal_user.first_name
    assert result["last_name"] == normal_user.last_name
    assert result["role"] == normal_user.role


def test_update_user_me(client: TestClient, student_token_headers: dict) -> None:
    """自分自身のユーザー情報を更新できることを確認"""
    data = {
        "first_name": "Updated",
        "last_name": "Name",
    }
    response = client.put("/api/v1/users/me", headers=student_token_headers, json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["first_name"] == data["first_name"]
    assert result["last_name"] == data["last_name"]


def test_read_user_by_id_teacher(
    client: TestClient, teacher_token_headers: dict, normal_user: User
) -> None:
    """教員が特定のユーザー情報を取得できることを確認"""
    response = client.get(f"/api/v1/users/{normal_user.id}", headers=teacher_token_headers)
    assert response.status_code == 200
    result = response.json()
    assert result["id"] == str(normal_user.id)
    assert result["email"] == normal_user.email


def test_read_user_by_id_student(
    client: TestClient, student_token_headers: dict, teacher_user: User
) -> None:
    """学生は他のユーザー情報を取得できないことを確認（権限エラー）"""
    response = client.get(f"/api/v1/users/{teacher_user.id}", headers=student_token_headers)
    assert response.status_code == 403


def test_update_user_by_id_teacher(
    client: TestClient, teacher_token_headers: dict, normal_user: User
) -> None:
    """教員が特定のユーザー情報を更新できることを確認"""
    data = {
        "first_name": "Teacher",
        "last_name": "Updated",
    }
    response = client.put(
        f"/api/v1/users/{normal_user.id}", headers=teacher_token_headers, json=data
    )
    assert response.status_code == 200
    result = response.json()
    assert result["first_name"] == data["first_name"]
    assert result["last_name"] == data["last_name"]


def test_update_nonexistent_user(client: TestClient, teacher_token_headers: dict) -> None:
    """存在しないユーザーの更新はエラーになることを確認"""
    data = {
        "first_name": "NonExistent",
    }
    response = client.put(
        "/api/v1/users/00000000-0000-0000-0000-000000000000",
        headers=teacher_token_headers,
        json=data,
    )
    assert response.status_code == 404