"""
社团相关Schema
"""
from typing import Optional
from pydantic import BaseModel, Field


class ClubCreateRequest(BaseModel):
    """创建社团请求"""
    name: str = Field(..., min_length=1, max_length=100, description="社团名称")
    description: Optional[str] = Field(default=None, description="社团简介")
    school_id: Optional[int] = Field(default=None, description="所属学校ID")
    logo_url: Optional[str] = Field(default=None, max_length=255, description="Logo URL")
    cover_url: Optional[str] = Field(default=None, max_length=255, description="封面图URL")


class ClubUpdateRequest(BaseModel):
    """更新社团请求"""
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = None
    logo_url: Optional[str] = Field(default=None, max_length=255)
    cover_url: Optional[str] = Field(default=None, max_length=255)


class ClubResponse(BaseModel):
    """社团响应"""
    id: int
    name: str
    description: Optional[str]
    logo_url: Optional[str]
    cover_url: Optional[str]
    school_id: int
    president_id: int
    status: int
    member_count: int
    created_at: str

    class Config:
        from_attributes = True


class ClubMemberResponse(BaseModel):
    """社团成员响应"""
    id: int
    club_id: int
    user_id: int
    role: str
    status: int
    created_at: str

    class Config:
        from_attributes = True


class AddMemberRequest(BaseModel):
    """添加成员请求"""
    user_id: int = Field(..., description="用户ID")
    role: str = Field(default="member", max_length=50, description="角色")

