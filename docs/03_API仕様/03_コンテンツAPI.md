# コンテンツAPI

このドキュメントでは、教材コンテンツに関するAPIエンドポイントの仕様を定義します。

## ベースURL

```
https://api.math-lms.example.com/v1
```

## 認証方式

- JWTトークンベースの認証
- `Authorization` ヘッダーに `Bearer {token}` 形式でトークンを指定

## エンドポイント一覧

### 1. 問題一覧取得

利用可能な問題の一覧を取得します。

- **URL**: `/problems`
- **メソッド**: `GET`
- **認証**: 必要

#### クエリパラメータ

| パラメータ | 必須 | デフォルト | 説明 |
|----------|------|-----------|------|
| limit | ✗ | 20 | 取得する問題の最大数 |
| offset | ✗ | 0 | 取得開始位置（ページネーション用） |
| tag | ✗ | - | 特定のタグに関連する問題のみをフィルタリング |
| difficulty | ✗ | - | 難易度によるフィルタリング（1-5） |
| created_by | ✗ | - | 特定のユーザーが作成した問題のみをフィルタリング |
| sort | ✗ | created_at:desc | ソート条件（title:asc、difficulty:desc など） |

#### レスポンス（成功）

- **ステータスコード**: `200 OK`

```json
{
  "status": "success",
  "problems": {
    "items": [
      {
        "id": "f1e2d3c4-b5a6-7890-abcd-1234567890ab",
        "title": "線形代数の基礎",
        "description": "行列の基本演算に関する問題です",
        "difficulty": 3,
        "tags": ["線形代数", "行列", "基礎"],
        "created_by": {
          "id": "a1b2c3d4-e5f6-7890-abcd-1234567890ab",
          "full_name": "鈴木 一郎"
        },
        "created_at": "2025-02-15T12:00:00Z"
      },
      {
        "id": "a9b8c7d6-e5f4-3210-abcd-1234567890ab",
        "title": "微分方程式入門",
        "description": "1階線形微分方程式を解く問題です",
        "difficulty": 4,
        "tags": ["微分方程式", "微積分", "応用"],
        "created_by": {
          "id": "b2c3d4e5-f6a7-8901-bcde-234567890123",
          "full_name": "田中 花子"
        },
        "created_at": "2025-02-20T09:30:00Z"
      }
      // ... 他の問題データ
    ],
    "total": 45,
    "limit": 20,
    "offset": 0
  }
}
```

#### レスポンス（失敗）

- **ステータスコード**: `400 Bad Request`

```json
{
  "status": "error",
  "message": "Invalid parameter",
  "errors": [
    {
      "field": "difficulty",
      "message": "Difficulty must be between 1 and 5"
    }
  ]
}
```

### 2. 問題詳細取得

特定の問題の詳細情報を取得します。

- **URL**: `/problems/{problem_id}`
- **メソッド**: `GET`
- **認証**: 必要

#### URL パラメータ

| パラメータ | 説明 |
|----------|------|
| problem_id | 対象問題のID（UUIDv4形式） |

#### クエリパラメータ

| パラメータ | 必須 | デフォルト | 説明 |
|----------|------|-----------|------|
| include_choices | ✗ | false | 選択肢情報を含めるかどうか |

#### レスポンス（成功）

- **ステータスコード**: `200 OK`

```json
{
  "status": "success",
  "problem": {
    "id": "f1e2d3c4-b5a6-7890-abcd-1234567890ab",
    "title": "線形代数の基礎",
    "description": "行列の基本演算に関する問題です",
    "problem_text": "次の行列 $A = \\begin{pmatrix} 2 & 1 \\\\ 3 & 4 \\end{pmatrix}$ の行列式を求めよ。",
    "difficulty": 3,
    "tags": ["線形代数", "行列", "基礎"],
    "created_by": {
      "id": "a1b2c3d4-e5f6-7890-abcd-1234567890ab",
      "full_name": "鈴木 一郎"
    },
    "created_at": "2025-02-15T12:00:00Z",
    "updated_at": "2025-02-15T12:00:00Z",
    "choices": [
      {
        "id": "c4d5e6f7-8901-abcd-ef23-456789012345",
        "text": "$5$",
        "is_correct": false
      },
      {
        "id": "d5e6f7g8-9012-abcd-ef34-567890123456",
        "text": "$8$",
        "is_correct": false
      },
      {
        "id": "e6f7g8h9-0123-abcd-ef45-678901234567",
        "text": "$5$",
        "is_correct": true
      },
      {
        "id": "f7g8h9i0-1234-abcd-ef56-789012345678",
        "text": "$-1$",
        "is_correct": false
      }
    ]
  }
}
```

