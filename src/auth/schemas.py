from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, HttpUrl

from shifts.schemas import Shift


class Token(BaseModel):
    access_token: str
    token_type: str
    expire: datetime


class UserRegister(BaseModel):
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    username: str = Field(max_length=30)
    birthday: datetime
    phone_number: str
    email: EmailStr
    password: str
    is_admin: bool = Field(default=False)


class UserLogin(BaseModel):
    phone_number: str
    password: str


class UserInfo(BaseModel):
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    username: str = Field(max_length=30)
    birthday: datetime
    phone_number: str
    email: EmailStr
    first_shift: Shift = Field(default=None)
    experience: int = Field(default=None)
    rank: str = Field(default=None)
    hobby: str = Field(max_length=30)
    media_link: HttpUrl = Field(default=None)
    is_admin: bool = Field(default=False)
    access_token: Token
