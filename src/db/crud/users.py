from src.db.connector import get_db
from src.db.models import User


def get_user_by_email(email: str) -> User:
    with get_db() as session:
        return session.query(User).filter_by(email=email).first()


def add_new_user(name, email, password, admin=False):
    with get_db() as session:
        user = User(name=name, email=email, hashed_password=User.get_password_hash(password), is_admin=admin)
        user.is_admin = admin
        session.add(user)
        session.commit()
        session.refresh(user)


def remove_user(user: User):
    with get_db() as session:
        session.query(User).filter_by(id=user.id).delete()
        session.commit()