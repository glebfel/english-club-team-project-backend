from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Depends, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from auth.schemas import Token, UserRegister
from config import settings
from db.crud.users import get_user_by_email, add_new_user
from db.models import User
from user.schemas import UserInfo
from utils import convert_sqlalchemy_row_to_dict

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_router = APIRouter(tags=["Authentication"], prefix='/auth')


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
    encoded_jwt = jwt.encode(to_encode, settings.AUTH_SECRET_KEY, algorithm='HS256')
    return encoded_jwt


@auth_router.post("/register")
def register_user(user: UserRegister) -> Token:
    # check if user already in db
    db_user = get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already registered")
    add_new_user(first_name=user.first_name, last_name=user.last_name,
                 email=user.email, username=user.username,
                 hashed_password=get_password_hash(user.password), admin=user.is_admin)

    # return new user form db (to get id)
    user = UserInfo(**convert_sqlalchemy_row_to_dict(get_user_by_email(email=user.email)))

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username, "email": user.email, "exp": datetime.utcnow() + access_token_expires},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer',
                 expire=datetime.utcnow() + access_token_expires,
                 user_info=user)


@auth_router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    user = UserInfo(**convert_sqlalchemy_row_to_dict(authenticate_user(form_data.username, form_data.password)))
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user.username, "email": user.email, "exp": datetime.utcnow() + access_token_expires},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer',
                 expire=datetime.utcnow() + access_token_expires,
                 user_info=user)
