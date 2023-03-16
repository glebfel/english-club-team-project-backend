from fastapi import APIRouter, Depends

from src.auth.router import get_current_user
from src.db.crud.news import get_news
from src.news.schemas import NewsList, NewsItem

router = APIRouter(tags=["news"], prefix='/news')


@router.get("/all", dependencies=[Depends(get_current_user)])
def get_all_news() -> NewsList:
    return get_news()


@router.post("/add", dependencies=[Depends(get_current_user)])
def add_news(news: NewsItem):
    add_news(news.title, news.content)
