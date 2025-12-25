"""
面试场次相关模型
"""
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, Relationship
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.club import Club
    from app.models.recruitment import Recruitment, Application
    from app.models.user_account import UserAccount


class InterviewSession(BaseModel, table=True):
    """
    面试场次表
    """
    __tablename__ = "interview_session"

    club_id: int = Field(foreign_key="club.id", nullable=False, description="社团ID")
    recruitment_id: Optional[int] = Field(default=None, foreign_key="recruitment.id", description="关联招新场次ID")
    name: str = Field(max_length=200, nullable=False, description="场次名称")
    description: Optional[str] = Field(default=None, description="场次描述")
    
    # 时间信息
    start_time: datetime = Field(nullable=False, description="场次开始时间")
    end_time: datetime = Field(nullable=False, description="场次结束时间")
    
    # 地点
    location: Optional[str] = Field(default=None, max_length=200, description="面试地点")
    
    # 状态
    status: int = Field(default=0, nullable=False, description="状态：0待开始 1进行中 2已结束 3已取消")
    
    # 关联关系
    club: Optional["Club"] = Relationship()
    recruitment: Optional["Recruitment"] = Relationship()
    interviewer_assignments: list["InterviewerAssignment"] = Relationship(back_populates="session")
    candidates: list["InterviewCandidate"] = Relationship(back_populates="session")
    records: list["InterviewRecord"] = Relationship(back_populates="session")


class InterviewerAssignment(BaseModel, table=True):
    """
    面试官场次关系表
    """
    __tablename__ = "interviewer_assignment"

    session_id: int = Field(foreign_key="interview_session.id", nullable=False, description="场次ID")
    interviewer_id: int = Field(foreign_key="user_account.id", nullable=False, description="面试官ID")
    
    # 关联关系
    session: Optional["InterviewSession"] = Relationship(back_populates="interviewer_assignments")
    interviewer: Optional["UserAccount"] = Relationship()


class InterviewCandidate(BaseModel, table=True):
    """
    候选人排期表
    """
    __tablename__ = "interview_candidate"

    session_id: int = Field(foreign_key="interview_session.id", nullable=False, description="场次ID")
    application_id: int = Field(foreign_key="application.id", nullable=False, description="申请ID")
    
    # 排期时间
    scheduled_time: Optional[datetime] = Field(default=None, description="排期时间")
    
    # 最终得分
    final_score: Optional[float] = Field(default=None, description="最终得分")
    
    # 状态
    status: int = Field(default=0, nullable=False, description="状态：0待安排 1已安排 2已完成 3已取消")
    
    # 关联关系
    session: Optional["InterviewSession"] = Relationship(back_populates="candidates")
    application: Optional["Application"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[InterviewCandidate.application_id]"}
    )


class InterviewRecord(BaseModel, table=True):
    """
    面试记录表
    """
    __tablename__ = "interview_record"

    session_id: int = Field(foreign_key="interview_session.id", nullable=False, description="场次ID")
    candidate_id: int = Field(foreign_key="interview_candidate.id", nullable=False, description="候选人ID")
    interviewer_id: int = Field(foreign_key="user_account.id", nullable=False, description="面试官ID")
    
    # 面试记录
    notes: Optional[str] = Field(default=None, description="面试记录文本")
    summary: Optional[str] = Field(default=None, description="面试总结")
    
    # 文件
    recording_url: Optional[str] = Field(default=None, max_length=500, description="录音文件URL")
    face_image_url: Optional[str] = Field(default=None, max_length=500, description="候选人照片URL")
    
    # 录音转写
    transcript_status: int = Field(default=0, nullable=False, description="转写状态：0待处理 1处理中 2已完成 3失败")
    transcript_text: Optional[str] = Field(default=None, description="转写文本")
    
    # 评分
    total_score: Optional[float] = Field(default=None, description="总分")
    status: int = Field(default=0, nullable=False, description="状态：0待评分 1已评分")
    
    # 时间
    started_at: Optional[datetime] = Field(default=None, description="开始时间")
    completed_at: Optional[datetime] = Field(default=None, description="完成时间")
    
    # 关联关系
    session: Optional["InterviewSession"] = Relationship(back_populates="records")
    candidate: Optional["InterviewCandidate"] = Relationship()
    interviewer: Optional["UserAccount"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[InterviewRecord.interviewer_id]"}
    )
    scores: list["InterviewScore"] = Relationship(back_populates="record")


class ScoreTemplate(BaseModel, table=True):
    """
    评分模板表
    """
    __tablename__ = "score_template"

    club_id: Optional[int] = Field(default=None, foreign_key="club.id", description="社团ID（None表示系统模板）")
    name: str = Field(max_length=100, nullable=False, description="模板名称")
    description: Optional[str] = Field(default=None, description="模板描述")
    status: int = Field(default=1, nullable=False, description="状态：1启用 0禁用")
    
    # 关联关系
    club: Optional["Club"] = Relationship()
    items: list["ScoreItem"] = Relationship(back_populates="template")


class ScoreItem(BaseModel, table=True):
    """
    评分项表
    """
    __tablename__ = "score_item"

    template_id: int = Field(foreign_key="score_template.id", nullable=False, description="模板ID")
    title: str = Field(max_length=100, nullable=False, description="评分项标题")
    description: Optional[str] = Field(default=None, description="评分项描述")
    weight: float = Field(default=1.0, nullable=False, description="权重")
    max_score: float = Field(default=100.0, nullable=False, description="满分")
    order: int = Field(default=0, nullable=False, description="排序")
    
    # 关联关系
    template: Optional["ScoreTemplate"] = Relationship(back_populates="items")
    scores: list["InterviewScore"] = Relationship(back_populates="item")


class InterviewScore(BaseModel, table=True):
    """
    面试评分明细表
    """
    __tablename__ = "interview_score"

    record_id: int = Field(foreign_key="interview_record.id", nullable=False, description="面试记录ID")
    item_id: int = Field(foreign_key="score_item.id", nullable=False, description="评分项ID")
    score: float = Field(nullable=False, description="得分")
    comment: Optional[str] = Field(default=None, description="评分备注")
    
    # 关联关系
    record: Optional["InterviewRecord"] = Relationship(back_populates="scores")
    item: Optional["ScoreItem"] = Relationship(back_populates="scores")

