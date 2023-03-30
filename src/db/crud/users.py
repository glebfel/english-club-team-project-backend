from db.connector import get_db
from db.models import User
from exceptions import DatabaseNotFoundError


def check_user_exist_decorator(func):
    def wrapper(email: str, *args, **kwargs):
        if not get_user_by_email(email):
            raise DatabaseNotFoundError('User with email={} not found'.format(email))
        return func(email=email, *args, **kwargs)

    return wrapper


def get_user_by_email(email: str) -> User:
    with get_db() as session:
        if not (user := session.query(User).filter_by(email=email).first()):
            raise DatabaseNotFoundError('User with email={} not found'.format(email))
        return user


def get_all_users() -> list[User]:
    with get_db() as session:
        return session.query(User).filter_by(is_admin=False).all()


def add_new_user(first_name: str, last_name,
                 email: str, username: str,
                 hashed_password: str, admin=False):
    with get_db() as session:
        user = User(first_name=first_name, last_name=last_name,
                    username=username, email=email,
                    hashed_password=hashed_password, is_admin=admin)
        user.is_admin = admin
        session.add(user)
        session.commit()
        session.refresh(user)


@check_user_exist_decorator
def update_user_by_email(email: str, **kwargs):
    with get_db() as session:
        session.query(User).filter_by(email=email).update(kwargs)
        session.commit()


@check_user_exist_decorator
def remove_user_by_email(email: str):
    with get_db() as session:
        session.query(User).filter_by(email=email).delete()
        session.commit()