#### レスポンス（失敗）

- **ステータスコード**: `404 Not Found`

```json
{
  "status": "error",
  "message": "Problem not found",
  "error_code": "PROBLEM_NOT_FOUND"
}
```

### 3. 問題作成

新しい問題を作成します。

- **URL**: `/problems`
- **メソッド**: `POST`
- **認証**: 必要
- **権限**: 教員ロールのみ

#### リクエスト本文

```json
{
  "title": "三角関数の基本",
  "description": "三角関数の基本的な性質に関する問題です",
  "problem_text": "次の式 $\\sin^2 x + \\cos^2 x$ の値として正しいものを選べ。",
  "difficulty": 2,
  "tags": ["三角関数", "基礎", "恒等式"],
  "choices": [
    {
      "text": "$0$",
      "is_correct": false
    },
    {
      "text": "$1$",
      "is_correct": true
    },
    {
      "text": "$\\pi$",
      "is_correct": false
    },
    {
      "text": "$2$",
      "is_correct": false
    }
  ]
}
```

| パラメータ | 型 | 必須 | 説明 |
|----------|---|------|------|
| title | string | ✓ | 問題のタイトル |
| description | string | ✗ | 問題の説明 |
| problem_text | string | ✓ | 問題文（LaTeX対応） |
| difficulty | integer | ✗ | 難易度（1-5） |
| tags | array of strings | ✗ | 問題に関連するタグ |
| choices | array of objects | ✓ | 選択肢のリスト |
| choices[].text | string | ✓ | 選択肢のテキスト（LaTeX対応） |
| choices[].is_correct | boolean | ✓ | 正解かどうか |

#### レスポンス（成功）

- **ステータスコード**: `201 Created`

```json
{
  "status": "success",
  "message": "Problem created successfully",
  "problem": {
    "id": "g2h3i4j5-k6l7-8901-mnop-234567890123",
    "title": "三角関数の基本",
    "description": "三角関数の基本的な性質に関する問題です",
    "problem_text": "次の式 $\\sin^2 x + \\cos^2 x$ の値として正しいものを選べ。",
    "difficulty": 2,
    "tags": ["三角関数", "基礎", "恒等式"],
    "created_by": {
      "id": "a1b2c3d4-e5f6-7890-abcd-1234567890ab",
      "full_name": "鈴木 一郎"
    },
    "created_at": "2025-03-10T14:25:00Z",
    "updated_at": "2025-03-10T14:25:00Z",
    "choices": [
      {
        "id": "h3i4j5k6-l7m8-9012-nopq-345678901234",
        "text": "$0$",
        "is_correct": false
      },
      {
        "id": "i4j5k6l7-m8n9-0123-opqr-456789012345",
        "text": "$1$",
        "is_correct": true
      },
      {
        "id": "j5k6l7m8-n9o0-1234-pqrs-567890123456",
        "text": "$\\pi$",
        "is_correct": false
      },
      {
        "id": "k6l7m8n9-o0p1-2345-qrst-678901234567",
        "text": "$2$",
        "is_correct": false
      }
    ]
  }
}
```

#### レスポンス（失敗）

- **ステータスコード**: `400 Bad Request`

```json
{
  "status": "error",
  "message": "Invalid problem data",
  "errors": [
    {
      "field": "choices",
      "message": "At least one choice must be marked as correct"
    }
  ]
}
```

または

- **ステータスコード**: `403 Forbidden`

```json
{
  "status": "error",
  "message": "Access denied",
  "error_code": "ACCESS_DENIED"
}
```

### 4. 問題更新

既存の問題を更新します。

- **URL**: `/problems/{problem_id}`
- **メソッド**: `PUT`
- **認証**: 必要
- **権限**: 教員ロールのみ（自分が作成した問題のみ更新可能）

#### URL パラメータ

| パラメータ | 説明 |
|----------|------|
| problem_id | 対象問題のID（UUIDv4形式） |

#### リクエスト本文

