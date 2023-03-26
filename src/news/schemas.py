from datetime import datetime

from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    content: str


class NewsInfo(NewsBase):
    id: int
    created_at: datetime
