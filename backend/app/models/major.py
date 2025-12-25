from typing import Optional
from sqlmodel import Field
from app.models.base import BaseModel


class Major(BaseModel, table=True):
    """
    专业表：基础维度表
    """
    __tablename__ = "major"

    name: str = Field(max_length=100, nullable=False, description="专业名称")
    code: Optional[str] = Field(default=None, max_length=50, description="专业代码")
    category: Optional[str] = Field(default=None, max_length=50, description="专业类别（如：工学、理学、文学等）")
    school_id: Optional[int] = Field(default=None, foreign_key="school.id", description="所属学校ID（可选，None表示通用专业）")
    status: int = Field(default=1, nullable=False, description="状态：1启用 0禁用")

