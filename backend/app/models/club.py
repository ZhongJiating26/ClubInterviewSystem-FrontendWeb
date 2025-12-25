"""
社团相关模型
"""
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user_account import UserAccount
    from app.models.recruitment import Recruitment
    from app.models.school import School


class Club(BaseModel, table=True):
    """
    社团表
    """
    __tablename__ = "club"

    name: str = Field(max_length=100, nullable=False, description="社团名称")
    description: Optional[str] = Field(default=None, description="社团简介")
    logo_url: Optional[str] = Field(default=None, max_length=255, description="社团Logo")
    cover_url: Optional[str] = Field(default=None, max_length=255, description="封面图")
    
    # 学校信息
    school_id: Optional[int] = Field(default=None, foreign_key="school.id", nullable=True, description="所属学校ID")
    
    # 社长信息
    president_id: int = Field(foreign_key="user_account.id", nullable=False, description="社长用户ID")
    
    # 状态
    status: int = Field(default=1, nullable=False, description="状态：1正常 0禁用")
    
    # 统计信息
    member_count: int = Field(default=0, nullable=False, description="成员数量")
    
    # 关联关系
    president: Optional["UserAccount"] = Relationship()
    school: Optional["School"] = Relationship()
    members: list["ClubMember"] = Relationship(back_populates="club")
    recruitments: list["Recruitment"] = Relationship(back_populates="club")


class ClubMember(BaseModel, table=True):
    """
    社团成员表
    """
    __tablename__ = "club_member"

    club_id: int = Field(foreign_key="club.id", nullable=False, description="社团ID")
    user_id: int = Field(foreign_key="user_account.id", nullable=False, description="用户ID")
    
    # 角色（在社团中的角色，如：社长、副社长、部长、成员等）
    role: str = Field(default="member", max_length=50, description="角色")
    
    # 加入时间
    joined_at: Optional[str] = Field(default=None, description="加入时间（冗余字段，实际用created_at）")
    
    # 状态
    status: int = Field(default=1, nullable=False, description="状态：1正常 0禁用")
    
    # 关联关系
    club: "Club" = Relationship(back_populates="members")
    user: "UserAccount" = Relationship()