```json
{
  "title": "三角関数の基本（改訂版）",
  "description": "三角関数の基本的な性質と恒等式に関する問題です",
  "problem_text": "次の三角関数の恒等式 $\\sin^2 x + \\cos^2 x$ の値として常に成り立つものを選べ。",
  "difficulty": 2,
  "tags": ["三角関数", "基礎", "恒等式", "公式"],
  "choices": [
    {
      "id": "h3i4j5k6-l7m8-9012-nopq-345678901234",
      "text": "$0$",
      "is_correct": false
    },
    {
      "id": "i4j5k6l7-m8n9-0123-opqr-456789012345",
      "text": "$1$",
      "is_correct": true
    },
    {
      "id": "j5k6l7m8-n9o0-1234-pqrs-567890123456",
      "text": "$\\pi$",
      "is_correct": false
    },
    {
      "id": "k6l7m8n9-o0p1-2345-qrst-678901234567",
      "text": "$x$に依存する",
      "is_correct": false
    }
  ]
}
```

#### レスポンス（成功）

- **ステータスコード**: `200 OK`

```json
{
  "status": "success",
  "message": "Problem updated successfully",
  "problem": {
    "id": "g2h3i4j5-k6l7-8901-mnop-234567890123",
    "title": "三角関数の基本（改訂版）",
    "description": "三角関数の基本的な性質と恒等式に関する問題です",
    "problem_text": "次の三角関数の恒等式 $\\sin^2 x + \\cos^2 x$ の値として常に成り立つものを選べ。",
    "difficulty": 2,
    "tags": ["三角関数", "基礎", "恒等式", "公式"],
    "created_by": {
      "id": "a1b2c3d4-e5f6-7890-abcd-1234567890ab",
      "full_name": "鈴木 一郎"
    },
    "created_at": "2025-03-10T14:25:00Z",
    "updated_at": "2025-03-11T09:15:00Z",
    "choices": [
      {
        "id": "h3i4j5k6-l7m8-9012-nopq-345678901234",
        "text": "$0$",
        "is_correct": false
      },
      {
        "id": "i4j5k6l7-m8n9-0123-opqr-456789012345",
        "text": "$1$",
        "is_correct": true
      },
      {
        "id": "j5k6l7m8-n9o0-1234-pqrs-567890123456",
        "text": "$\\pi$",
        "is_correct": false
      },
      {
        "id": "k6l7m8n9-o0p1-2345-qrst-678901234567",
        "text": "$x$に依存する",
        "is_correct": false
      }
    ]
  }
}
```

#### レスポンス（失敗）

- **ステータスコード**: `404 Not Found`

```json
{
  "status": "error",
  "message": "Problem not found",
  "error_code": "PROBLEM_NOT_FOUND"
}
```

または

- **ステータスコード**: `403 Forbidden`

```json
{
  "status": "error",
  "message": "Access denied",
  "error_code": "ACCESS_DENIED"
}
```

### 5. タグ一覧取得

問題に関連付けられたタグの一覧を取得します。

- **URL**: `/tags`
- **メソッド**: `GET`
- **認証**: 必要

#### クエリパラメータ

| パラメータ | 必須 | デフォルト | 説明 |
|----------|------|-----------|------|
| limit | ✗ | 50 | 取得するタグの最大数 |
| offset | ✗ | 0 | 取得開始位置（ページネーション用） |
| sort | ✗ | name:asc | ソート条件（name:asc、created_at:desc など） |

#### レスポンス（成功）

- **ステータスコード**: `200 OK`

```json
{
  "status": "success",
  "tags": {
    "items": [
      {
        "id": "t1a2g3-4567-abcd-ef89-0123456789ab",
        "name": "三角関数",
        "description": "三角関数に関する問題",
        "problem_count": 15,
        "created_by": {
          "id": "a1b2c3d4-e5f6-7890-abcd-1234567890ab",
          "full_name": "鈴木 一郎"
        },
        "created_at": "2025-01-20T10:00:00Z"
      },
      {
        "id": "t2a3g4-5678-bcde-fa90-1234567890bc",
        "name": "線形代数",
        "description": "線形代数学に関する問題",
        "problem_count": 23,
        "created_by": {
          "id": "b2c3d4e5-f6a7-8901-bcde-234567890123",
          "full_name": "田中 花子"
        },
        "created_at": "2025-01-22T11:30:00Z"
      }
      // ... 他のタグデータ
    ],
    "total": 35,
    "limit": 50,
    "offset": 0
  }
}
```

## エラーコード一覧

| エラーコード | 説明 |
|------------|------|
| PROBLEM_NOT_FOUND | 指定された問題が存在しません |
| ACCESS_DENIED | このリソースへのアクセス権限がありません |
| INVALID_PARAMETER | リクエストパラメータが無効です |
| DUPLICATE_TAG | 同名のタグが既に存在します |
| VALIDATION_FAILED | 入力データのバリデーションに失敗しました |
