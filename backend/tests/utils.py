import uuid
from typing import Dict, Optional

import jwt
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.services.auth import get_password_hash


def create_test_user(
    db: Session,
    email: str = "test@example.com",
    password: str = "password123",
    first_name: str = "Test",
    last_name: str = "User",
    role: str = "student",
    is_active: bool = True,
    is_verified: bool = True,
) -> User:
    """ユーザーをテスト用に作成する"""
    password_hash = get_password_hash(password)
    user = User(
        email=email,
        password_hash=password_hash,
        first_name=first_name,
        last_name=last_name,
        role=role,
        is_active=is_active,
        is_verified=is_verified,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_test_token(user_id: str, role: str = "student") -> str:
    """テスト用のJWTトークンを生成する"""
    payload = {
        "sub": str(user_id),
        "role": role,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def user_authentication_headers(
    client: TestClient, email: str, password: str
) -> Dict[str, str]:
    """ユーザー認証を行いヘッダーを取得する"""
    data = {"username": email, "password": password}
    r = client.post("/api/v1/auth/login", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_user(
    user: User, role: Optional[str] = None
) -> Dict[str, str]:
    """ユーザーからトークンを生成してヘッダーを作成する"""
    role = role or user.role
    token = create_test_token(user.id, role)
    return {"Authorization": f"Bearer {token}"}