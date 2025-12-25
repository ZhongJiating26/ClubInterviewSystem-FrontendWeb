"""
认证服务：处理用户注册、登录、初始化等业务逻辑
"""
from typing import Optional
from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.user_account import UserAccount
from app.repositories.user_account import UserAccountRepository
from app.core.security import create_access_token
from app.schemas.auth import (
    InitAccountRequest,
    ChangePasswordRequest,
)


class AuthService:
    """认证服务"""

    def __init__(self):
        self.user_repo = UserAccountRepository()

    def register(
        self,
        session: Session,
        *,
        phone: str,
        password: str,
        name: Optional[str] = None,
        school_id: Optional[int] = None,
    ) -> UserAccount:
        """
        用户注册
        - 检查手机号是否已注册
        - 创建用户（密码哈希）
        """
        # 检查手机号是否已注册
        existing = self.user_repo.get_by_phone(session, phone)
        if existing:
            raise HTTPException(
                status_code=400,
                detail="手机号已注册",
            )

        # 创建用户
        user = self.user_repo.create_user(
            session,
            phone=phone,
            password=password,
            name=name,
            school_id=school_id,
        )

        return user

    def login(
        self,
        session: Session,
        *,
        phone: str,
        password: str,
    ) -> dict:
        """
        用户登录
        - 验证用户存在
        - 验证用户状态
        - 验证账号已初始化
        - 验证密码
        - 签发JWT
        """
        # 查询用户
        user = self.user_repo.get_by_phone(session, phone)
        if not user:
            raise HTTPException(
                status_code=400,
                detail="手机号或密码错误",
            )

        # 校验状态
        if user.status != 1:
            raise HTTPException(
                status_code=403,
                detail="用户已被禁用",
            )

        # 校验账号是否初始化
        if user.password_hash is None:
            raise HTTPException(
                status_code=403,
                detail="账号尚未初始化，请先完善账号信息",
            )

        # 校验密码
        if not self.user_repo.verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=400,
                detail="手机号或密码错误",
            )

        # 签发JWT
        token_payload = {
            "user_id": user.id,
            "token_version": user.token_version,
        }
        access_token = create_access_token(subject=token_payload)

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    def init_account(
        self,
        session: Session,
        *,
        user: UserAccount,
        data: InitAccountRequest,
    ) -> None:
        """
        账号初始化
        - 检查用户状态
        - 检查是否已初始化
        - 执行初始化
        """
        # 检查用户状态
        if user.status != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="用户已被禁用",
            )

        # 检查是否已初始化
        if user.password_hash is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="账号已初始化，无需重复初始化",
            )

        # 执行初始化
        self.user_repo.init_account(
            session,
            user=user,
            password=data.password,
            name=data.name,
            id_card_no=data.id_card_no,
            school_id=data.school_id,
            major=data.major,
            student_no=data.student_no,
            email=data.email,
            avatar_url=data.avatar_url,
        )

    def change_password(
        self,
        session: Session,
        *,
        user: UserAccount,
        data: ChangePasswordRequest,
    ) -> None:
        """
        修改密码
        - 检查用户状态
        - 检查是否已初始化
        - 验证旧密码
        - 设置新密码（会更新token_version使旧token失效）
        """
        # 检查用户状态
        if user.status != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="用户已被禁用",
            )

        # 检查是否已初始化
        if user.password_hash is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="账号尚未初始化，无法修改密码",
            )

        # 执行密码修改
        try:
            self.user_repo.change_password(
                session,
                user=user,
                old_password=data.old_password,
                new_password=data.new_password,
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )

