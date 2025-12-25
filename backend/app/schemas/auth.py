from pydantic import BaseModel, Field
from typing import Optional


class InitAccountRequest(BaseModel):
    # bcrypt 建议 <= 72 bytes，这里先限制长度，避免你之前遇到的报错
    password: str = Field(min_length=6, max_length=72)

    # 实名信息
    name: str = Field(min_length=1, max_length=50)
    id_card_no: str = Field(min_length=15, max_length=32)

    # 学籍信息
    school_id: int
    major: str = Field(min_length=1, max_length=100)
    student_no: str = Field(min_length=1, max_length=50)

    # 可选信息
    email: Optional[str] = Field(default=None, max_length=100)
    avatar_url: Optional[str] = Field(default=None, max_length=255)


class InitAccountResponse(BaseModel):
    message: str = "账号初始化成功"


class AuthMeResponse(BaseModel):
    id: int
    phone: str
    name: str | None
    status: int
    is_initialized: bool


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=6, max_length=72)
    new_password: str = Field(min_length=6, max_length=72)


class ChangePasswordResponse(BaseModel):
    message: str = "密码修改成功，请重新登录"