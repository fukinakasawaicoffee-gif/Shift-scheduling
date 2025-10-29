.PHONY: help build up down logs clean restart init-db

help: ## ヘルプを表示
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Dockerイメージをビルド
	docker-compose build

up: ## アプリケーションを起動
	docker-compose up -d

down: ## アプリケーションを停止
	docker-compose down

logs: ## ログを表示
	docker-compose logs -f

clean: ## コンテナとボリュームを削除
	docker-compose down -v
	rm -rf backend/__pycache__
	rm -rf frontend/node_modules

restart: ## アプリケーションを再起動
	docker-compose restart

init-db: ## 初期データを投入
	docker-compose exec backend python scripts/init_data.py

backend-shell: ## バックエンドコンテナに入る
	docker-compose exec backend bash

frontend-shell: ## フロントエンドコンテナに入る
	docker-compose exec frontend sh

db-shell: ## データベースに接続
	docker-compose exec db psql -U shift_user -d shift_scheduling

test-backend: ## バックエンドのテストを実行
	docker-compose exec backend pytest

migrate: ## DBマイグレーションを実行
	docker-compose exec backend alembic upgrade head

migrate-create: ## 新しいマイグレーションファイルを作成
	@read -p "Migration message: " msg; \
	docker-compose exec backend alembic revision --autogenerate -m "$$msg"
