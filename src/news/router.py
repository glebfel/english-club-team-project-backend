from fastapi import APIRouter, Depends

from src.auth.dependencies import get_current_user, check_user_status
from src.db.crud.news import get_news as get_news_db, add_news as add_news_db
from src.news.schemas import NewsList, NewsItem

news_router = APIRouter(tags=["News"], prefix='/news')


@news_router.get("/all", dependencies=[Depends(get_current_user)])
def get_all_news() -> NewsList:
    """Get all news"""
    return NewsList(news=[NewsItem(title=i.title, content=i.content) for i in get_news_db()])


@news_router.post("/add", dependencies=[Depends(check_user_status)])
def add_news(news: NewsItem):
    """Add new news (required admin permission)"""
    add_news_db(news.title, news.content)
