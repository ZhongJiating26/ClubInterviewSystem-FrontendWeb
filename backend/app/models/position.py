"""
岗位相关模型
"""
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.club import Club
    from app.models.department import Department


class Position(BaseModel, table=True):
    """
    岗位表：社团招新的岗位
    """
    __tablename__ = "position"

    club_id: int = Field(foreign_key="club.id", nullable=False, description="社团ID")
    department_id: Optional[int] = Field(default=None, foreign_key="department.id", description="部门ID（可选）")
    name: str = Field(max_length=100, nullable=False, description="岗位名称")
    description: Optional[str] = Field(default=None, description="岗位描述")
    requirements: Optional[str] = Field(default=None, description="岗位要求")
    max_count: Optional[int] = Field(default=None, description="最大招聘人数")
    status: int = Field(default=1, nullable=False, description="状态：1启用 0禁用")
    
    # 关联关系
    club: Optional["Club"] = Relationship()
    department: Optional["Department"] = Relationship(back_populates="positions")

