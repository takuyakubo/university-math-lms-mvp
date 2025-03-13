from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.problem import Tag


def test_read_tags(client: TestClient, student_token_headers: dict, test_problem: object) -> None:
    """タグ一覧を取得できることを確認"""
    response = client.get("/api/v1/tags", headers=student_token_headers)
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) > 0
    
    # タグの詳細をチェック
    tag = result[0]
    assert "id" in tag
    assert "name" in tag
    assert "description" in tag
    assert "created_by" in tag


def test_create_tag_teacher(client: TestClient, teacher_token_headers: dict) -> None:
    """教員がタグを作成できることを確認"""
    data = {
        "name": "algebra",
        "description": "Algebra problems"
    }
    response = client.post("/api/v1/tags", headers=teacher_token_headers, json=data)
    assert response.status_code == 201
    result = response.json()
    assert result["name"] == data["name"]
    assert result["description"] == data["description"]
    assert "id" in result
    assert "created_by" in result


def test_create_tag_student(client: TestClient, student_token_headers: dict) -> None:
    """学生はタグを作成できないことを確認（権限エラー）"""
    data = {
        "name": "student_tag",
        "description": "Student created tag"
    }
    response = client.post("/api/v1/tags", headers=student_token_headers, json=data)
    assert response.status_code == 403


def test_create_duplicate_tag(client: TestClient, teacher_token_headers: dict, test_problem: object) -> None:
    """既に存在するタグ名で作成を試みるとエラーになることを確認"""
    # 既存タグを取得
    response = client.get("/api/v1/tags", headers=teacher_token_headers)
    existing_tag = response.json()[0]
    
    # 同じ名前のタグを作成しようとする
    data = {
        "name": existing_tag["name"],
        "description": "Duplicate tag"
    }
    response = client.post("/api/v1/tags", headers=teacher_token_headers, json=data)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_update_tag_teacher(client: TestClient, teacher_token_headers: dict) -> None:
    """教員がタグを更新できることを確認"""
    # 既存タグを取得
    response = client.get("/api/v1/tags", headers=teacher_token_headers)
    existing_tag = response.json()[0]
    
    # タグの説明を更新
    data = {
        "description": "Updated tag description"
    }
    response = client.put(
        f"/api/v1/tags/{existing_tag['id']}", headers=teacher_token_headers, json=data
    )
    assert response.status_code == 200
    result = response.json()
    assert result["description"] == data["description"]
    # 名前は維持されていることを確認
    assert result["name"] == existing_tag["name"]


def test_update_tag_student(client: TestClient, student_token_headers: dict) -> None:
    """学生はタグを更新できないことを確認（権限エラー）"""
    # 既存タグを取得
    response = client.get("/api/v1/tags", headers=student_token_headers)
    existing_tag = response.json()[0]
    
    # 学生がタグを更新しようとする
    data = {
        "description": "Student update"
    }
    response = client.put(
        f"/api/v1/tags/{existing_tag['id']}", headers=student_token_headers, json=data
    )
    assert response.status_code == 403