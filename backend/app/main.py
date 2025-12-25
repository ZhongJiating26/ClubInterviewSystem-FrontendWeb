from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.auth import router as auth_router
from app.api.v1.dict import router as dict_router
from app.api.v1.club import router as club_router
from app.api.v1.recruitment import router as recruitment_router

app = FastAPI(
    title=settings.app_name,
    description="校园社团招新与面试管理系统",
    version="0.1.0",
    debug=settings.debug,
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # 前端地址
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)

app.include_router(auth_router)
app.include_router(dict_router)
app.include_router(club_router)
app.include_router(recruitment_router)

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "env": settings.app_env
    }


