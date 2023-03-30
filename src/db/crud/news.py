from db.connector import get_db
from db.models import News
from exceptions import DatabaseElementNotFoundError


def add_news(title: str, content: str):
    with get_db() as session:
        news = News(title=title, content=content)
        session.add(news)
        session.commit()
        session.refresh(news)


def get_news_by_id(news_id: int) -> News | None:
    with get_db() as session:
        if not (news := session.query(News).filter_by(id=news_id).first()):
            raise DatabaseElementNotFoundError('News with id={} not found'.format(news_id))
        return news


def get_news() -> list[News]:
    with get_db() as session:
        return session.query(News).all()


def remove_news(news_id: int):
    # check if news with given id in db
    if not get_news_by_id(news_id):
        raise DatabaseElementNotFoundError('News with id={} not found'.format(news_id))
    # remove
    with get_db() as session:
        session.query(News).filter_by(id=news_id).delete()
        session.commit()
