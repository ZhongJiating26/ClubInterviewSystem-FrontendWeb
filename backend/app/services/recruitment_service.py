"""
招新服务：处理招新相关的业务逻辑
"""
from typing import Optional, List
from datetime import datetime
from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.recruitment import Recruitment, Application, Interview
from app.models.user_account import UserAccount
from app.repositories.recruitment import (
    RecruitmentRepository,
    ApplicationRepository,
    InterviewRepository,
)
from app.repositories.club import ClubRepository


class RecruitmentService:
    """招新服务"""

    def __init__(self):
        self.recruitment_repo = RecruitmentRepository()
        self.application_repo = ApplicationRepository()
        self.interview_repo = InterviewRepository()
        self.club_repo = ClubRepository()

    def create_recruitment(
        self,
        session: Session,
        *,
        club_id: int,
        title: str,
        description: Optional[str],
        start_time: datetime,
        end_time: datetime,
        interview_start_time: Optional[datetime] = None,
        interview_end_time: Optional[datetime] = None,
    ) -> Recruitment:
        """创建招新活动"""
        # 检查社团是否存在
        club = self.club_repo.get(session, club_id)
        if not club:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="社团不存在",
            )

        # 检查时间逻辑
        if end_time <= start_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="结束时间必须晚于开始时间",
            )

        # 创建招新活动
        recruitment = Recruitment(
            club_id=club_id,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            interview_start_time=interview_start_time,
            interview_end_time=interview_end_time,
            status=0,  # 待发布
            application_count=0,
        )
        return self.recruitment_repo.create(session, recruitment)

    def publish_recruitment(
        self, session: Session, recruitment: Recruitment
    ) -> Recruitment:
        """发布招新活动"""
        if recruitment.status != 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="只能发布待发布状态的招新活动",
            )

        # 检查时间
        now = datetime.utcnow()
        if recruitment.end_time < now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="招新活动已过期，无法发布",
            )

        recruitment.status = 1  # 进行中
        session.add(recruitment)
        session.commit()
        session.refresh(recruitment)
        return recruitment

    def get_recruitment(self, session: Session, recruitment_id: int) -> Recruitment:
        """获取招新详情"""
        recruitment = self.recruitment_repo.get(session, recruitment_id)
        if not recruitment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="招新活动不存在",
            )
        return recruitment

    def list_recruitments(
        self,
        session: Session,
        *,
        club_id: Optional[int] = None,
        status: Optional[int] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> List[Recruitment]:
        """获取招新列表"""
        if club_id:
            recruitments = self.recruitment_repo.get_by_club(session, club_id)
        elif status == 1:
            recruitments = self.recruitment_repo.get_active(session)
        else:
            recruitments = self.recruitment_repo.list(
                session, offset=offset, limit=limit
            )
        return recruitments

    def create_application(
        self,
        session: Session,
        *,
        recruitment_id: int,
        user_id: int,
        motivation: Optional[str] = None,
        experience: Optional[str] = None,
        skills: Optional[str] = None,
    ) -> Application:
        """创建报名申请"""
        # 检查招新活动是否存在且可报名
        recruitment = self.recruitment_repo.get(session, recruitment_id)
        if not recruitment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="招新活动不存在",
            )

        if recruitment.status != 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="招新活动未开始或已结束",
            )

        # 检查时间
        now = datetime.utcnow()
        if now < recruitment.start_time or now > recruitment.end_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="不在报名时间内",
            )

        # 检查是否已申请
        existing = self.application_repo.get_by_recruitment_and_user(
            session, recruitment_id, user_id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="您已申请过该招新活动",
            )

        # 创建申请
        application = Application(
            recruitment_id=recruitment_id,
            user_id=user_id,
            motivation=motivation,
            experience=experience,
            skills=skills,
            status=0,  # 待审核
        )
        application = self.application_repo.create(session, application)

        # 更新报名人数
        recruitment.application_count += 1
        session.add(recruitment)
        session.commit()

        return application

    def review_application(
        self,
        session: Session,
        *,
        application: Application,
        reviewer_id: int,
        approved: bool,
        comment: Optional[str] = None,
    ) -> Application:
        """审核申请"""
        if application.status != 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该申请已审核",
            )

        application.status = 1 if approved else 2
        application.reviewed_by = reviewer_id
        application.reviewed_at = datetime.utcnow()
        application.review_comment = comment

        session.add(application)
        session.commit()
        session.refresh(application)

        return application

    def create_interview(
        self,
        session: Session,
        *,
        application_id: int,
        interviewer_id: int,
        scheduled_time: datetime,
        duration: int = 30,
        location: Optional[str] = None,
    ) -> Interview:
        """创建面试安排"""
        # 检查申请是否存在且已通过
        application = self.application_repo.get(session, application_id)
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="申请不存在",
            )

        if application.status != 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="只能为已通过的申请安排面试",
            )

        # 检查是否已有面试安排
        existing = self.interview_repo.get_by_application(session, application_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该申请已有面试安排",
            )

        # 创建面试
        interview = Interview(
            application_id=application_id,
            interviewer_id=interviewer_id,
            scheduled_time=scheduled_time,
            duration=duration,
            location=location,
            status=0,  # 待面试
        )
        return self.interview_repo.create(session, interview)

    def complete_interview(
        self,
        session: Session,
        *,
        interview: Interview,
        result: int,
        score: Optional[float] = None,
        comment: Optional[str] = None,
    ) -> Interview:
        """完成面试"""
        interview.status = 2  # 已完成
        interview.result = result
        interview.score = score
        interview.comment = comment
        interview.completed_at = datetime.utcnow()

        session.add(interview)
        session.commit()
        session.refresh(interview)

        return interview

