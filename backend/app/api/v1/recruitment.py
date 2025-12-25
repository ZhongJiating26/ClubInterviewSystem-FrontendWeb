"""
招新管理API
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session

from app.api.deps import get_current_user
from app.db.session import get_session
from app.models.user_account import UserAccount
from app.models.recruitment import Recruitment, Application, Interview
from app.services.recruitment_service import RecruitmentService
from app.services.club_service import ClubService
from app.schemas.recruitment import (
    RecruitmentCreateRequest,
    RecruitmentResponse,
    ApplicationCreateRequest,
    ApplicationResponse,
    ApplicationReviewRequest,
    InterviewCreateRequest,
    InterviewResponse,
    InterviewCompleteRequest,
)

router = APIRouter(prefix="/recruitments", tags=["招新管理"])
recruitment_service = RecruitmentService()
club_service = ClubService()


@router.post("", response_model=RecruitmentResponse, status_code=201)
def create_recruitment(
    data: RecruitmentCreateRequest,
    session: Session = Depends(get_session),
    current_user: UserAccount = Depends(get_current_user),
):
    """创建招新活动（仅社长可操作）"""
    # 检查权限：必须是社长
    club = club_service.get_club(session, data.club_id)
    if not club_service.check_user_is_president(session, club, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有社长可以创建招新活动",
        )

    recruitment = recruitment_service.create_recruitment(
        session,
        club_id=data.club_id,
        title=data.title,
        description=data.description,
        start_time=data.start_time,
        end_time=data.end_time,
        interview_start_time=data.interview_start_time,
        interview_end_time=data.interview_end_time,
    )
    return RecruitmentResponse.model_validate(recruitment)


@router.post("/{recruitment_id}/publish", response_model=RecruitmentResponse)
def publish_recruitment(
    recruitment_id: int,
    session: Session = Depends(get_session),
    current_user: UserAccount = Depends(get_current_user),
):
    """发布招新活动（仅社长可操作）"""
    recruitment = recruitment_service.get_recruitment(session, recruitment_id)
    
    # 检查权限
    club = club_service.get_club(session, recruitment.club_id)
    if not club_service.check_user_is_president(session, club, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有社长可以发布招新活动",
        )

    recruitment = recruitment_service.publish_recruitment(session, recruitment)
    return RecruitmentResponse.model_validate(recruitment)


@router.get("/{recruitment_id}", response_model=RecruitmentResponse)
def get_recruitment(
    recruitment_id: int,
    session: Session = Depends(get_session),
):
    """获取招新详情"""
    recruitment = recruitment_service.get_recruitment(session, recruitment_id)
    return RecruitmentResponse.model_validate(recruitment)


@router.get("", response_model=List[RecruitmentResponse])
def list_recruitments(
    club_id: Optional[int] = Query(None, description="社团ID筛选"),
    status: Optional[int] = Query(None, description="状态筛选：0待发布 1进行中 2已结束 3已取消"),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    """获取招新列表"""
    recruitments = recruitment_service.list_recruitments(
        session,
        club_id=club_id,
        status=status,
        offset=offset,
        limit=limit,
    )
    return [RecruitmentResponse.model_validate(r) for r in recruitments]


@router.post("/applications", response_model=ApplicationResponse, status_code=201)
def create_application(
    data: ApplicationCreateRequest,
    session: Session = Depends(get_session),
    current_user: UserAccount = Depends(get_current_user),
):
    """创建报名申请"""
    application = recruitment_service.create_application(
        session,
        recruitment_id=data.recruitment_id,
        user_id=current_user.id,
        motivation=data.motivation,
        experience=data.experience,
        skills=data.skills,
    )
    return ApplicationResponse.model_validate(application)


@router.get("/applications/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: int,
    session: Session = Depends(get_session),
):
    """获取申请详情"""
    from app.repositories.recruitment import ApplicationRepository
    repo = ApplicationRepository()
    application = repo.get(session, application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="申请不存在",
        )
    return ApplicationResponse.model_validate(application)


@router.get("/applications", response_model=List[ApplicationResponse])
def list_applications(
    recruitment_id: Optional[int] = Query(None, description="招新ID筛选"),
    session: Session = Depends(get_session),
    current_user: Optional[UserAccount] = Depends(get_current_user),
):
    """获取申请列表"""
    from app.repositories.recruitment import ApplicationRepository
    repo = ApplicationRepository()
    
    if recruitment_id:
        applications = repo.get_by_recruitment(session, recruitment_id)
    elif current_user:
        applications = repo.get_by_user(session, current_user.id)
    else:
        applications = repo.list(session)
    
    return [ApplicationResponse.model_validate(a) for a in applications]


@router.get("/applications/my", response_model=List[ApplicationResponse])
def get_my_applications(
    session: Session = Depends(get_session),
    current_user: UserAccount = Depends(get_current_user),
):
    """获取当前用户的申请列表"""
    from app.repositories.recruitment import ApplicationRepository
    repo = ApplicationRepository()
    applications = repo.get_by_user(session, current_user.id)
    
    # 获取招新标题
    result = []
    for app in applications:
        app_dict = ApplicationResponse.model_validate(app).model_dump()
        try:
            recruitment = recruitment_service.get_recruitment(session, app.recruitment_id)
            app_dict["recruitment_title"] = recruitment.title
        except:
            pass
        result.append(app_dict)
    
    return result


@router.post("/applications/{application_id}/review", response_model=ApplicationResponse)
def review_application(
    application_id: int,
    data: ApplicationReviewRequest,
    session: Session = Depends(get_session),
    current_user: UserAccount = Depends(get_current_user),
):
    """审核申请（仅社长可操作）"""
    from app.repositories.recruitment import ApplicationRepository
    repo = ApplicationRepository()
    application = repo.get(session, application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="申请不存在",
        )

    # 检查权限：必须是社长
    recruitment = recruitment_service.get_recruitment(session, application.recruitment_id)
    club = club_service.get_club(session, recruitment.club_id)
    if not club_service.check_user_is_president(session, club, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有社长可以审核申请",
        )

    application = recruitment_service.review_application(
        session,
        application=application,
        reviewer_id=current_user.id,
        approved=data.approved,
        comment=data.comment,
    )
    return ApplicationResponse.model_validate(application)


@router.post("/interviews", response_model=InterviewResponse, status_code=201)
def create_interview(
    data: InterviewCreateRequest,
    session: Session = Depends(get_session),
    current_user: UserAccount = Depends(get_current_user),
):
    """创建面试安排（仅社长可操作）"""
    # 检查权限
    from app.repositories.recruitment import ApplicationRepository
    app_repo = ApplicationRepository()
    application = app_repo.get(session, data.application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="申请不存在",
        )

    recruitment = recruitment_service.get_recruitment(session, application.recruitment_id)
    club = club_service.get_club(session, recruitment.club_id)
    if not club_service.check_user_is_president(session, club, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有社长可以安排面试",
        )

    interview = recruitment_service.create_interview(
        session,
        application_id=data.application_id,
        interviewer_id=data.interviewer_id,
        scheduled_time=data.scheduled_time,
        duration=data.duration,
        location=data.location,
    )
    return InterviewResponse.model_validate(interview)


@router.get("/interviews/{interview_id}", response_model=InterviewResponse)
def get_interview(
    interview_id: int,
    session: Session = Depends(get_session),
):
    """获取面试详情"""
    from app.repositories.recruitment import InterviewRepository
    repo = InterviewRepository()
    interview = repo.get(session, interview_id)
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="面试不存在",
        )
    return InterviewResponse.model_validate(interview)


@router.post("/interviews/{interview_id}/complete", response_model=InterviewResponse)
def complete_interview(
    interview_id: int,
    data: InterviewCompleteRequest,
    session: Session = Depends(get_session),
    current_user: UserAccount = Depends(get_current_user),
):
    """完成面试（仅面试官可操作）"""
    from app.repositories.recruitment import InterviewRepository
    repo = InterviewRepository()
    interview = repo.get(session, interview_id)
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="面试不存在",
        )

    # 检查权限：必须是面试官
    if interview.interviewer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有面试官可以完成面试",
        )

    interview = recruitment_service.complete_interview(
        session,
        interview=interview,
        result=data.result,
        score=data.score,
        comment=data.comment,
    )
    return InterviewResponse.model_validate(interview)

