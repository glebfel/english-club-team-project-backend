from src.db.connector import get_db
from src.db.models import User


def get_user_by_email(email: str) -> User:
    return get_db().query(User).filter(User.email == email).first()


def add_new_user(user: User, admin=False):
    with get_db() as session:
        user.is_admin = admin
        session.add(user)
        session.commit()
        session.refresh()


def remove_user(user: User):
    with get_db() as session:
        session.query(User).filter_by(id=user.id).delete()
        session.commit()