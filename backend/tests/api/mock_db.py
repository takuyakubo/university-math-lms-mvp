"""
データベースへの依存を取り除くためのモックユーティリティ
"""
from unittest.mock import MagicMock, patch
from uuid import UUID

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.db.base import get_db


class MockDB:
    """
    テスト用にSQLAlchemyセッションをモックするクラス
    アプリケーション全体で使用されるget_db依存関係を置き換える
    """
    def __init__(self):
        self.mock_db = MagicMock(spec=Session)
        self._setup()

    def _setup(self):
        """基本的なモックの設定"""
        # モックのDBセッションを設定
        self.mock_db.query.return_value.filter.return_value.first.return_value = None
        self.mock_db.query.return_value.filter.return_value.all.return_value = []
        self.mock_db.query.return_value.all.return_value = []
        
        # commit, add, refresh, deleteなどの操作が呼ばれるとき、何もしないようにモック
        self.mock_db.commit.return_value = None
        self.mock_db.add.return_value = None
        self.mock_db.refresh.return_value = None
        self.mock_db.delete.return_value = None
        
        # オフセット・リミットチェーンの設定
        self.mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = []
    
    def setup_mocks(self):
        """
        テスト中にget_db依存関係をこのモックに置き換える
        """
        # get_dbのパッチを作成
        db_patch = patch('app.db.base.get_db', self.get_mock_db)
        db_patch.start()
        
        # 他の場所でのget_dbの使用もモック
        api_auth_patch = patch('app.api.v1.endpoints.auth.get_db', self.get_mock_db)
        api_auth_patch.start()
        
        api_problems_patch = patch('app.api.v1.endpoints.problems.get_db', self.get_mock_db)
        api_problems_patch.start()
        
        api_progress_patch = patch('app.api.v1.endpoints.progress.get_db', self.get_mock_db)
        api_progress_patch.start()
        
        api_tags_patch = patch('app.api.v1.endpoints.tags.get_db', self.get_mock_db)
        api_tags_patch.start()
        
        api_users_patch = patch('app.api.v1.endpoints.users.get_db', self.get_mock_db)
        api_users_patch.start()
        
        services_auth_patch = patch('app.services.auth.get_db', self.get_mock_db)
        services_auth_patch.start()
        
        # 戻り値にパッチオブジェクトを含めて、テスト後にstop()できるようにする
        return [db_patch, api_auth_patch, api_problems_patch, api_progress_patch, 
                api_tags_patch, api_users_patch, services_auth_patch]
    
    def get_mock_db(self):
        """モックDBセッションのジェネレータ関数"""
        yield self.mock_db


# グローバルインスタンス
mock_db = MockDB()