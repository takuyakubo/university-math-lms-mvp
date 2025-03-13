"""
データベースに依存しないタグエンドポイントの直接テスト
"""
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import status, HTTPException

from app.api.v1.endpoints.tags import read_tags, create_tag, read_tag, update_tag, delete_tag
from app.schemas.tag import TagCreate, TagUpdate


@pytest.fixture
def mock_uuid():
    return "123e4567-e89b-12d3-a456-426614174000"


@pytest.fixture
def mock_student_user():
    """モック学生ユーザー"""
    user = MagicMock()
    user.id = UUID("123e4567-e89b-12d3-a456-426614174000")
    user.email = "student@example.com"
    user.role = "student"
    user.is_active = True
    return user


@pytest.fixture
def mock_teacher_user():
    """モック教員ユーザー"""
    user = MagicMock()
    user.id = UUID("123e4567-e89b-12d3-a456-426614174001")
    user.email = "teacher@example.com"
    user.role = "teacher"
    user.is_active = True
    return user


@pytest.fixture
def mock_tag():
    """モックタグ"""
    tag = MagicMock()
    tag.id = UUID("123e4567-e89b-12d3-a456-426614174002")
    tag.name = "微分積分学"
    tag.description = "微分と積分に関する問題"
    tag.created_by = UUID("123e4567-e89b-12d3-a456-426614174001")  # 教員のID
    tag.created_at = datetime.now()
    
    # dictへの変換をサポート
    tag.dict = lambda: {
        "id": str(tag.id),
        "name": tag.name,
        "description": tag.description,
        "created_by": str(tag.created_by),
        "created_at": tag.created_at.isoformat()
    }
    
    return tag


@pytest.fixture
def mock_db():
    """モックデータベースセッション"""
    return MagicMock()


def test_read_tags(mock_db, mock_student_user, mock_tag):
    """タグ一覧を取得できることをテスト"""
    # タグ一覧のモック
    mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = [mock_tag]
    
    # エンドポイント関数を直接呼び出し
    result = read_tags(0, 100, mock_db, mock_student_user)
    
    # 結果の検証
    assert isinstance(result, list)
    assert len(result) == 1
    tag = result[0]
    assert hasattr(tag, "id")
    assert hasattr(tag, "name")
    assert hasattr(tag, "description")
    assert hasattr(tag, "created_by")
    assert tag.name == "微分積分学"
    assert tag.description == "微分と積分に関する問題"


def test_create_tag(mock_db, mock_teacher_user):
    """教員がタグを作成できることをテスト"""
    # リクエストデータ
    tag_in = TagCreate(
        name="代数学",
        description="群論、環論、体論の問題"
    )
    
    # 既存タグのチェック（存在しない場合）
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # 新しいタグを作成
    created_tag = MagicMock()
    created_tag.id = UUID("123e4567-e89b-12d3-a456-426614174003")
    created_tag.name = tag_in.name
    created_tag.description = tag_in.description
    created_tag.created_by = mock_teacher_user.id
    created_tag.created_at = datetime.now()
    
    # refreshのモック
    def mock_refresh(tag):
        # refreshの役割を模倣
        for attr in ["id", "name", "description", "created_by", "created_at"]:
            setattr(tag, attr, getattr(created_tag, attr))
    
    mock_db.refresh.side_effect = mock_refresh
    
    # エンドポイント関数を直接呼び出し
    result = create_tag(tag_in, mock_db, mock_teacher_user)
    
    # add、commitが呼ばれたことを確認
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    
    # 結果の検証
    assert hasattr(result, "id")
    assert hasattr(result, "name")
    assert hasattr(result, "description")
    assert hasattr(result, "created_by")
    assert result.name == tag_in.name
    assert result.description == tag_in.description
    assert str(result.created_by) == str(mock_teacher_user.id)


def test_create_duplicate_tag(mock_db, mock_teacher_user, mock_tag):
    """既に存在するタグ名で作成を試みるとエラーになることを確認"""
    # リクエストデータ（既存タグと同名）
    tag_in = TagCreate(
        name=mock_tag.name,
        description="重複するタグの説明"
    )
    
    # 既存タグのチェック（同名タグが存在する）
    mock_db.query.return_value.filter.return_value.first.return_value = mock_tag
    
    # エンドポイント関数を呼び出すと例外が発生
    with pytest.raises(HTTPException) as exc_info:
        create_tag(tag_in, mock_db, mock_teacher_user)
    
    # 例外の詳細をチェック
    assert exc_info.value.status_code == 400
    assert "already exists" in exc_info.value.detail


