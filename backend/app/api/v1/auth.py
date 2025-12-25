from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.deps import get_current_user
from app.models.user_account import UserAccount
from app.db.session import get_session
from app.services.auth_service import AuthService
from app.schemas.auth import (
    InitAccountRequest,
    InitAccountResponse,
    AuthMeResponse,
    ChangePasswordRequest,
    ChangePasswordResponse,
)


class RegisterRequest(BaseModel):
    phone: str = Field(..., min_length=6, max_length=20)
    password: str = Field(..., min_length=6, max_length=72)  # bcrypt 限制 72 字节，哈希函数会自动截断
    name: str | None = None
    school_id: int | None = None

class LoginRequest(BaseModel):
    phone: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RegisterResponse(BaseModel):
    id: int
    phone: str
    name: str | None


router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()


@router.post("/register", response_model=RegisterResponse)
def register(
    data: RegisterRequest,
    session: Session = Depends(get_session),
):
    """用户注册"""
    user = auth_service.register(
        session,
        phone=data.phone,
        password=data.password,
        name=data.name,
        school_id=data.school_id,
    )
    return RegisterResponse(
        id=user.id,
        phone=user.phone,
        name=user.name,
    )


@router.post("/login", response_model=LoginResponse)
def login(
    data: LoginRequest,
    session: Session = Depends(get_session),
):
    """用户登录"""
    result = auth_service.login(
        session,
        phone=data.phone,
        password=data.password,
    )
    return LoginResponse(**result)


@router.get("/me", response_model=AuthMeResponse)
def me(current_user: UserAccount = Depends(get_current_user)):
    return AuthMeResponse(
        id=current_user.id,
        phone=current_user.phone,
        name=current_user.name,
        status=current_user.status,
        is_initialized=current_user.password_hash is not None,
    )


@router.post("/init", response_model=InitAccountResponse)
def init_account(
    data: InitAccountRequest,
    session: Session = Depends(get_session),
    current_user: UserAccount = Depends(get_current_user),
):
    """账号初始化"""
    auth_service.init_account(
        session,
        user=current_user,
        data=data,
    )
    return InitAccountResponse()


@router.post("/change-password", response_model=ChangePasswordResponse)
def change_password(
    data: ChangePasswordRequest,
    session: Session = Depends(get_session),
    current_user: UserAccount = Depends(get_current_user),
):
    """
    修改密码接口
    修改密码后，所有旧token将失效（通过token_version实现）
    """
    auth_service.change_password(
        session,
        user=current_user,
        data=data,
    )
    return ChangePasswordResponse()
