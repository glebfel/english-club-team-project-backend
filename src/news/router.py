from fastapi import APIRouter, Depends

from auth.dependencies import get_current_user, check_user_status
from db.crud.news import get_news as get_news_db, add_news as add_news_db, get_news_by_id
from news.schemas import NewsInfo, NewsBase
from utils import convert_sqlalchemy_row_to_dict, common_error_handler_decorator

news_router = APIRouter(tags=["News"], prefix='/news')


@news_router.get("/all", dependencies=[Depends(get_current_user)])
def get_all_news() -> list[NewsInfo]:
    """Get all news"""
    return [NewsInfo(id=i.id, title=i.title, content=i.content, created_at=i.created_at) for i in get_news_db()]


@news_router.post("/add", dependencies=[Depends(check_user_status)])
def add_news(news: NewsBase):
    """Add new news (required admin rights)"""
    add_news_db(news.title, news.content)
    return {'status': 'success', 'message': 'News added'}


@news_router.get("/info/{news_id}", dependencies=[Depends(get_current_user)])
@common_error_handler_decorator
def get_news_info_by_id(news_id: int) -> NewsInfo:
    """Get news info"""
    return NewsInfo(**convert_sqlalchemy_row_to_dict(get_news_by_id(news_id)))
