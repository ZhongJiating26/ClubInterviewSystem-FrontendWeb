from typing import Optional
from datetime import datetime
from sqlmodel import Field
from app.models.base import BaseModel


class VerificationCode(BaseModel, table=True):
    """
    验证码表：存储手机验证码
    """
    __tablename__ = "verification_code"

    phone: str = Field(max_length=20, nullable=False, index=True, description="手机号")
    code: str = Field(max_length=10, nullable=False, description="验证码")
    code_type: str = Field(max_length=20, nullable=False, description="验证码类型（register, login, reset_password等）")
    expires_at: datetime = Field(nullable=False, description="过期时间")
    is_used: int = Field(default=0, nullable=False, description="是否已使用：1已使用 0未使用")
    used_at: Optional[datetime] = Field(default=None, description="使用时间")

