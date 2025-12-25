"""
工单（在线答疑）相关模型
"""
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, Relationship
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user_account import UserAccount


class Ticket(BaseModel, table=True):
    """
    工单表
    """
    __tablename__ = "ticket"

    user_id: int = Field(foreign_key="user_account.id", nullable=False, description="创建用户ID")
    
    # 工单信息
    title: str = Field(max_length=200, nullable=False, description="工单标题")
    content: str = Field(nullable=False, description="工单内容")
    
    # 工单类型
    category: Optional[str] = Field(default=None, max_length=50, description="工单分类：question, bug, suggestion等")
    
    # 状态
    status: int = Field(default=0, nullable=False, description="状态：0待处理 1处理中 2已解决 3已关闭")
    
    # 处理信息
    handler_id: Optional[int] = Field(default=None, foreign_key="user_account.id", description="处理人ID")
    handled_at: Optional[datetime] = Field(default=None, description="处理时间")
    solution: Optional[str] = Field(default=None, description="解决方案")
    
    # 关联关系
    user: Optional["UserAccount"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Ticket.user_id]"}
    )
    handler: Optional["UserAccount"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Ticket.handler_id]"}
    )
    replies: list["TicketReply"] = Relationship(back_populates="ticket")


class TicketReply(BaseModel, table=True):
    """
    工单回复表
    """
    __tablename__ = "ticket_reply"

    ticket_id: int = Field(foreign_key="ticket.id", nullable=False, description="工单ID")
    user_id: int = Field(foreign_key="user_account.id", nullable=False, description="回复用户ID")
    
    # 回复内容
    content: str = Field(nullable=False, description="回复内容")
    
    # 关联关系
    ticket: Optional["Ticket"] = Relationship(back_populates="replies")
    user: Optional["UserAccount"] = Relationship()

