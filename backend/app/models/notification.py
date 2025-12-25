"""
通知相关模型
"""
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, Relationship
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user_account import UserAccount


class Notification(BaseModel, table=True):
    """
    通知表
    """
    __tablename__ = "notification"

    user_id: int = Field(foreign_key="user_account.id", nullable=False, description="接收用户ID")
    
    # 通知类型
    type: str = Field(max_length=50, nullable=False, description="通知类型：system, interview, application, ticket")
    
    # 通知标题和内容
    title: str = Field(max_length=200, nullable=False, description="通知标题")
    content: Optional[str] = Field(default=None, description="通知内容")
    
    # 关联资源
    related_type: Optional[str] = Field(default=None, max_length=50, description="关联资源类型：recruitment, application, interview, ticket")
    related_id: Optional[int] = Field(default=None, description="关联资源ID")
    
    # 状态
    is_read: int = Field(default=0, nullable=False, description="是否已读：1已读 0未读")
    read_at: Optional[datetime] = Field(default=None, description="阅读时间")
    
    # 关联关系
    user: Optional["UserAccount"] = Relationship()

