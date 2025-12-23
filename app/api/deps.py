from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session

from app.core.security import decode_access_token
from app.db.session import get_session
from app.models.user_account import UserAccount
from app.repositories.user_account import UserAccountRepository


class AuthenticationError(Exception):
    """用于 token 校验过程中的内部异常"""
    pass


bearer_scheme = HTTPBearer(auto_error=False)
user_repo = UserAccountRepository()



def get_current_user_by_token(
    token: str,
    session: Session,
) -> UserAccount:
    payload = decode_access_token(token)

    user_id = payload.get("user_id")
    token_version = payload.get("token_version")

    if user_id is None or token_version is None:
        raise AuthenticationError("Invalid token payload")

    user = user_repo.get_by_id(session, user_id)
    if not user:
        raise AuthenticationError("User not found")

    if user.is_deleted == 1:
        raise AuthenticationError("User deleted")

    if user.status != 1:
        raise AuthenticationError("User is disabled")

    if user.token_version != token_version:
        raise AuthenticationError("Token has been revoked")

    return user



def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    session: Session = Depends(get_session),
) -> UserAccount:
    if credentials is None or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = credentials.credentials

    try:
        return get_current_user_by_token(token, session)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
