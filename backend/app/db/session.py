from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# SQLite 数据库连接
# 数据库文件保存在项目根目录
DATABASE_URL = f"sqlite:///./{settings.db_name}"

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    echo=settings.debug,   # dev 环境打印 SQL
    connect_args={"check_same_thread": False},  # SQLite 需要这个参数
)


def get_session():
    """
    FastAPI 依赖注入用的数据库 Session
    """
    with Session(engine) as session:
        yield session
