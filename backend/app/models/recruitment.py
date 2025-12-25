"""
招新相关模型
"""
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.orm import RelationshipProperty
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.club import Club
    from app.models.user_account import UserAccount


class Recruitment(BaseModel, table=True):
    """
    招新活动表
    """
    __tablename__ = "recruitment"

    club_id: int = Field(foreign_key="club.id", nullable=False, description="社团ID")
    title: str = Field(max_length=200, nullable=False, description="招新标题")
    description: Optional[str] = Field(default=None, description="招新描述")
    
    # 时间信息
    start_time: datetime = Field(nullable=False, description="报名开始时间")
    end_time: datetime = Field(nullable=False, description="报名结束时间")
    interview_start_time: Optional[datetime] = Field(default=None, description="面试开始时间")
    interview_end_time: Optional[datetime] = Field(default=None, description="面试结束时间")
    
    # 状态
    status: int = Field(default=0, nullable=False, description="状态：0待发布 1进行中 2已结束 3已取消")
    
    # 统计信息
    application_count: int = Field(default=0, nullable=False, description="报名人数")
    
    # 关联关系
    club: "Club" = Relationship(back_populates="recruitments")
    applications: list["Application"] = Relationship(back_populates="recruitment")


class Application(BaseModel, table=True):
    """
    报名申请表
    """
    __tablename__ = "application"

    recruitment_id: int = Field(foreign_key="recruitment.id", nullable=False, description="招新ID")
    user_id: int = Field(foreign_key="user_account.id", nullable=False, description="申请人ID")
    
    # 申请信息
    motivation: Optional[str] = Field(default=None, description="申请动机")
    experience: Optional[str] = Field(default=None, description="相关经历")
    skills: Optional[str] = Field(default=None, description="技能特长")
    
    # 状态
    status: int = Field(default=0, nullable=False, description="状态：0待审核 1已通过 2已拒绝 3已取消")
    
    # 审核信息
    reviewed_by: Optional[int] = Field(default=None, foreign_key="user_account.id", description="审核人ID")
    reviewed_at: Optional[datetime] = Field(default=None, description="审核时间")
    review_comment: Optional[str] = Field(default=None, description="审核意见")
    
    # 关联关系
    recruitment: "Recruitment" = Relationship(back_populates="applications")
    # 明确指定外键，因为有两个外键都指向 UserAccount
    user: Optional["UserAccount"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Application.user_id]"}
    )
    reviewer: Optional["UserAccount"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Application.reviewed_by]"}
    )


class Interview(BaseModel, table=True):
    """
    面试安排表
    """
    __tablename__ = "interview"

    application_id: int = Field(foreign_key="application.id", nullable=False, description="申请ID")
    
    # 面试时间
    scheduled_time: datetime = Field(nullable=False, description="面试时间")
    duration: int = Field(default=30, nullable=False, description="面试时长（分钟）")
    
    # 面试官
    interviewer_id: int = Field(foreign_key="user_account.id", nullable=False, description="面试官ID")
    
    # 地点
    location: Optional[str] = Field(default=None, max_length=200, description="面试地点")
    
    # 状态
    status: int = Field(default=0, nullable=False, description="状态：0待面试 1进行中 2已完成 3已取消")
    
    # 面试结果
    result: Optional[int] = Field(default=None, description="面试结果：1通过 2不通过")
    score: Optional[float] = Field(default=None, description="面试评分")
    comment: Optional[str] = Field(default=None, description="面试评价")
    completed_at: Optional[datetime] = Field(default=None, description="完成时间")
    
    # 关联关系
    application: Optional["Application"] = Relationship()
    interviewer: Optional["UserAccount"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Interview.interviewer_id]"}
    )

