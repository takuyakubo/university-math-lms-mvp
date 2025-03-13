from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User


def test_register_user(client: TestClient) -> None:
    """ユーザー登録のテスト"""
    data = {
        "email": "newuser@example.com",
        "password": "password123",
        "first_name": "New",
        "last_name": "User",
        "role": "student",
    }
    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code == 201
    result = response.json()
    assert result["email"] == data["email"]
    assert result["first_name"] == data["first_name"]
    assert result["last_name"] == data["last_name"]
    assert result["role"] == data["role"]
    assert "id" in result
    assert "is_active" in result
    assert "is_verified" in result


def test_register_user_duplicate_email(client: TestClient, normal_user: User) -> None:
    """重複するメールアドレスでユーザー登録を行うとエラーになることを確認"""
    data = {
        "email": normal_user.email,  # 既に存在するメールアドレス
        "password": "password123",
        "first_name": "Another",
        "last_name": "User",
        "role": "student",
    }
    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_login_correct_password(client: TestClient, normal_user: User) -> None:
    """正しいパスワードでログインできることを確認"""
    data = {
        "username": normal_user.email,
        "password": "password123",
    }
    response = client.post("/api/v1/auth/login", data=data)
    assert response.status_code == 200
    result = response.json()
    assert "access_token" in result
    assert result["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, normal_user: User) -> None:
    """誤ったパスワードではログインできないことを確認"""
    data = {
        "username": normal_user.email,
        "password": "wrongpassword",
    }
    response = client.post("/api/v1/auth/login", data=data)
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_login_nonexistent_user(client: TestClient) -> None:
    """存在しないユーザーではログインできないことを確認"""
    data = {
        "username": "nonexistent@example.com",
        "password": "password123",
    }
    response = client.post("/api/v1/auth/login", data=data)
    assert response.status_code == 401


def test_test_token(client: TestClient, student_token_headers: dict) -> None:
    """トークンのテストエンドポイントが機能することを確認"""
    response = client.post("/api/v1/auth/test-token", headers=student_token_headers)
    assert response.status_code == 200
    result = response.json()
    assert "id" in result
    assert "email" in result
    assert "role" in result


def test_test_token_invalid_token(client: TestClient) -> None:
    """無効なトークンが拒否されることを確認"""
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.post("/api/v1/auth/test-token", headers=headers)
    assert response.status_code == 401