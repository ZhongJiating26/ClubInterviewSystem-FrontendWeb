from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # ===== 基础 =====
    app_name: str = Field(default="FastAPI App")
    app_env: str = Field(default="dev")
    debug: bool = Field(default=False)

    # ===== 数据库 =====
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    # ===== JWT =====
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 全局唯一配置对象
settings = Settings()
