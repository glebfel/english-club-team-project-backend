from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, HttpUrl


class UserInfo(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    points: int
    media_link: HttpUrl
    is_admin: bool
    registered_at: datetime


class UpdateUserInfo(BaseModel):
    first_name: str = Field(max_length=30, default=None)
    last_name: str = Field(max_length=30, default=None)
    username: str = Field(max_length=30, default=None)
    media_link: HttpUrl = Field(default=None)