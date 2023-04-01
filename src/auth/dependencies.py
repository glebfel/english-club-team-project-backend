import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from db.crud.users import get_user_by_email
from config import settings
from user.schemas import UserInfo
from utils import convert_sqlalchemy_row_to_dict

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", scheme_name="JWT")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInfo:
    try:
        payload = jwt.decode(token, settings.AUTH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_email(email)
    return UserInfo(**convert_sqlalchemy_row_to_dict(user))


async def check_user_status(user: UserInfo = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Current user has no permission to do this action")
    return user