from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.db.session import get_session
from app.core.security import decode_access_token
from app.repositories.user_account import UserAccountRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

user_repo = UserAccountRepository()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
):
    # 1️⃣ 解码 JWT
    payload = decode_access_token(token)

    user_id = payload.get("user_id")
    token_version = payload.get("token_version")

    if user_id is None or token_version is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的登录凭证",
        )

    # 2️⃣ 查用户（未删除）
    user = user_repo.get_by_id(session, user_id)
    if not user or user.is_deleted == 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或已被删除",
        )

    # 3️⃣ 校验 token_version（关键）
    if user.token_version != token_version:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="登录已失效，请重新登录",
        )

    return user
