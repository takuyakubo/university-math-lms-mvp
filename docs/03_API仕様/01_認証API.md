# 認証API

このドキュメントでは、ユーザー認証に関するAPIエンドポイントの仕様を定義します。

## ベースURL

```
https://api.math-lms.example.com/v1
```

## 認証方式

- JWTトークンベースの認証
- `Authorization` ヘッダーに `Bearer {token}` 形式でトークンを指定

## エンドポイント一覧

### 1. ユーザー登録

新規ユーザーを登録します。

- **URL**: `/auth/register`
- **メソッド**: `POST`
- **認証**: 不要

#### リクエスト本文

```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "山田 太郎",
  "role": "student"
}
```

| パラメータ | 型 | 必須 | 説明 |
|----------|---|------|------|
| email | string | ✓ | ユーザーのメールアドレス |
| password | string | ✓ | パスワード（8文字以上、英数字記号を含む） |
| full_name | string | ✓ | ユーザーの氏名 |
| role | string | ✓ | ユーザーロール（"student"または"teacher"） |

#### レスポンス（成功）

- **ステータスコード**: `201 Created`

```json
{
  "status": "success",
  "message": "User registered successfully",
  "user_id": "a1b2c3d4-e5f6-7890-abcd-1234567890ab"
}
```

#### レスポンス（失敗）

- **ステータスコード**: `400 Bad Request`

```json
{
  "status": "error",
  "message": "Email already registered",
  "error_code": "EMAIL_EXISTS"
}
```

または

```json
{
  "status": "error",
  "message": "Invalid input data",
  "errors": [
    {
      "field": "password",
      "message": "Password must be at least 8 characters and contain letters, numbers, and symbols"
    }
  ]
}
```

### 2. ログイン

登録済みユーザーのログイン認証を行います。

- **URL**: `/auth/login`
- **メソッド**: `POST`
- **認証**: 不要

#### リクエスト本文

```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

| パラメータ | 型 | 必須 | 説明 |
|----------|---|------|------|
| email | string | ✓ | 登録済みのメールアドレス |
| password | string | ✓ | パスワード |

#### レスポンス（成功）

- **ステータスコード**: `200 OK`

```json
{
  "status": "success",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "a1b2c3d4-e5f6-7890-abcd-1234567890ab",
    "email": "user@example.com",
    "full_name": "山田 太郎",
    "role": "student"
  }
}
```

#### レスポンス（失敗）

- **ステータスコード**: `401 Unauthorized`

```json
{
  "status": "error",
  "message": "Invalid credentials",
  "error_code": "INVALID_CREDENTIALS"
}
```

### 3. ログアウト

ユーザーのトークンを無効化します。

- **URL**: `/auth/logout`
- **メソッド**: `POST`
- **認証**: 必要

#### リクエストヘッダー

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### レスポンス（成功）

- **ステータスコード**: `200 OK`

```json
{
  "status": "success",
  "message": "Successfully logged out"
}
```

#### レスポンス（失敗）

- **ステータスコード**: `401 Unauthorized`

```json
{
  "status": "error",
  "message": "Invalid or expired token",
  "error_code": "INVALID_TOKEN"
}
```

### 4. パスワードリセットリクエスト

パスワードリセットのためのメール送信をリクエストします。

- **URL**: `/auth/password-reset/request`
- **メソッド**: `POST`
- **認証**: 不要

#### リクエスト本文

```json
{
  "email": "user@example.com"
}
```

| パラメータ | 型 | 必須 | 説明 |
|----------|---|------|------|
| email | string | ✓ | 登録済みのメールアドレス |

#### レスポンス（成功）

- **ステータスコード**: `200 OK`

```json
{
  "status": "success",
  "message": "If the email exists, a password reset link has been sent"
}
```

#### レスポンス（失敗）

- **ステータスコード**: `400 Bad Request`

```json
{
  "status": "error",
  "message": "Invalid email format",
  "error_code": "INVALID_EMAIL"
}
```

### 5. パスワードリセット実行

新しいパスワードを設定します。

- **URL**: `/auth/password-reset/confirm`
- **メソッド**: `POST`
- **認証**: 不要（トークンはリクエスト本文に含む）

#### リクエスト本文

```json
{
  "token": "reset-token-from-email",
  "password": "NewSecurePassword123!"
}
```

| パラメータ | 型 | 必須 | 説明 |
|----------|---|------|------|
| token | string | ✓ | メールで送信されたリセットトークン |
| password | string | ✓ | 新しいパスワード |

#### レスポンス（成功）

- **ステータスコード**: `200 OK`

```json
{
  "status": "success",
  "message": "Password has been reset successfully"
}
```

#### レスポンス（失敗）

- **ステータスコード**: `400 Bad Request`

```json
{
  "status": "error",
  "message": "Invalid or expired token",
  "error_code": "INVALID_RESET_TOKEN"
}
```

または

```json
{
  "status": "error",
  "message": "Invalid password format",
  "errors": [
    {
      "field": "password",
      "message": "Password must be at least 8 characters and contain letters, numbers, and symbols"
    }
  ]
}
```

### 6. 現在のユーザー情報取得

認証済みユーザーの情報を取得します。

- **URL**: `/auth/me`
- **メソッド**: `GET`
- **認証**: 必要

#### リクエストヘッダー

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### レスポンス（成功）

- **ステータスコード**: `200 OK`

```json
{
  "status": "success",
  "user": {
    "id": "a1b2c3d4-e5f6-7890-abcd-1234567890ab",
    "email": "user@example.com",
    "full_name": "山田 太郎",
    "role": "student",
    "created_at": "2025-01-15T12:00:00Z"
  }
}
```

#### レスポンス（失敗）

- **ステータスコード**: `401 Unauthorized`

```json
{
  "status": "error",
  "message": "Not authenticated",
  "error_code": "NOT_AUTHENTICATED"
}
```

## エラーコード一覧

| エラーコード | 説明 |
|------------|------|
| EMAIL_EXISTS | 指定されたメールアドレスは既に登録されています |
| INVALID_CREDENTIALS | メールアドレスまたはパスワードが正しくありません |
| INVALID_TOKEN | 認証トークンが無効または期限切れです |
| INVALID_RESET_TOKEN | パスワードリセットトークンが無効または期限切れです |
| INVALID_EMAIL | メールアドレスの形式が正しくありません |
| NOT_AUTHENTICATED | 認証が必要です |
