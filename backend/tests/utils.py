"""
モックテスト用のユーティリティ関数
"""
import uuid
from typing import Dict
import jwt
from app.core.config import settings


def create_test_token(user_id: str, role: str = "student") -> str:
    """テスト用のJWTトークンを生成する"""
    payload = {
        "sub": str(user_id),
        "role": role,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def get_test_auth_headers(user_id: str = None, role: str = "student") -> Dict[str, str]:
    """テスト用の認証ヘッダーを生成する"""
    if user_id is None:
        user_id = str(uuid.uuid4())
    token = create_test_token(user_id, role)
    return {"Authorization": f"Bearer {token}"}