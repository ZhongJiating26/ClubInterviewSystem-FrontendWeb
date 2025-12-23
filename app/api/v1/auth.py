from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel, Field
from fastapi import Depends

from app.api.deps import get_current_user
from app.models.user_account import UserAccount
from app.db.session import get_session
from app.repositories.user_account import UserAccountRepository
from app.core.security import create_access_token




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


@router.get("/me")
def me(current_user: UserAccount = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "phone": current_user.phone,
        "name": current_user.name,
        "status": current_user.status,
    }