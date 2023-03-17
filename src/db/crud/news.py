from db.connector import get_db
from db.models import News


def add_news(title: str, content: str):
    with get_db() as session:
        news = News(title=title, content=content)
        session.add(news)
        session.commit()
        session.refresh(news)


def get_news_by_id(news_id: int) -> News | None:
    with get_db() as session:
        return session.query(News).filter_by(id=news_id).first()


def get_news() -> list[News]:
    with get_db() as session:
        return session.query(News).all()


def remove_news(news_id: int):
    with get_db() as session:
        session.query(News).filter_by(id=news_id).delete()
        session.commit()
