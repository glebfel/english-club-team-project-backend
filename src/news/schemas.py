from datetime import datetime

from pydantic import BaseModel, Field


class NewsItem(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class NewsList(BaseModel):
    news: list[NewsItem] = Field(default_factory=list)
