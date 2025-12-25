"""
招新相关Schema
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class RecruitmentCreateRequest(BaseModel):
    """创建招新活动请求"""
    club_id: int = Field(..., description="社团ID")
    title: str = Field(..., min_length=1, max_length=200, description="招新标题")
    description: Optional[str] = Field(default=None, description="招新描述")
    start_time: datetime = Field(..., description="报名开始时间")
    end_time: datetime = Field(..., description="报名结束时间")
    interview_start_time: Optional[datetime] = Field(default=None, description="面试开始时间")
    interview_end_time: Optional[datetime] = Field(default=None, description="面试结束时间")


class RecruitmentResponse(BaseModel):
    """招新活动响应"""
    id: int
    club_id: int
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    interview_start_time: Optional[datetime]
    interview_end_time: Optional[datetime]
    status: int
    application_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class ApplicationCreateRequest(BaseModel):
    """创建报名申请请求"""
    recruitment_id: int = Field(..., description="招新ID")
    motivation: Optional[str] = Field(default=None, description="申请动机")
    experience: Optional[str] = Field(default=None, description="相关经历")
    skills: Optional[str] = Field(default=None, description="技能特长")


class ApplicationResponse(BaseModel):
    """报名申请响应"""
    id: int
    recruitment_id: int
    user_id: int
    motivation: Optional[str]
    experience: Optional[str]
    skills: Optional[str]
    status: int
    reviewed_by: Optional[int]
    reviewed_at: Optional[datetime]
    review_comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ApplicationReviewRequest(BaseModel):
    """审核申请请求"""
    approved: bool = Field(..., description="是否通过")
    comment: Optional[str] = Field(default=None, description="审核意见")


class InterviewCreateRequest(BaseModel):
    """创建面试安排请求"""
    application_id: int = Field(..., description="申请ID")
    interviewer_id: int = Field(..., description="面试官ID")
    scheduled_time: datetime = Field(..., description="面试时间")
    duration: int = Field(default=30, ge=10, le=180, description="面试时长（分钟）")
    location: Optional[str] = Field(default=None, max_length=200, description="面试地点")


class InterviewResponse(BaseModel):
    """面试安排响应"""
    id: int
    application_id: int
    interviewer_id: int
    scheduled_time: datetime
    duration: int
    location: Optional[str]
    status: int
    result: Optional[int]
    score: Optional[float]
    comment: Optional[str]
    completed_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class InterviewCompleteRequest(BaseModel):
    """完成面试请求"""
    result: int = Field(..., ge=1, le=2, description="面试结果：1通过 2不通过")
    score: Optional[float] = Field(default=None, ge=0, le=100, description="面试评分")
    comment: Optional[str] = Field(default=None, description="面试评价")

