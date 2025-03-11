# 学習API

このドキュメントでは、学習活動に関するAPIエンドポイントの仕様を定義します。

## ベースURL

```
https://api.math-lms.example.com/v1
```

## 認証方式

- JWTトークンベースの認証
- `Authorization` ヘッダーに `Bearer {token}` 形式でトークンを指定

## エンドポイント一覧

### 1. 問題に回答する

問題に対する回答を提出します。

- **URL**: `/learning/answers`
- **メソッド**: `POST`
- **認証**: 必要

#### リクエスト本文

```json
{
  "problem_id": "f1e2d3c4-b5a6-7890-abcd-1234567890ab",
  "selected_choice_id": "e6f7g8h9-0123-abcd-ef45-678901234567"
}
```

| パラメータ | 型 | 必須 | 説明 |
|----------|---|------|------|
| problem_id | string (UUID) | ✓ | 問題のID |
| selected_choice_id | string (UUID) | ✓ | 選択した選択肢のID |

#### レスポンス（成功）

- **ステータスコード**: `201 Created`

```json
{
  "status": "success",
  "answer": {
    "id": "d4c3b2a1-e5f6-7890-abcd-1234567890ab",
    "problem_id": "f1e2d3c4-b5a6-7890-abcd-1234567890ab",
    "selected_choice_id": "e6f7g8h9-0123-abcd-ef45-678901234567",
    "is_correct": true,
    "created_at": "2025-03-11T15:20:00Z"
  },
  "feedback": {
    "is_correct": true,
    "message": "正解です！",
    "explanation": "三角関数の基本的な恒等式 $\\sin^2 x + \\cos^2 x = 1$ は常に成り立ちます。この式は単位円上の点$(\\cos x, \\sin x)$が常に単位円上にあることを表しています。",
    "mastery_level": 0.75,
    "attempts": 3,
    "correct_attempts": 2
  }
}
```

#### レスポンス（失敗）

- **ステータスコード**: `400 Bad Request`

```json
{
  "status": "error",
  "message": "Invalid choice for the given problem",
  "error_code": "INVALID_CHOICE"
}
```

または

- **ステータスコード**: `404 Not Found`

```json
{
  "status": "error",
  "message": "Problem not found",
  "error_code": "PROBLEM_NOT_FOUND"
}
```

### 2. 学習進捗の取得

学習者の特定の問題に対する進捗状況を取得します。

- **URL**: `/learning/progress/{problem_id}`
- **メソッド**: `GET`
- **認証**: 必要

#### URL パラメータ

| パラメータ | 説明 |
|----------|------|
| problem_id | 対象問題のID（UUIDv4形式） |

#### レスポンス（成功）

- **ステータスコード**: `200 OK`

```json
{
  "status": "success",
  "progress": {
    "problem_id": "f1e2d3c4-b5a6-7890-abcd-1234567890ab",
    "attempts": 3,
    "correct_attempts": 2,
    "mastery_level": 0.75,
    "last_attempt_at": "2025-03-11T15:20:00Z"
  }
}
```

#### レスポンス（未挑戦）

- **ステータスコード**: `200 OK`

