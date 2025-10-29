from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.api import auth, departments, employees, schedules

# データベーステーブル作成
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["認証"])
app.include_router(departments.router, prefix=f"{settings.API_V1_STR}/departments", tags=["部署"])
app.include_router(employees.router, prefix=f"{settings.API_V1_STR}/employees", tags=["従業員"])
app.include_router(schedules.router, prefix=f"{settings.API_V1_STR}/schedules", tags=["スケジュール"])


@app.get("/")
def root():
    """ルートエンドポイント"""
    return {
        "message": "シフト自動生成システムAPI",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """ヘルスチェック"""
    return {"status": "healthy"}
