"""
社团管理API
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.api.deps import get_current_user
from app.db.session import get_session
from app.models.user_account import UserAccount
from app.models.club import Club
from app.services.club_service import ClubService
from app.schemas.club import (
    ClubCreateRequest,
    ClubUpdateRequest,
    ClubResponse,
    ClubMemberResponse,
    AddMemberRequest,
)

router = APIRouter(prefix="/clubs", tags=["社团管理"])
club_service = ClubService()


@router.post("", response_model=ClubResponse, status_code=201)
def create_club(
    data: ClubCreateRequest,
    session: Session = Depends(get_session),
    current_user: UserAccount = Depends(get_current_user),
):
    """创建社团"""
    club = club_service.create_club(
        session,
        name=data.name,
        description=data.description,
        school_id=data.school_id,
        president_id=current_user.id,
        logo_url=data.logo_url,
        cover_url=data.cover_url,
    )
    return ClubResponse.model_validate(club)


@router.get("/{club_id}", response_model=ClubResponse)
def get_club(
    club_id: int,
    session: Session = Depends(get_session),
):
    """获取社团详情"""
    club = club_service.get_club(session, club_id)
    return ClubResponse.model_validate(club)


@router.get("", response_model=List[ClubResponse])
def list_clubs(
    school_id: Optional[int] = Query(None, description="学校ID筛选"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session),
):
    """获取社团列表"""
    clubs = club_service.list_clubs(
        session,
        school_id=school_id,
        keyword=keyword,
        offset=offset,
        limit=limit,
    )
    return [ClubResponse.model_validate(club) for club in clubs]


@router.put("/{club_id}", response_model=ClubResponse)
def update_club(
    club_id: int,
    data: ClubUpdateRequest,
    session: Session = Depends(get_session),
    current_user: UserAccount = Depends(get_current_user),
):
    """更新社团信息（仅社长可操作）"""
    club = club_service.get_club(session, club_id)
    
    # 检查权限
    if not club_service.check_user_is_president(session, club, current_user.id):
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有社长可以修改社团信息",
        )

    club = club_service.update_club(
        session,
        club=club,
        name=data.name,
        description=data.description,
        logo_url=data.logo_url,
        cover_url=data.cover_url,
    )
    return ClubResponse.model_validate(club)


@router.post("/{club_id}/members", response_model=ClubMemberResponse, status_code=201)
def add_member(
    club_id: int,
    data: AddMemberRequest,
    session: Session = Depends(get_session),
    current_user: UserAccount = Depends(get_current_user),
):
    """添加成员（仅社长可操作）"""
    club = club_service.get_club(session, club_id)
    
    # 检查权限
    if not club_service.check_user_is_president(session, club, current_user.id):
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有社长可以添加成员",
        )

    member = club_service.add_member(
        session,
        club_id=club_id,
        user_id=data.user_id,
        role=data.role,
    )
    return ClubMemberResponse.model_validate(member)


@router.delete("/{club_id}/members/{user_id}")
def remove_member(
    club_id: int,
    user_id: int,
    session: Session = Depends(get_session),
    current_user: UserAccount = Depends(get_current_user),
):
    """移除成员（仅社长可操作）"""
    club = club_service.get_club(session, club_id)
    
    # 检查权限
    if not club_service.check_user_is_president(session, club, current_user.id):
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有社长可以移除成员",
        )

    club_service.remove_member(session, club_id=club_id, user_id=user_id)
    return {"message": "成员已移除"}


@router.get("/{club_id}/members", response_model=List[ClubMemberResponse])
def get_members(
    club_id: int,
    session: Session = Depends(get_session),
):
    """获取社团成员列表"""
    members = club_service.get_members(session, club_id)
    return [ClubMemberResponse.model_validate(member) for member in members]