```json
{
  "status": "success",
  "progress": {
    "problem_id": "f1e2d3c4-b5a6-7890-abcd-1234567890ab",
    "attempts": 0,
    "correct_attempts": 0,
    "mastery_level": 0,
    "last_attempt_at": null
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

### 3. 総合学習進捗の取得

現在のユーザーの総合的な学習進捗を取得します。

- **URL**: `/learning/progress/summary`
- **メソッド**: `GET`
- **認証**: 必要

#### レスポンス（成功）

- **ステータスコード**: `200 OK`

```json
{
  "status": "success",
  "summary": {
    "total_problems_attempted": 25,
    "total_problems_mastered": 18,
    "average_mastery_level": 0.72,
    "total_correct_answers": 42,
    "total_attempts": 65,
    "correct_rate": 64.6,
    "recent_activity": [
      {
        "date": "2025-03-11",
        "problems_attempted": 3,
        "correct_answers": 2
      },
      {
        "date": "2025-03-10",
        "problems_attempted": 5,
        "correct_answers": 4
      },
      {
        "date": "2025-03-09",
        "problems_attempted": 4,
        "correct_answers": 3
      },
      {
        "date": "2025-03-08",
        "problems_attempted": 2,
        "correct_answers": 1
      },
      {
        "date": "2025-03-07",
        "problems_attempted": 6,
        "correct_answers": 4
      }
    ],
    "tag_performance": [
      {
        "tag": "線形代数",
        "problems_attempted": 8,
        "mastery_level": 0.85
      },
      {
        "tag": "微分方程式",
        "problems_attempted": 6,
        "mastery_level": 0.65
      },
      {
        "tag": "三角関数",
        "problems_attempted": 5,
        "mastery_level": 0.90
      },
      {
        "tag": "数列",
        "problems_attempted": 4,
        "mastery_level": 0.50
      },
      {
        "tag": "複素数",
        "problems_attempted": 2,
        "mastery_level": 0.70
      }
    ]
  }
}
```

### 4. 推奨問題の取得

ユーザーの学習進捗に基づいて推奨される問題のリストを取得します。

- **URL**: `/learning/recommendations`
- **メソッド**: `GET`
- **認証**: 必要

#### クエリパラメータ

| パラメータ | 必須 | デフォルト | 説明 |
|----------|------|-----------|------|
| limit | ✗ | 10 | 推奨問題の最大数 |

#### レスポンス（成功）

- **ステータスコード**: `200 OK`

```json
{
  "status": "success",
  "recommendations": [
    {
      "problem_id": "a9b8c7d6-e5f4-3210-abcd-1234567890ab",
      "title": "微分方程式入門",
      "difficulty": 4,
      "tags": ["微分方程式", "微積分", "応用"],
      "recommendation_reason": "弱点分野の強化",
      "mastery_level": 0.35
    },
    {
      "problem_id": "b9c8d7e6-f5g4-3210-hijk-2345678901cd",
      "title": "行列の固有値",
      "difficulty": 3,
      "tags": ["線形代数", "行列", "固有値"],
      "recommendation_reason": "次のステップ",
      "mastery_level": 0.60
    },
    {
      "problem_id": "c9d8e7f6-g5h4-3210-ijkl-3456789012de",
      "title": "数列の収束",
      "difficulty": 3,
      "tags": ["数列", "極限", "収束"],
      "recommendation_reason": "弱点分野の強化",
      "mastery_level": 0.40
    }
    // ... 他の推奨問題
  ]
}
```

### 5. 回答履歴の取得

特定の問題に対するユーザーの回答履歴を取得します。

- **URL**: `/learning/answers/history/{problem_id}`
- **メソッド**: `GET`
- **認証**: 必要

#### URL パラメータ

| パラメータ | 説明 |
|----------|------|
| problem_id | 対象問題のID（UUIDv4形式） |

#### クエリパラメータ

| パラメータ | 必須 | デフォルト | 説明 |
|----------|------|-----------|------|
| limit | ✗ | 10 | 取得する履歴の最大数 |

#### レスポンス（成功）

- **ステータスコード**: `200 OK`

```json
{
  "status": "success",
  "history": {
    "problem_id": "f1e2d3c4-b5a6-7890-abcd-1234567890ab",
    "problem_title": "線形代数の基礎",
    "items": [
      {
        "id": "d4c3b2a1-e5f6-7890-abcd-1234567890ab",
        "selected_choice_id": "e6f7g8h9-0123-abcd-ef45-678901234567",
        "selected_choice_text": "$5$",
        "is_correct": true,
        "created_at": "2025-03-11T15:20:00Z"
      },
      {
        "id": "e5d4c3b2-f6g7-8901-hijk-2345678901bc",
        "selected_choice_id": "d5e6f7g8-9012-abcd-ef34-567890123456",
        "selected_choice_text": "$8$",
        "is_correct": false,
        "created_at": "2025-03-08T09:45:00Z"
      },
      {
        "id": "f6e5d4c3-g7h8-9012-ijkl-3456789012cd",
        "selected_choice_id": "f7g8h9i0-1234-abcd-ef56-789012345678",
        "selected_choice_text": "$-1$",
        "is_correct": false,
        "created_at": "2025-03-05T14:30:00Z"
      }
    ],
    "total": 3
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

### 6. 学習統計の取得

期間別の学習統計情報を取得します。

- **URL**: `/learning/stats`
- **メソッド**: `GET`
- **認証**: 必要

#### クエリパラメータ

| パラメータ | 必須 | デフォルト | 説明 |
|----------|------|-----------|------|
| period | ✗ | week | 期間（day、week、month、year） |
| start_date | ✗ | - | 特定の開始日（YYYY-MM-DD形式） |
| end_date | ✗ | - | 特定の終了日（YYYY-MM-DD形式） |

#### レスポンス（成功）

- **ステータスコード**: `200 OK`

```json
{
  "status": "success",
  "stats": {
    "period": "week",
    "start_date": "2025-03-05",
    "end_date": "2025-03-11",
    "total_problems_attempted": 20,
    "total_correct_answers": 14,
    "correct_rate": 70.0,
    "study_time_minutes": 180,
    "daily_breakdown": [
      {
        "date": "2025-03-05",
        "problems_attempted": 2,
        "correct_answers": 1,
        "study_time_minutes": 15
      },
      {
        "date": "2025-03-06",
        "problems_attempted": 0,
        "correct_answers": 0,
        "study_time_minutes": 0
      },
      {
        "date": "2025-03-07",
        "problems_attempted": 6,
        "correct_answers": 4,
        "study_time_minutes": 45
      },
      {
        "date": "2025-03-08",
        "problems_attempted": 2,
        "correct_answers": 1,
        "study_time_minutes": 20
      },
      {
        "date": "2025-03-09",
        "problems_attempted": 4,
        "correct_answers": 3,
        "study_time_minutes": 35
      },
      {
        "date": "2025-03-10",
        "problems_attempted": 5,
        "correct_answers": 4,
        "study_time_minutes": 40
      },
      {
        "date": "2025-03-11",
        "problems_attempted": 3,
        "correct_answers": 2,
        "study_time_minutes": 25
      }
    ]
  }
}
```

## エラーコード一覧

| エラーコード | 説明 |
|------------|------|
| PROBLEM_NOT_FOUND | 指定された問題が存在しません |
| INVALID_CHOICE | 指定された選択肢が問題に存在しないか、無効です |
| ACCESS_DENIED | このリソースへのアクセス権限がありません |
| INVALID_PARAMETER | リクエストパラメータが無効です |
| INVALID_DATE | 指定された日付形式が無効です |
