from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.api.deps import get_current_user
from app.models.user_account import UserAccount
from app.db.session import get_session
from app.repositories.user_account import UserAccountRepository
from app.core.security import create_access_token
from app.schemas.auth import InitAccountRequest, InitAccountResponse, AuthMeResponse


class RegisterRequest(BaseModel):
    phone: str = Field(..., min_length=6, max_length=20)
    password: str = Field(..., min_length=6, max_length=50)
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
user_repo = UserAccountRepository()


@router.post("/register", response_model=RegisterResponse)
def register(
    data: RegisterRequest,
    session: Session = Depends(get_session),
):
    # 1️⃣ 检查手机号是否已注册
    existing = user_repo.get_by_phone(session, data.phone)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="手机号已注册",
        )

    # 2️⃣ 创建用户
    user = user_repo.create_user(
        session,
        phone=data.phone,
        password=data.password,
        name=data.name,
        school_id=data.school_id,
    )

    # 3️⃣ 返回结果
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
    # 1️⃣ 查用户
    user = user_repo.get_by_phone(session, data.phone)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="手机号或密码错误",
        )

    # 2️⃣ 校验状态
    if user.status != 1:
        raise HTTPException(
            status_code=403,
            detail="用户已被禁用",
        )

    # ⭐ 2.5️⃣ 账号是否初始化（新增，关键）
    if user.password_hash is None:
        raise HTTPException(
            status_code=403,
            detail="账号尚未初始化，请先完善账号信息",
        )

    # 3️⃣ 校验密码
    if not user_repo.verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=400,
            detail="手机号或密码错误",
        )

    # 4️⃣ 签发 JWT（带 token_version）
    token_payload = {
        "user_id": user.id,
        "token_version": user.token_version,
    }

    access_token = create_access_token(subject=token_payload)
    return LoginResponse(access_token=access_token)


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
    # 1) 禁用用户不能操作
    if current_user.status != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用",
        )

    # 2) 已初始化不能重复初始化
    if current_user.password_hash is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="账号已初始化，无需重复初始化",
        )

    # 3) 执行初始化（写入密码 + 资料）
    user_repo.init_account(
        session,
        user=current_user,
        password=data.password,
        name=data.name,
        id_card_no=data.id_card_no,
        school_id=data.school_id,
        major=data.major,
        student_no=data.student_no,
        email=data.email,
        avatar_url=data.avatar_url,
    )

    return InitAccountResponse()
