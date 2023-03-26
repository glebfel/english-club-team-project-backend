from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

from user.schemas import UserInfo


class Token(BaseModel):
    access_token: str
    token_type: str
    expire: datetime
    user_info: UserInfo


class UserRegister(BaseModel):
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    username: str = Field(max_length=30)
    email: EmailStr
    password: str
    is_admin: bool = Field(default=False)


class UserLogin(BaseModel):
    email: str
    password: str
