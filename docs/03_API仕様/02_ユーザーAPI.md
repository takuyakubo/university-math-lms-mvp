# ユーザーAPI

このドキュメントでは、ユーザー管理に関するAPIエンドポイントの仕様を定義します。

## ベースURL

```
https://api.math-lms.example.com/v1
```

## 認証方式

- JWTトークンベースの認証
- `Authorization` ヘッダーに `Bearer {token}` 形式でトークンを指定

## エンドポイント一覧

### 1. ユーザープロフィール取得

ユーザーの詳細プロフィール情報を取得します。

- **URL**: `/users/{user_id}/profile`
- **メソッド**: `GET`
- **認証**: 必要
- **権限**: 自分自身のプロフィールに対してのみアクセス可能（教員は全てのユーザープロフィールにアクセス可能）

#### URL パラメータ

| パラメータ | 説明 |
|----------|------|
| user_id | 対象ユーザーのID（UUIDv4形式） |

#### レスポンス（成功）

- **ステータスコード**: `200 OK`

```json
{
  "status": "success",
  "profile": {
    "user_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ab",
    "email": "user@example.com",
    "full_name": "山田 太郎",
    "role": "student",
    "avatar_url": "https://example.com/avatars/default.png",
    "bio": "数学科の学生です。線形代数を勉強中。",
    "organization": "○○大学理学部",
    "created_at": "2025-01-15T12:00:00Z",
    "updated_at": "2025-02-20T15:30:00Z"
  }
}
```

#### レスポンス（失敗）

- **ステータスコード**: `404 Not Found`

