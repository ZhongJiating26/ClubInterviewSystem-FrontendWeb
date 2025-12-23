from sqlmodel import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import decode_access_token
from app.db.session import get_session
from app.models.user_account import UserAccount
from app.repositories.user_account import UserAccountRepository
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials



class AuthenticationError(Exception):
    pass

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user_by_token(
    token: str,
    session: Session,
) -> UserAccount:
    payload = decode_access_token(token)

    user_id = payload.get("user_id")
    token_version = payload.get("token_version")

    if user_id is None or token_version is None:
        raise AuthenticationError("Invalid token payload")

    repo = UserAccountRepository()
    user = repo.get_by_id(session, user_id)

    if not user:
        raise AuthenticationError("User not found")

    if user.token_version != token_version:
        raise AuthenticationError("Token has been revoked")

    if user.status != 1:
        raise AuthenticationError("User is disabled")

    return user



def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session=Depends(get_session),
):
    if credentials is None:
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
