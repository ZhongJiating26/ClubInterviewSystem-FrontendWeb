"""
服务层：封装业务逻辑
"""
from app.services.auth_service import AuthService
from app.services.club_service import ClubService
from app.services.recruitment_service import RecruitmentService
from app.services.permission_service import PermissionService

__all__ = ["AuthService", "ClubService", "RecruitmentService", "PermissionService"]

