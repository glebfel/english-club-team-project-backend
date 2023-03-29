from pydantic import BaseModel, Field, EmailStr, HttpUrl


class UserInfo(BaseModel):
    id: int
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    username: str = Field(max_length=30)
    email: EmailStr
    points: int = Field(default=0)
    media_link: HttpUrl = Field(default=None)
    is_admin: bool = Field(default=False)


class UpdateUserInfo(BaseModel):
    first_name: str = Field(max_length=30, default=None)
    last_name: str = Field(max_length=30, default=None)
    username: str = Field(max_length=30, default=None)
    media_link: HttpUrl = Field(default=None)