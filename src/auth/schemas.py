from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    expire: datetime


class UserRegister(BaseModel):
    name: str = Field(max_length=30)
    email: EmailStr
    password: str
    is_admin: bool = Field(default=False)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserInfo(BaseModel):
    name: str = Field(max_length=30)
    email: EmailStr
    is_admin: bool = Field(default=False)
    access_token: Token
