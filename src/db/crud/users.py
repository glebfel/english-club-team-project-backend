from datetime import datetime

from db.connector import get_db
from db.models import User


def get_user_by_phone_number(phone_number: str) -> User:
    with get_db() as session:
        return session.query(User).filter_by(phone_number=phone_number).first()


def get_all_users() -> list[User]:
    with get_db() as session:
        return session.query(User).all()


def add_new_user(first_name: str, last_name,
                 email: str, username: str,
                 phone_number: str, birthday: datetime,
                 hashed_password: str, admin=False):
    with get_db() as session:
        user = User(first_name=first_name, last_name=last_name,
                    username=username, birthday=birthday,
                    phone_number=phone_number, email=email,
                    hashed_password=hashed_password, is_admin=admin)
        user.is_admin = admin
        session.add(user)
        session.commit()
        session.refresh(user)


def update_user_by_phone_number(phone_number: str, **kwargs):
    with get_db() as session:
        session.query(User).filter_by(phone_number=phone_number).update(kwargs)
        session.commit()


def remove_user_by_phone_number(phone_number: str):
    with get_db() as session:
        session.query(User).filter_by(phone_number=phone_number).delete()
        session.commit()
