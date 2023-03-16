from datetime import datetime

import jwt
from fastapi import Depends, HTTPException, status

from src.auth.dependencies import oauth2_scheme
from src.auth.schemas import UserInfo, Token
from src.config import settings
from src.db.crud.users import get_user_by_email


async def check_user_status(token: str = Depends(oauth2_scheme)) -> UserInfo:
    try:
        payload = jwt.decode(token, settings.AUTH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        expire: datetime = payload.get("exp")
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Current user has no permission to do this action")
    return UserInfo(name=user.name, email=user.email,
                    is_admin=user.is_admin, access_token=Token(access_token=token, expire=expire, token_type='Bearer'))
