from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel, Field

from app.db.session import get_session
from app.repositories.user_account import UserAccountRepository


router = APIRouter(prefix="/auth", tags=["Auth"])
user_repo = UserAccountRepository()


class RegisterRequest(BaseModel):
    phone: str = Field(..., min_length=6, max_length=20)
    password: str = Field(..., min_length=6, max_length=50)
    name: str | None = None
    school_id: int | None = None


class RegisterResponse(BaseModel):
    id: int
    phone: str
    name: str | None


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
