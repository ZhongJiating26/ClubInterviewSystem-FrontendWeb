from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.auth import router as auth_router
app = FastAPI(
    title=settings.app_name,
    description="校园社团招新与面试管理系统",
    version="0.1.0",
    debug=settings.debug,
)

app.include_router(auth_router)

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "env": settings.app_env
    }


