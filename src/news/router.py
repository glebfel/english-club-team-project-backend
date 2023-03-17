from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.dependencies import get_current_user, check_user_status
from src.db.crud.news import get_news as get_news_db, add_news as add_news_db, get_news_by_id
from src.news.schemas import NewsItem

news_router = APIRouter(tags=["News"], prefix='/news')


@news_router.get("/all", dependencies=[Depends(get_current_user)])
def get_all_news() -> list[NewsItem]:
    """Get all news"""
    return [NewsItem(id=i.id, title=i.title, content=i.content, created_at=i.created_at) for i in get_news_db()]


@news_router.post("/add", dependencies=[Depends(check_user_status)])
def add_news(news: NewsItem):
    """Add new news (required admin rights)"""
    add_news_db(news.title, news.content)
    return {'status': 'success', 'message': 'News added'}


@news_router.get("/info", dependencies=[Depends(get_current_user)])
def get_news_info_by_id(news_id: int) -> NewsItem:
    """Get news info"""
    if not (news := get_news_by_id(news_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="News not found")
    return NewsItem(**news.dict())
