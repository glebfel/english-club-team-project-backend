from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


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
