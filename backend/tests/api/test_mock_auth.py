import json
import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_register_user(client):
    """ユーザー登録APIのテスト（モック版）"""
    # テストデータ
    test_user = {
        "email": "test@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User",
        "role": "student"
    }
    
    # get_dbの依存関係をモック
    with patch("app.api.v1.endpoints.auth.get_db") as mock_get_db:
        # DBセッションをモック
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value.__next__.return_value = mock_db
        
        # ユーザー検索のモック化（存在しないユーザー）
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # DBに保存されるユーザーオブジェクトのモック
        mock_user = MagicMock()
        mock_user.id = "123e4567-e89b-12d3-a456-426614174000"
        mock_user.email = test_user["email"]
        mock_user.first_name = test_user["first_name"]
        mock_user.last_name = test_user["last_name"]
        mock_user.role = test_user["role"]
        mock_user.is_active = True
        mock_user.is_verified = False
        mock_user.created_at = datetime.utcnow()
        
        # パスワードハッシュ化のモック
        with patch("app.services.auth.get_password_hash", return_value="hashed_password"):
            # ユーザー作成モック
            with patch("app.services.user.get_password_hash", return_value="hashed_password"):
                # APIリクエスト実行（ユーザーモックをセット）
                with patch("app.services.user.User", return_value=mock_user):
                    response = client.post("/api/v1/auth/register", json=test_user)
                    
                    # レスポンスの検証
                    assert response.status_code == 201
                    result = response.json()
                    assert result["email"] == test_user["email"]
                    assert result["first_name"] == test_user["first_name"]
                    assert result["last_name"] == test_user["last_name"]
                    assert result["role"] == test_user["role"]


def test_login_user(client):
    """ユーザーログインAPIのテスト（モック版）"""
    # テストデータ
    login_data = {
        "username": "test@example.com",
        "password": "password123"
    }
    
    # get_dbの依存関係をモック
    with patch("app.api.v1.endpoints.auth.get_db") as mock_get_db:
        # DBセッションをモック
        mock_db = MagicMock(spec=Session)
        mock_get_db.return_value.__next__.return_value = mock_db
        
        # ユーザー認証のモック
        with patch("app.api.v1.endpoints.auth.authenticate_user") as mock_auth:
            # モックユーザー
            mock_user = MagicMock()
            mock_user.id = "123e4567-e89b-12d3-a456-426614174000"
            mock_user.role = "student"
            mock_auth.return_value = mock_user
            
            # トークン生成のモック
            with patch("app.api.v1.endpoints.auth.create_access_token") as mock_token:
                mock_token.return_value = "fake_token"
                
                # APIリクエスト実行
                response = client.post("/api/v1/auth/login", data=login_data)
                
                # レスポンスの検証
                assert response.status_code == 200
                result = response.json()
                assert result["access_token"] == "fake_token"
                assert result["token_type"] == "bearer"