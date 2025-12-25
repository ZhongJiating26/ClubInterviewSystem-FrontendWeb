"""
权限检查依赖
"""
from typing import List
from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from app.api.deps import get_current_user
from app.models.user_account import UserAccount
from app.db.session import get_session
from app.repositories.role import UserRoleRepository, RolePermissionRepository


user_role_repo = UserRoleRepository()
role_permission_repo = RolePermissionRepository()


def require_permissions(*permission_codes: str):
    """
    权限检查装饰器工厂
    用法：
    @router.get("/admin/users")
    def get_users(
        current_user: UserAccount = Depends(require_permissions("user:read", "admin:access"))
    ):
        ...
    """
    def permission_checker(
        current_user: UserAccount = Depends(get_current_user),
        session: Session = Depends(get_session),
    ) -> UserAccount:
        """检查用户是否拥有所需权限"""
        for permission_code in permission_codes:
            if not role_permission_repo.user_has_permission(session, current_user.id, permission_code):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"缺少权限: {permission_code}",
                )
        return current_user
    
    return permission_checker


def require_roles(*role_codes: str):
    """
    角色检查装饰器工厂
    用法：
    @router.get("/admin/dashboard")
    def admin_dashboard(
        current_user: UserAccount = Depends(require_roles("admin"))
    ):
        ...
    """
    def role_checker(
        current_user: UserAccount = Depends(get_current_user),
        session: Session = Depends(get_session),
    ) -> UserAccount:
        """检查用户是否拥有所需角色"""
        for role_code in role_codes:
            if not user_role_repo.has_role(session, current_user.id, role_code):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"缺少角色: {role_code}",
                )
        return current_user
    
    return role_checker


def get_user_permissions(
    current_user: UserAccount = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> List[str]:
    """
    获取当前用户的所有权限代码
    """
    user_role_repo = UserRoleRepository()
    role_ids = user_role_repo.get_user_role_ids(session, current_user.id)
    
    if not role_ids:
        return []
    
    all_permissions = []
    for role_id in role_ids:
        permissions = role_permission_repo.get_role_permission_codes(session, role_id)
        all_permissions.extend(permissions)
    
    # 去重
    return list(set(all_permissions))

