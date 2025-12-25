"""
招新相关仓储
"""
from typing import Optional, List
from sqlmodel import Session, select
from app.models.recruitment import Recruitment, Application, Interview
from app.repositories.base import BaseRepository


class RecruitmentRepository(BaseRepository[Recruitment]):
    """招新活动仓储"""

    def __init__(self):
        super().__init__(Recruitment)

    def get_by_club(self, session: Session, club_id: int) -> List[Recruitment]:
        """根据社团ID查询招新列表"""
        stmt = (
            self._base_stmt()
            .where(Recruitment.club_id == club_id)
            .order_by(Recruitment.created_at.desc())
        )
        return list(session.exec(stmt).all())

    def get_active(self, session: Session) -> List[Recruitment]:
        """查询进行中的招新活动"""
        stmt = (
            self._base_stmt()
            .where(Recruitment.status == 1)
            .order_by(Recruitment.created_at.desc())
        )
        return list(session.exec(stmt).all())


class ApplicationRepository(BaseRepository[Application]):
    """报名申请仓储"""

    def __init__(self):
        super().__init__(Application)

    def get_by_recruitment(
        self, session: Session, recruitment_id: int
    ) -> List[Application]:
        """根据招新ID查询申请列表"""
        stmt = (
            self._base_stmt()
            .where(Application.recruitment_id == recruitment_id)
            .order_by(Application.created_at.desc())
        )
        return list(session.exec(stmt).all())

    def get_by_user(self, session: Session, user_id: int) -> List[Application]:
        """根据用户ID查询申请列表"""
        stmt = (
            self._base_stmt()
            .where(Application.user_id == user_id)
            .order_by(Application.created_at.desc())
        )
        return list(session.exec(stmt).all())

    def get_by_recruitment_and_user(
        self, session: Session, recruitment_id: int, user_id: int
    ) -> Optional[Application]:
        """根据招新ID和用户ID查询申请"""
        stmt = (
            self._base_stmt()
            .where(Application.recruitment_id == recruitment_id)
            .where(Application.user_id == user_id)
        )
        return session.exec(stmt).first()


class InterviewRepository(BaseRepository[Interview]):
    """面试安排仓储"""

    def __init__(self):
        super().__init__(Interview)

    def get_by_application(
        self, session: Session, application_id: int
    ) -> Optional[Interview]:
        """根据申请ID查询面试安排"""
        stmt = (
            self._base_stmt()
            .where(Interview.application_id == application_id)
        )
        return session.exec(stmt).first()

    def get_by_interviewer(
        self, session: Session, interviewer_id: int
    ) -> List[Interview]:
        """根据面试官ID查询面试列表"""
        stmt = (
            self._base_stmt()
            .where(Interview.interviewer_id == interviewer_id)
            .order_by(Interview.scheduled_time)
        )
        return list(session.exec(stmt).all())

    def get_by_club(
        self, session: Session, club_id: int
    ) -> List[Interview]:
        """根据社团ID查询面试列表（需要通过application关联）"""
        from app.models.recruitment import Application
        stmt = (
            select(Interview)
            .join(Application, Interview.application_id == Application.id)
            .where(Interview.is_deleted == 0)
            .where(Application.is_deleted == 0)
            .where(Application.recruitment_id.in_(
                select(Recruitment.id)
                .where(Recruitment.club_id == club_id)
                .where(Recruitment.is_deleted == 0)
            ))
            .order_by(Interview.scheduled_time)
        )
        return list(session.exec(stmt).all())

