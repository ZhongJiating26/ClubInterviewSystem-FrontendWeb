from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user_account import UserAccount


class Role(BaseModel, table=True):
    """
    角色表：定义系统中的角色（如：管理员、社长、成员、申请人等）
    """
    __tablename__ = "role"

    name: str = Field(max_length=50, nullable=False, unique=True, description="角色名称")
    code: str = Field(max_length=50, nullable=False, unique=True, description="角色代码（如：admin, president, member, applicant）")
    description: Optional[str] = Field(default=None, max_length=255, description="角色描述")
    status: int = Field(default=1, nullable=False, description="状态：1启用 0禁用")

    # 关联关系
    user_roles: list["UserRole"] = Relationship(back_populates="role")
    role_permissions: list["RolePermission"] = Relationship(back_populates="role")


class Permission(BaseModel, table=True):
    """
    权限表：定义系统中的权限（如：创建社团、审核申请、管理成员等）
    """
    __tablename__ = "permission"

    name: str = Field(max_length=50, nullable=False, unique=True, description="权限名称")
    code: str = Field(max_length=100, nullable=False, unique=True, description="权限代码（如：club:create, application:review）")
    description: Optional[str] = Field(default=None, max_length=255, description="权限描述")
    resource: Optional[str] = Field(default=None, max_length=50, description="资源类型（如：club, application, user）")
    action: Optional[str] = Field(default=None, max_length=50, description="操作类型（如：create, read, update, delete）")
    status: int = Field(default=1, nullable=False, description="状态：1启用 0禁用")

    # 关联关系
    role_permissions: list["RolePermission"] = Relationship(back_populates="permission")


class RolePermission(BaseModel, table=True):
    """
    角色权限关联表：多对多关系
    """
    __tablename__ = "role_permission"

    role_id: int = Field(foreign_key="role.id", nullable=False, description="角色ID")
    permission_id: int = Field(foreign_key="permission.id", nullable=False, description="权限ID")

    # 关联关系
    role: Role = Relationship(back_populates="role_permissions")
    permission: Permission = Relationship(back_populates="role_permissions")


class UserRole(BaseModel, table=True):
    """
    用户角色关联表：多对多关系
    """
    __tablename__ = "user_role"

    user_id: int = Field(foreign_key="user_account.id", nullable=False, description="用户ID")
    role_id: int = Field(foreign_key="role.id", nullable=False, description="角色ID")
    status: int = Field(default=1, nullable=False, description="状态：1启用 0禁用")

    # 关联关系
    role: Role = Relationship(back_populates="user_roles")

