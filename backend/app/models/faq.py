"""
FAQ（常见问题）相关模型
"""
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.club import Club
    from app.models.school import School


class FAQ(BaseModel, table=True):
    """
    常见问题表
    """
    __tablename__ = "faq"

    title: str = Field(max_length=200, nullable=False, description="问题标题")
    content: str = Field(nullable=False, description="问题内容/答案")
    
    # 分类
    category: Optional[str] = Field(default=None, max_length=50, description="分类：general, club, application, interview等")
    
    # 关联信息
    school_id: Optional[int] = Field(default=None, foreign_key="school.id", description="学校ID（None表示平台级FAQ）")
    club_id: Optional[int] = Field(default=None, foreign_key="club.id", description="社团ID（None表示学校级或平台级FAQ）")
    
    # 排序
    order: int = Field(default=0, nullable=False, description="排序")
    view_count: int = Field(default=0, nullable=False, description="查看次数")
    
    # 状态
    status: int = Field(default=1, nullable=False, description="状态：1启用 0禁用")
    
    # 关联关系
    school: Optional["School"] = Relationship()
    club: Optional["Club"] = Relationship()

