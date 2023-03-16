from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from src.auth.schemas import Token, UserRegister
from src.config import settings
from src.db.crud.users import get_user_by_phone_number, add_new_user
from src.db.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_router = APIRouter(tags=["Authentication"], prefix='/auth')


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def authenticate_user(phone_number: str, password: str) -> User | None:
    user = get_user_by_phone_number(phone_number)
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


@auth_router.post("/register")
def register_user(user: UserRegister) -> Token:
    db_user = get_user_by_phone_number(phone_number=user.phone_number)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Phone number already registered")
    add_new_user(first_name=user.first_name, last_name=user.last_name,
                 email=user.email, username=user.username,
                 phone_number=user.phone_number, birthday=user.birthday,
                 hashed_password=get_password_hash(user.password), admin=user.is_admin)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username, "phone_number": user.phone_number, "email": user.email,
              "is_admin": user.is_admin, "exp": datetime.utcnow() + access_token_expires},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer', expire=datetime.utcnow() + access_token_expires)


@auth_router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect phone number or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username, "phone_number": user.phone_number, "email": user.email,
              "is_admin": user.is_admin, "exp": datetime.utcnow() + access_token_expires},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer', expire=datetime.utcnow() + access_token_expires)
