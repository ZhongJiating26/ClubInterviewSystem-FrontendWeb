"""
社团服务：处理社团相关的业务逻辑
"""
from typing import Optional, List
from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.club import Club, ClubMember
from app.models.user_account import UserAccount
from app.repositories.club import ClubRepository, ClubMemberRepository


class ClubService:
    """社团服务"""

    def __init__(self):
        self.club_repo = ClubRepository()
        self.member_repo = ClubMemberRepository()

    def create_club(
        self,
        session: Session,
        *,
        name: str,
        description: Optional[str],
        school_id: Optional[int],
        president_id: int,
        logo_url: Optional[str] = None,
        cover_url: Optional[str] = None,
    ) -> Club:
        """
        创建社团
        - 检查社长是否已创建其他社团（可选限制）
        - 创建社团
        - 自动将社长添加为成员
        """
        # 创建社团
        club = Club(
            name=name,
            description=description,
            school_id=school_id,
            president_id=president_id,
            logo_url=logo_url,
            cover_url=cover_url,
            status=1,
            member_count=0,
        )
        club = self.club_repo.create(session, club)

        # 自动将社长添加为成员
        member = ClubMember(
            club_id=club.id,
            user_id=president_id,
            role="president",
            status=1,
        )
        self.member_repo.create(session, member)

        # 更新成员数量
        club.member_count = 1
        session.add(club)
        session.commit()
        session.refresh(club)

        return club

    def get_club(self, session: Session, club_id: int) -> Club:
        """获取社团详情"""
        club = self.club_repo.get(session, club_id)
        if not club:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="社团不存在",
            )
        return club

    def list_clubs(
        self,
        session: Session,
        *,
        school_id: Optional[int] = None,
        keyword: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> List[Club]:
        """获取社团列表"""
        if keyword:
            clubs = self.club_repo.search_by_name(session, keyword)
        elif school_id:
            clubs = self.club_repo.get_by_school(session, school_id)
        else:
            clubs = self.club_repo.list(session, offset=offset, limit=limit)
        return clubs

    def update_club(
        self,
        session: Session,
        *,
        club: Club,
        name: Optional[str] = None,
        description: Optional[str] = None,
        logo_url: Optional[str] = None,
        cover_url: Optional[str] = None,
    ) -> Club:
        """更新社团信息"""
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        if logo_url is not None:
            update_data["logo_url"] = logo_url
        if cover_url is not None:
            update_data["cover_url"] = cover_url

        if update_data:
            club = self.club_repo.update(session, club, update_data)
        return club

    def add_member(
        self,
        session: Session,
        *,
        club_id: int,
        user_id: int,
        role: str = "member",
    ) -> ClubMember:
        """添加成员"""
        # 检查是否已是成员
        existing = self.member_repo.get_by_club_and_user(session, club_id, user_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户已是该社团成员",
            )

        # 创建成员关系
        member = ClubMember(
            club_id=club_id,
            user_id=user_id,
            role=role,
            status=1,
        )
        member = self.member_repo.create(session, member)

        # 更新成员数量
        club = self.club_repo.get(session, club_id)
        if club:
            club.member_count += 1
            session.add(club)
            session.commit()

        return member

    def remove_member(
        self,
        session: Session,
        *,
        club_id: int,
        user_id: int,
    ) -> None:
        """移除成员"""
        member = self.member_repo.get_by_club_and_user(session, club_id, user_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="成员不存在",
            )

        # 软删除成员
        self.member_repo.soft_delete(session, member)

        # 更新成员数量
        club = self.club_repo.get(session, club_id)
        if club:
            club.member_count = max(0, club.member_count - 1)
            session.add(club)
            session.commit()

    def get_members(self, session: Session, club_id: int) -> List[ClubMember]:
        """获取社团成员列表"""
        return self.member_repo.get_by_club(session, club_id)

    def check_user_is_president(
        self, session: Session, club: Club, user_id: int
    ) -> bool:
        """检查用户是否是社长"""
        return club.president_id == user_id

    def check_user_is_member(
        self, session: Session, club_id: int, user_id: int
    ) -> bool:
        """检查用户是否是成员"""
        member = self.member_repo.get_by_club_and_user(session, club_id, user_id)
        return member is not None

