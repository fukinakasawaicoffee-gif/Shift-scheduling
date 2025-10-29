# シフト自動生成システム

社内のシフト自動生成を支援するWebアプリケーションです。Google OR-Toolsを使用した最適化アルゴリズムにより、複雑な制約条件を考慮したシフトを自動生成します。

## 主な機能

- **部署管理**: 複数の部署を管理し、部署ごとに異なる設定が可能
- **従業員管理**: 従業員情報の登録・管理（200名規模対応）
- **シフトパターン管理**: 部署ごとに柔軟なシフトパターンを設定
  - 早番・遅番・普通番など、各パターンで異なる開始時間を設定可能
- **休暇管理**:
  - 通常休（月最大8日）
  - 有給休暇
  - 特別休暇（夏季・冬季・バースデー）
- **シフト自動生成**: 以下の制約を考慮した最適化
  - 必要人数の充足
  - 従業員の希望休
  - 連続勤務日数の制限
  - 公平性（シフト配分の均等化）
  - 特別期間（セール期間など）の人数調整

## 技術スタック

### バックエンド
- **Python 3.11**
- **FastAPI**: 高速で型安全なAPIフレームワーク
- **SQLAlchemy**: ORM
- **PostgreSQL**: データベース
- **Google OR-Tools**: 制約付き最適化ライブラリ

### フロントエンド
- **React 18**
- **TypeScript**
- **Material-UI**: UIコンポーネント
- **React Query**: データフェッチング管理

### インフラ
- **Docker & Docker Compose**: コンテナ化と開発環境管理

## セットアップ

### 前提条件

- Docker & Docker Compose がインストールされていること
- Git がインストールされていること

### インストール手順

1. **リポジトリのクローン**
```bash
git clone <repository-url>
cd Shift-scheduling
```

2. **環境変数の設定**
```bash
cp backend/.env.example backend/.env
```

`.env`ファイルを編集し、必要に応じて設定を変更してください：
```env
DATABASE_URL=postgresql://shift_user:shift_password@db:5432/shift_scheduling
SECRET_KEY=your-secret-key-change-this-in-production
```

3. **Docker Composeでアプリケーションを起動**
```bash
docker-compose up -d
```

初回起動時は、Dockerイメージのビルドとパッケージのインストールに時間がかかります。

4. **初期データの投入（オプション）**
```bash
docker-compose exec backend python scripts/init_data.py
```

5. **アプリケーションへのアクセス**
- フロントエンド: http://localhost:3000
- バックエンドAPI: http://localhost:8000
- API ドキュメント: http://localhost:8000/docs

## 使い方

### 1. 初期セットアップ

1. **ユーザー登録**
   - APIエンドポイント `/api/v1/auth/register` を使用してユーザーを作成
   - または、初期データスクリプトで管理者ユーザーを作成

2. **部署の登録**
   - 部署管理画面から部署を登録
   - 各部署の休日設定（月の通常休日数、最大連続勤務日数）を設定

3. **シフトパターンの設定**
   - 部署ごとにシフトパターンを登録
   - 開始時刻、終了時刻、勤務時間を設定

4. **従業員の登録**
   - 従業員管理画面から従業員を登録
   - 所属部署、有給残日数などを設定

### 2. シフト生成

1. **必要人数の設定**
   - 日付・シフトパターンごとに必要人数を設定
   - セール期間などの特別期間も設定可能

2. **休暇申請の登録**
   - 従業員の希望休や有給申請を登録
   - 申請を承認

3. **シフト自動生成の実行**
   - シフトカレンダー画面で生成期間を指定
   - 「自動生成」ボタンをクリック
   - 最適化アルゴリズムが制約を満たすシフトを生成

4. **シフトの確認と調整**
   - 生成されたシフトを確認
   - 必要に応じて手動で調整
   - 確定後、従業員に公開

## API仕様

詳細なAPI仕様は以下のエンドポイントで確認できます：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 主なエンドポイント

#### 認証
- `POST /api/v1/auth/login`: ログイン
- `POST /api/v1/auth/register`: ユーザー登録

#### 部署
- `GET /api/v1/departments/`: 部署一覧
- `POST /api/v1/departments/`: 部署作成
- `PUT /api/v1/departments/{id}`: 部署更新
- `DELETE /api/v1/departments/{id}`: 部署削除

#### 従業員
- `GET /api/v1/employees/`: 従業員一覧
- `POST /api/v1/employees/`: 従業員作成
- `PUT /api/v1/employees/{id}`: 従業員更新
- `DELETE /api/v1/employees/{id}`: 従業員削除

#### スケジュール
- `GET /api/v1/schedules/`: スケジュール一覧
- `POST /api/v1/schedules/generate`: シフト自動生成
- `PUT /api/v1/schedules/{id}`: スケジュール更新

## 開発

### バックエンドの開発

```bash
# バックエンドコンテナに入る
docker-compose exec backend bash

# テストの実行
pytest

# DBマイグレーション
alembic revision --autogenerate -m "migration message"
alembic upgrade head
```

### フロントエンドの開発

```bash
# フロントエンドコンテナに入る
docker-compose exec frontend sh

# パッケージの追加
npm install <package-name>

# ビルド
npm run build
```

### データベース管理

```bash
# PostgreSQLに接続
docker-compose exec db psql -U shift_user -d shift_scheduling

# バックアップ
docker-compose exec db pg_dump -U shift_user shift_scheduling > backup.sql

# リストア
docker-compose exec -T db psql -U shift_user shift_scheduling < backup.sql
```

## シフト最適化アルゴリズム

Google OR-ToolsのCP-SATソルバーを使用して、以下の制約を満たすシフトを生成します：

### 制約条件

1. **1日1シフト制約**: 各従業員は1日に最大1つのシフトのみ
2. **必要人数制約**: 各シフトパターン・日付ごとの必要人数を満たす
3. **休日制約**: 月の通常休日数を守る（有給・特別休は別枠）
4. **連続勤務制約**: 最大連続勤務日数を超えない
5. **休暇申請制約**: 承認済みの休暇申請を遵守

### 目的関数

従業員間のシフト配分の公平性を最大化（勤務日数の偏りを最小化）

## トラブルシューティング

### コンテナが起動しない

```bash
# ログを確認
docker-compose logs

# コンテナを再ビルド
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### データベース接続エラー

```bash
# データベースコンテナのヘルスチェック
docker-compose ps

# データベースを再起動
docker-compose restart db
```

### フロントエンドでAPIエラーが発生

- `.env`ファイルで`REACT_APP_API_URL`が正しく設定されているか確認
- ブラウザのコンソールでCORSエラーがないか確認
- バックエンドの`BACKEND_CORS_ORIGINS`設定を確認

## ライセンス

このプロジェクトは社内利用のためのものです。

## お問い合わせ

システムに関する質問や問題報告は、プロジェクトの管理者にお問い合わせください。
