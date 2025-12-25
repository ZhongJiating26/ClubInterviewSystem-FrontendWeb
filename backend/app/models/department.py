"""
部门相关模型
"""
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.club import Club
    from app.models.recruitment import Position


class Department(BaseModel, table=True):
    """
    部门表：社团的部门
    """
    __tablename__ = "department"

    club_id: int = Field(foreign_key="club.id", nullable=False, description="社团ID")
    name: str = Field(max_length=100, nullable=False, description="部门名称")
    description: Optional[str] = Field(default=None, description="部门描述")
    status: int = Field(default=1, nullable=False, description="状态：1启用 0禁用")
    
    # 关联关系
    club: Optional["Club"] = Relationship()
    positions: list["Position"] = Relationship(back_populates="department")

