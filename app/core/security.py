from datetime import datetime, timedelta
from typing import Any, Dict

from jose import jwt

from app.core.config import settings


def create_access_token(
    *,
    subject: Dict[str, Any],
    expires_minutes: int | None = None,
) -> str:
    if expires_minutes is None:
        expires_minutes = settings.jwt_expire_minutes

    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)

    payload = subject.copy()
    payload.update({"exp": expire})

    encoded_jwt = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return encoded_jwt
