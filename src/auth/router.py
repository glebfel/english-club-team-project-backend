from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Depends, APIRouter, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.auth.schemas import Token, UserRegister, UserLogin, UserInfo
from src.config import settings
from src.db.crud.users import get_user_by_email, add_new_user
from src.db.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(tags=["auth"], prefix='/auth')


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
        expire: datetime = payload.get("exp")
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserInfo(name=user.name, email=user.email,
                    is_admin=user.is_admin, access_token=Token(access_token=token, expire=expire, token_type='Bearer'))


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def authenticate_user(email: str, password: str) -> User | None:
    user = get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.AUTH_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


@router.post("/register")
def register_user(user: UserRegister) -> Token:
    db_user = get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    add_new_user(User(name=user.name, email=user.email, hashed_password=get_password_hash(user.password)))
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": db_user.email, "name": db_user.name,
              "is_admin": db_user.is_admin, "exp": datetime.utcnow() + access_token_expires},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer', expire=datetime.utcnow() + access_token_expires)


@router.post("/login")
def login_for_access_token(user: UserLogin) -> Token:
    user = authenticate_user(user.email, user.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"email": user.email, "name": user.name,
              "is_admin": user.is_admin, "exp": datetime.utcnow() + access_token_expires},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer', expire=datetime.utcnow() + access_token_expires)


@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)) -> UserInfo:
    return current_user
