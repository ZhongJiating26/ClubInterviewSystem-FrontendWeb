from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

DATABASE_URL = (
    f"mysql+pymysql://{settings.db_user}:"
    f"{settings.db_password}@"
    f"{settings.db_host}:"
    f"{settings.db_port}/"
    f"{settings.db_name}"
    "?charset=utf8mb4"
)

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    echo=settings.debug,   # dev 环境打印 SQL
    pool_pre_ping=True,    # 自动检测断开的连接
)


def get_session():
    """
    FastAPI 依赖注入用的数据库 Session
    """
    with Session(engine) as session:
        yield session
