from typing import Optional, List
from sqlmodel import Session, select
from app.models.role import Role, Permission, RolePermission, UserRole
from app.repositories.base import BaseRepository


class RoleRepository(BaseRepository[Role]):
    def __init__(self):
        super().__init__(Role)

    def get_by_code(self, session: Session, code: str) -> Optional[Role]:
        """根据角色代码查询"""
        stmt = (
            select(Role)
            .where(Role.code == code)
            .where(Role.is_deleted == 0)
            .where(Role.status == 1)
        )
        return session.exec(stmt).first()


class PermissionRepository(BaseRepository[Permission]):
    def __init__(self):
        super().__init__(Permission)

    def get_by_code(self, session: Session, code: str) -> Optional[Permission]:
        """根据权限代码查询"""
        stmt = (
            select(Permission)
            .where(Permission.code == code)
            .where(Permission.is_deleted == 0)
            .where(Permission.status == 1)
        )
        return session.exec(stmt).first()


class UserRoleRepository(BaseRepository[UserRole]):
    def __init__(self):
        super().__init__(UserRole)

    def get_user_roles(self, session: Session, user_id: int) -> List[Role]:
        """获取用户的所有角色"""
        stmt = (
            select(UserRole, Role)
            .join(Role, UserRole.role_id == Role.id)
            .where(UserRole.user_id == user_id)
            .where(UserRole.is_deleted == 0)
            .where(UserRole.status == 1)
            .where(Role.is_deleted == 0)
            .where(Role.status == 1)
        )
        results = session.exec(stmt).all()
        return [role for _, role in results]

    def get_user_role_ids(self, session: Session, user_id: int) -> List[int]:
        """获取用户的所有角色ID"""
        stmt = (
            select(UserRole.role_id)
            .where(UserRole.user_id == user_id)
            .where(UserRole.is_deleted == 0)
            .where(UserRole.status == 1)
        )
        return list(session.exec(stmt).all())

    def has_role(self, session: Session, user_id: int, role_code: str) -> bool:
        """检查用户是否拥有指定角色"""
        stmt = (
            select(UserRole, Role)
            .join(Role, UserRole.role_id == Role.id)
            .where(UserRole.user_id == user_id)
            .where(Role.code == role_code)
            .where(UserRole.is_deleted == 0)
            .where(UserRole.status == 1)
            .where(Role.is_deleted == 0)
            .where(Role.status == 1)
        )
        return session.exec(stmt).first() is not None


class RolePermissionRepository(BaseRepository[RolePermission]):
    def __init__(self):
        super().__init__(RolePermission)

    def get_role_permissions(self, session: Session, role_id: int) -> List[Permission]:
        """获取角色的所有权限"""
        stmt = (
            select(RolePermission, Permission)
            .join(Permission, RolePermission.permission_id == Permission.id)
            .where(RolePermission.role_id == role_id)
            .where(RolePermission.is_deleted == 0)
            .where(Permission.is_deleted == 0)
            .where(Permission.status == 1)
        )
        results = session.exec(stmt).all()
        return [permission for _, permission in results]

    def get_role_permission_codes(self, session: Session, role_id: int) -> List[str]:
        """获取角色的所有权限代码"""
        stmt = (
            select(Permission.code)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .where(RolePermission.role_id == role_id)
            .where(RolePermission.is_deleted == 0)
            .where(Permission.is_deleted == 0)
            .where(Permission.status == 1)
        )
        return list(session.exec(stmt).all())

    def user_has_permission(self, session: Session, user_id: int, permission_code: str) -> bool:
        """检查用户是否拥有指定权限（通过角色）"""
        # 1. 获取用户的所有角色ID
        user_role_repo = UserRoleRepository()
        role_ids = user_role_repo.get_user_role_ids(session, user_id)
        
        if not role_ids:
            return False

        # 2. 检查这些角色是否拥有指定权限
        stmt = (
            select(RolePermission, Permission)
            .join(Permission, RolePermission.permission_id == Permission.id)
            .where(RolePermission.role_id.in_(role_ids))
            .where(Permission.code == permission_code)
            .where(RolePermission.is_deleted == 0)
            .where(Permission.is_deleted == 0)
            .where(Permission.status == 1)
        )
        return session.exec(stmt).first() is not None

