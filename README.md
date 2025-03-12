# 大学生向け数学特化型学習管理システム（LMS）- MVP版

大学生向けの数学特化型学習管理システム（LMS）のMVP（Minimum Viable Product）版のリポジトリです。

## 概要

このプロジェクトは、大学生が数学を効率的に学習できるよう支援するための学習管理システムのMVP版を開発することを目的としています。フロントエンドにはNext.js（TypeScript）、バックエンドにはPython（FastAPI）を使用しています。

## MVPの主な機能

- ユーザー認証（ログイン・ログアウト）
- LaTeX対応の数式エディタ
- 基本的な問題作成と回答機能
- 学習進捗の基本的な追跡
- シンプルなダッシュボード

## ドキュメント構成

MVPの開発に必要なドキュメントは以下の構成で整理されています：

- [01_要件・範囲](./docs/01_要件・範囲/)
  - [01_MVPの目的と範囲](./docs/01_要件・範囲/01_MVPの目的と範囲.md)
  - [02_ユーザーストーリー](./docs/01_要件・範囲/02_ユーザーストーリー.md)
  - [03_機能要件](./docs/01_要件・範囲/03_機能要件.md)

- [02_アーキテクチャ](./docs/02_アーキテクチャ/)
  - [01_システム構成](./docs/02_アーキテクチャ/01_システム構成.md)
  - [02_技術スタック](./docs/02_アーキテクチャ/02_技術スタック.md)
  - [03_データモデル](./docs/02_アーキテクチャ/03_データモデル.md)

- [03_API仕様](./docs/03_API仕様/)
  - [01_認証API](./docs/03_API仕様/01_認証API.md)
  - [02_ユーザーAPI](./docs/03_API仕様/02_ユーザーAPI.md)
  - [03_コンテンツAPI](./docs/03_API仕様/03_コンテンツAPI.md)
  - [04_学習API](./docs/03_API仕様/04_学習API.md)

- [04_フロントエンド](./docs/04_フロントエンド/)
  - [01_画面フロー](./docs/04_フロントエンド/01_画面フロー.md)
  - [02_UIコンポーネント](./docs/04_フロントエンド/02_UIコンポーネント.md)
  - [03_状態管理](./docs/04_フロントエンド/03_状態管理.md)

- [05_開発・運用ガイド](./docs/05_開発・運用ガイド/)
  - [01_開発環境構築](./docs/05_開発・運用ガイド/01_開発環境構築.md)
  - [02_デプロイ手順](./docs/05_開発・運用ガイド/02_デプロイ手順.md)
  - [03_テスト計画](./docs/05_開発・運用ガイド/03_テスト計画.md)

## 開発環境構築

インストール手順については、[開発環境構築](./docs/05_開発・運用ガイド/01_開発環境構築.md)を参照してください。

### クイックスタート (Docker)

```bash
# リポジトリのクローン
git clone https://github.com/takuyakubo/university-math-lms-mvp.git
cd university-math-lms-mvp

# Docker環境の起動
docker-compose up -d
```

### 手動セットアップ

```bash
# バックエンド
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # 環境変数を編集
uvicorn app.main:app --reload

# フロントエンド
cd frontend
npm install
cp .env.example .env.local  # 環境変数を編集
npm run dev
```

## プロジェクト構造

```
university-math-lms-mvp/
├── backend/               # バックエンドアプリケーション
│   ├── app/
│   │   ├── api/           # APIルート
│   │   ├── core/          # 設定と共通機能
│   │   ├── db/            # データベース設定
│   │   ├── models/        # SQLAlchemyモデル
│   │   ├── schemas/       # Pydanticスキーマ
│   │   └── services/      # ビジネスロジック
│   ├── migrations/        # Alembicマイグレーション
│   ├── scripts/           # ユーティリティスクリプト
│   └── tests/             # バックエンドテスト
├── frontend/              # フロントエンドアプリケーション
│   ├── public/            # 静的ファイル
│   ├── src/
│   │   ├── components/    # Reactコンポーネント
│   │   ├── hooks/         # カスタムフック
│   │   ├── pages/         # Next.jsページ
│   │   ├── styles/        # CSSとスタイル
│   │   └── utils/         # ユーティリティ関数
│   └── tests/             # フロントエンドテスト
├── docs/                  # プロジェクトドキュメント
└── docker-compose.yml     # Docker構成
```

## 開発状況

このプロジェクトはMVP開発段階にあります。MVPの機能実装完了後、フィードバックを基に機能拡張を行う予定です。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
