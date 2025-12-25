from typing import Optional, List
from sqlmodel import Session, select
from app.models.major import Major
from app.repositories.base import BaseRepository


class MajorRepository(BaseRepository[Major]):
    def __init__(self):
        super().__init__(Major)

    def get_by_school(self, session: Session, school_id: Optional[int] = None) -> List[Major]:
        """
        获取专业列表
        - 如果school_id为None，返回通用专业
        - 如果school_id有值，返回该学校的专业
        """
        stmt = self._base_stmt()
        
        if school_id is None:
            # 通用专业（school_id为NULL）
            stmt = stmt.where(Major.school_id.is_(None))
        else:
            # 指定学校的专业
            stmt = stmt.where(Major.school_id == school_id)
        
        stmt = stmt.order_by(Major.name)
        return list(session.exec(stmt).all())

    def search_by_keyword(self, session: Session, keyword: str) -> List[Major]:
        """根据关键词搜索专业"""
        stmt = (
            self._base_stmt()
            .where(Major.name.contains(keyword))
            .order_by(Major.name)
        )
        return list(session.exec(stmt).all())

