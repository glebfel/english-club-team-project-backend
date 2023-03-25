from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, HttpUrl


class UserInfo(BaseModel):
    id: int
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    username: str = Field(max_length=30)
    email: EmailStr
    experience: int = Field(default=None)
    rank: str = Field(default=None)
    hobby: str = Field(default=None)
    media_link: HttpUrl = Field(default=None)
    is_admin: bool = Field(default=False)


class UpdateInfo(BaseModel):
    first_name: str = Field(max_length=30, default=None)
    last_name: str = Field(max_length=30, default=None)
    username: str = Field(max_length=30, default=None)
    experience: int = Field(default=None)
    rank: str = Field(default=None)
    hobby: str = Field(default=None)
    media_link: HttpUrl = Field(default=None)