```json
{
  "status": "error",
  "message": "User profile not found",
  "error_code": "PROFILE_NOT_FOUND"
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

### 2. ユーザープロフィール更新

ユーザーのプロフィール情報を更新します。

- **URL**: `/users/{user_id}/profile`
- **メソッド**: `PUT`
- **認証**: 必要
- **権限**: 自分自身のプロフィールに対してのみ更新可能

#### URL パラメータ

| パラメータ | 説明 |
|----------|------|
| user_id | 対象ユーザーのID（UUIDv4形式） |

#### リクエスト本文

```json
{
  "full_name": "山田 太郎",
  "avatar_url": "https://example.com/avatars/user1.png",
  "bio": "数学科の学生です。線形代数と微分方程式を勉強中。",
  "organization": "○○大学理学部"
}
```

| パラメータ | 型 | 必須 | 説明 |
|----------|---|------|------|
| full_name | string | ✗ | ユーザーの氏名 |
| avatar_url | string | ✗ | プロフィール画像のURL |
| bio | string | ✗ | 自己紹介文 |
| organization | string | ✗ | 所属組織 |

#### レスポンス（成功）

- **ステータスコード**: `200 OK`

```json
{
  "status": "success",
  "message": "Profile updated successfully",
  "profile": {
    "user_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ab",
    "email": "user@example.com",
    "full_name": "山田 太郎",
    "role": "student",
    "avatar_url": "https://example.com/avatars/user1.png",
    "bio": "数学科の学生です。線形代数と微分方程式を勉強中。",
    "organization": "○○大学理学部",
    "created_at": "2025-01-15T12:00:00Z",
    "updated_at": "2025-03-10T09:45:00Z"
  }
}
```

#### レスポンス（失敗）

- **ステータスコード**: `404 Not Found`

```json
{
  "status": "error",
  "message": "User profile not found",
  "error_code": "PROFILE_NOT_FOUND"
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

### 3. ユーザーの学習進捗取得

ユーザーの学習進捗状況を取得します。

- **URL**: `/users/{user_id}/progress`
- **メソッド**: `GET`
- **認証**: 必要
- **権限**: 自分自身の進捗に対してのみアクセス可能（教員は全てのユーザー進捗にアクセス可能）

#### URL パラメータ

| パラメータ | 説明 |
|----------|------|
| user_id | 対象ユーザーのID（UUIDv4形式） |

#### クエリパラメータ

| パラメータ | 必須 | デフォルト | 説明 |
|----------|------|-----------|------|
| limit | ✗ | 20 | 取得する進捗データの最大数 |
| offset | ✗ | 0 | 取得開始位置（ページネーション用） |
| tag | ✗ | - | 特定のタグに関連する進捗のみをフィルタリング |

#### レスポンス（成功）

- **ステータスコード**: `200 OK`

```json
{
  "status": "success",
  "progress": {
    "items": [
      {
        "problem_id": "f1e2d3c4-b5a6-7890-abcd-1234567890ab",
        "problem_title": "線形代数の基礎",
        "attempts": 3,
        "correct_attempts": 2,
        "mastery_level": 0.75,
        "last_attempt_at": "2025-03-05T14:20:00Z"
      },
      {
        "problem_id": "a9b8c7d6-e5f4-3210-abcd-1234567890ab",
        "problem_title": "微分方程式入門",
        "attempts": 1,
        "correct_attempts": 0,
        "mastery_level": 0.0,
        "last_attempt_at": "2025-03-02T10:15:00Z"
      }
      // ... 他の進捗データ
    ],
    "total": 15,
    "limit": 20,
    "offset": 0
  },
  "summary": {
    "total_problems_attempted": 15,
    "total_correct_answers": 10,
    "average_mastery_level": 0.65,
    "total_time_spent": 320 // 分単位
  }
}
```

#### レスポンス（失敗）

- **ステータスコード**: `404 Not Found`

```json
{
  "status": "error",
  "message": "User not found",
  "error_code": "USER_NOT_FOUND"
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

### 4. ユーザーの回答履歴取得

ユーザーの問題回答履歴を取得します。

- **URL**: `/users/{user_id}/answers`
- **メソッド**: `GET`
- **認証**: 必要
- **権限**: 自分自身の回答履歴に対してのみアクセス可能（教員は全てのユーザー回答履歴にアクセス可能）

#### URL パラメータ

| パラメータ | 説明 |
|----------|------|
| user_id | 対象ユーザーのID（UUIDv4形式） |

#### クエリパラメータ

| パラメータ | 必須 | デフォルト | 説明 |
|----------|------|-----------|------|
| limit | ✗ | 20 | 取得する回答データの最大数 |
| offset | ✗ | 0 | 取得開始位置（ページネーション用） |
| problem_id | ✗ | - | 特定の問題の回答履歴のみをフィルタリング |

#### レスポンス（成功）

- **ステータスコード**: `200 OK`

```json
{
  "status": "success",
  "answers": {
    "items": [
      {
        "id": "d4c3b2a1-e5f6-7890-abcd-1234567890ab",
        "problem_id": "f1e2d3c4-b5a6-7890-abcd-1234567890ab",
        "problem_title": "線形代数の基礎",
        "selected_choice_id": "c4d5e6f7-8901-abcd-ef23-456789012345",
        "is_correct": true,
        "created_at": "2025-03-05T14:20:00Z"
      },
      {
        "id": "e5f6g7h8-i9j0-abcd-ef12-345678901234",
        "problem_id": "a9b8c7d6-e5f4-3210-abcd-1234567890ab",
        "problem_title": "微分方程式入門",
        "selected_choice_id": "d5e6f7g8-9012-abcd-ef34-567890123456",
        "is_correct": false,
        "created_at": "2025-03-02T10:15:00Z"
      }
      // ... 他の回答データ
    ],
    "total": 25,
    "limit": 20,
    "offset": 0
  }
}
```

#### レスポンス（失敗）

- **ステータスコード**: `404 Not Found`

```json
{
  "status": "error",
  "message": "User not found",
  "error_code": "USER_NOT_FOUND"
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

## エラーコード一覧

| エラーコード | 説明 |
|------------|------|
| USER_NOT_FOUND | 指定されたユーザーが存在しません |
| PROFILE_NOT_FOUND | 指定されたユーザーのプロフィールが存在しません |
| ACCESS_DENIED | このリソースへのアクセス権限がありません |
| INVALID_PARAMETER | リクエストパラメータが無効です |
