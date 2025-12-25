"""
权限服务：处理RBAC权限验证
"""
from typing import List, Optional
from sqlmodel import Session, select

from app.models.role import Role, Permission, UserRole, RolePermission
from app.repositories.base import BaseRepository


class PermissionService:
    """权限服务"""

    def get_user_roles(
        self, session: Session, user_id: int
    ) -> List[Role]:
        """获取用户的所有角色"""
        stmt = (
            select(Role)
            .join(UserRole, Role.id == UserRole.role_id)
            .where(UserRole.user_id == user_id)
            .where(UserRole.is_deleted == 0)
            .where(UserRole.status == 1)
            .where(Role.is_deleted == 0)
            .where(Role.status == 1)
        )
        return list(session.exec(stmt).all())

    def get_role_permissions(
        self, session: Session, role_id: int
    ) -> List[Permission]:
        """获取角色的所有权限"""
        stmt = (
            select(Permission)
            .join(RolePermission, Permission.id == RolePermission.permission_id)
            .where(RolePermission.role_id == role_id)
            .where(RolePermission.is_deleted == 0)
            .where(Permission.is_deleted == 0)
            .where(Permission.status == 1)
        )
        return list(session.exec(stmt).all())

    def get_user_permissions(
        self, session: Session, user_id: int
    ) -> List[Permission]:
        """获取用户的所有权限（通过角色）"""
        roles = self.get_user_roles(session, user_id)
        all_permissions = []
        permission_ids = set()
        
        for role in roles:
            permissions = self.get_role_permissions(session, role.id)
            for perm in permissions:
                if perm.id not in permission_ids:
                    all_permissions.append(perm)
                    permission_ids.add(perm.id)
        
        return all_permissions

    def has_permission(
        self, session: Session, user_id: int, permission_code: str
    ) -> bool:
        """检查用户是否有指定权限"""
        permissions = self.get_user_permissions(session, user_id)
        return any(perm.code == permission_code for perm in permissions)

    def has_role(
        self, session: Session, user_id: int, role_code: str
    ) -> bool:
        """检查用户是否有指定角色"""
        roles = self.get_user_roles(session, user_id)
        return any(role.code == role_code for role in roles)

    def assign_role(
        self, session: Session, user_id: int, role_id: int
    ) -> UserRole:
        """为用户分配角色"""
        # 检查是否已有该角色
        stmt = (
            select(UserRole)
            .where(UserRole.user_id == user_id)
            .where(UserRole.role_id == role_id)
            .where(UserRole.is_deleted == 0)
        )
        existing = session.exec(stmt).first()
        if existing:
            return existing

        # 创建角色分配
        user_role = UserRole(
            user_id=user_id,
            role_id=role_id,
            status=1,
        )
        session.add(user_role)
        session.commit()
        session.refresh(user_role)
        return user_role

    def revoke_role(
        self, session: Session, user_id: int, role_id: int
    ) -> None:
        """撤销用户角色"""
        stmt = (
            select(UserRole)
            .where(UserRole.user_id == user_id)
            .where(UserRole.role_id == role_id)
            .where(UserRole.is_deleted == 0)
        )
        user_role = session.exec(stmt).first()
        if user_role:
            user_role.soft_delete()
            session.add(user_role)
            session.commit()