def test_read_tag(mock_db, mock_student_user, mock_tag):
    """タグの詳細を取得できることをテスト"""
    # タグIDで検索
    mock_db.query.return_value.filter.return_value.first.return_value = mock_tag
    
    # エンドポイント関数を直接呼び出し
    result = read_tag(str(mock_tag.id), mock_db, mock_student_user)
    
    # 結果の検証
    assert hasattr(result, "id")
    assert hasattr(result, "name")
    assert hasattr(result, "description")
    assert str(result.id) == str(mock_tag.id)
    assert result.name == mock_tag.name
    assert result.description == mock_tag.description


def test_read_tag_not_found(mock_db, mock_student_user, mock_uuid):
    """存在しないタグIDで検索するとエラーになることをテスト"""
    # タグが見つからない場合
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # エンドポイント関数を呼び出すと例外が発生
    with pytest.raises(HTTPException) as exc_info:
        read_tag(mock_uuid, mock_db, mock_student_user)
    
    # 例外の詳細をチェック
    assert exc_info.value.status_code == 404
    assert "Tag not found" in exc_info.value.detail


def test_update_tag(mock_db, mock_teacher_user, mock_tag):
    """教員がタグを更新できることをテスト"""
    # 更新データ
    tag_in = TagUpdate(
        description="更新された説明"
    )
    
    # タグIDで検索
    mock_db.query.return_value.filter.return_value.first.return_value = mock_tag
    
    # エンドポイント関数を直接呼び出し
    result = update_tag(str(mock_tag.id), tag_in, mock_db, mock_teacher_user)
    
    # add、commitが呼ばれたことを確認
    mock_db.add.assert_called_once_with(mock_tag)
    mock_db.commit.assert_called_once()
    
    # 結果の検証
    assert hasattr(result, "description")
    assert result.description == tag_in.description
    assert result.name == mock_tag.name  # 名前は変更されていない


def test_update_tag_not_found(mock_db, mock_teacher_user, mock_uuid):
    """存在しないタグIDで更新を試みるとエラーになることをテスト"""
    # 更新データ
    tag_in = TagUpdate(
        description="更新された説明"
    )
    
    # タグが見つからない場合
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # エンドポイント関数を呼び出すと例外が発生
    with pytest.raises(HTTPException) as exc_info:
        update_tag(mock_uuid, tag_in, mock_db, mock_teacher_user)
    
    # 例外の詳細をチェック
    assert exc_info.value.status_code == 404
    assert "Tag not found" in exc_info.value.detail


def test_update_tag_name_conflict(mock_db, mock_teacher_user, mock_tag):
    """名前を変更する際に既存タグ名と衝突するとエラーになることをテスト"""
    # 既存タグ
    existing_tag = MagicMock()
    existing_tag.id = UUID("123e4567-e89b-12d3-a456-426614174003")  # 異なるID
    existing_tag.name = "線形代数"  # 既に使われている名前
    
    # 更新データ（既存タグの名前と衝突）
    tag_in = TagUpdate(
        name="線形代数"
    )
    
    # タグIDで検索
    mock_db.query.return_value.filter.return_value.first.side_effect = [
        mock_tag,  # 最初の呼び出し（更新対象のタグ）
        existing_tag  # 2回目の呼び出し（名前の重複チェック）
    ]
    
    # エンドポイント関数を呼び出すと例外が発生
    with pytest.raises(HTTPException) as exc_info:
        update_tag(str(mock_tag.id), tag_in, mock_db, mock_teacher_user)
    
    # 例外の詳細をチェック
    assert exc_info.value.status_code == 400
    assert "already exists" in exc_info.value.detail


def test_delete_tag(mock_db, mock_teacher_user, mock_tag):
    """教員がタグを削除できることをテスト"""
    # タグIDで検索
    mock_db.query.return_value.filter.return_value.first.return_value = mock_tag
    
    # エンドポイント関数を直接呼び出し
    result = delete_tag(str(mock_tag.id), mock_db, mock_teacher_user)
    
    # delete、commitが呼ばれたことを確認
    mock_db.delete.assert_called_once_with(mock_tag)
    mock_db.commit.assert_called_once()
    
    # 204 No Contentなので結果はNone
    assert result is None


def test_delete_tag_not_found(mock_db, mock_teacher_user, mock_uuid):
    """存在しないタグIDで削除を試みるとエラーになることをテスト"""
    # タグが見つからない場合
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    # エンドポイント関数を呼び出すと例外が発生
    with pytest.raises(HTTPException) as exc_info:
        delete_tag(mock_uuid, mock_db, mock_teacher_user)
    
    # 例外の詳細をチェック
    assert exc_info.value.status_code == 404
    assert "Tag not found" in exc_info.value.detail