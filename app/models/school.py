from typing import Optional

from sqlmodel import Field

from app.models.base import BaseModel


class School(BaseModel, table=True):
    """
    学校表：基础维度表
    """
    __tablename__ = "school"

    name: str = Field(max_length=100, nullable=False, description="学校名称")
    code: Optional[str] = Field(default=None, max_length=50, description="学校编码/代号")

    province: Optional[str] = Field(default=None, max_length=50, description="省份")
    city: Optional[str] = Field(default=None, max_length=50, description="城市")

    status: int = Field(default=1, nullable=False, description="状态：1启用 0禁用")
