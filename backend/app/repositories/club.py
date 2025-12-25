"""
社团仓储
"""
from typing import Optional, List
from sqlmodel import Session, select
from app.models.club import Club, ClubMember
from app.repositories.base import BaseRepository


class ClubRepository(BaseRepository[Club]):
    """社团仓储"""

    def __init__(self):
        super().__init__(Club)

    def get_by_school(self, session: Session, school_id: int) -> List[Club]:
        """根据学校ID查询社团列表"""
        stmt = (
            self._base_stmt()
            .where(Club.school_id == school_id)
            .order_by(Club.created_at.desc())
        )
        return list(session.exec(stmt).all())

    def get_by_president(self, session: Session, president_id: int) -> List[Club]:
        """根据社长ID查询社团列表"""
        stmt = (
            self._base_stmt()
            .where(Club.president_id == president_id)
            .order_by(Club.created_at.desc())
        )
        return list(session.exec(stmt).all())

    def search_by_name(self, session: Session, keyword: str) -> List[Club]:
        """根据名称搜索社团"""
        stmt = (
            self._base_stmt()
            .where(Club.name.contains(keyword))
            .order_by(Club.created_at.desc())
        )
        return list(session.exec(stmt).all())


class ClubMemberRepository(BaseRepository[ClubMember]):
    """社团成员仓储"""

    def __init__(self):
        super().__init__(ClubMember)

    def get_by_club(self, session: Session, club_id: int) -> List[ClubMember]:
        """根据社团ID查询成员列表"""
        stmt = (
            self._base_stmt()
            .where(ClubMember.club_id == club_id)
            .order_by(ClubMember.created_at.desc())
        )
        return list(session.exec(stmt).all())

    def get_by_user(self, session: Session, user_id: int) -> List[ClubMember]:
        """根据用户ID查询加入的社团列表"""
        stmt = (
            self._base_stmt()
            .where(ClubMember.user_id == user_id)
            .order_by(ClubMember.created_at.desc())
        )
        return list(session.exec(stmt).all())

    def get_by_club_and_user(
        self, session: Session, club_id: int, user_id: int
    ) -> Optional[ClubMember]:
        """根据社团ID和用户ID查询成员关系"""
        stmt = (
            self._base_stmt()
            .where(ClubMember.club_id == club_id)
            .where(ClubMember.user_id == user_id)
        )
        return session.exec(stmt).first()

