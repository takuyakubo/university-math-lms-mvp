"""
テスト設定ファイル。
データベース依存テストは使用せず、モックテスト（test_mock_*_direct.py）を使用します。
"""
import os
import sys
import pytest
from fastapi.testclient import TestClient

# モジュールパスの追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app

@pytest.fixture
def client():
    """シンプルなテストクライアント"""
    with TestClient(app) as c:
        yield c