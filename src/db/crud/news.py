from src.db.connector import get_db
from src.db.models import News


def add_new_news(title: str, content: str):
    with get_db() as session:
        news = News(title=title, content=content)
        session.add(news)
        session.commit()
        session.refresh(news)


def get_news(news_id: int) -> News | None:
    with get_db() as session:
        return session.query(News).filter_by(id=news_id).first()


def remove_news(news_id: int):
    with get_db() as session:
        session.query(News).filter_by(id=news_id).delete()
        session.commit()
