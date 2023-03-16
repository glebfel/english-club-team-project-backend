from datetime import datetime

from db.crud.users import get_user_by_email
from src.db.connector import get_db
from src.db.models import Shift, UserShift


def add_shift(name: str, start_date: datetime, end_date: datetime):
    with get_db() as session:
        shift = Shift(name=name, start_date=start_date, end_date=end_date)
        session.add(shift)
        session.commit()
        session.refresh(shift)


def get_shift_by_id(shift_id: int) -> Shift | None:
    with get_db() as session:
        return session.query(Shift).filter_by(id=shift_id).first()


def get_all_shifts() -> list[Shift]:
    with get_db() as session:
        return session.query(Shift).all()


def get_user_shifts_by_email(email: str) -> list[Shift]:
    with get_db() as session:
        # get user id
        user = get_user_by_email(email)
        # extract all shifts ids
        shifts_ids = [_.shift_id for _ in session.query(UserShift).filter_by(user_id=user.id).all()]
        # extract info about each shift
        shifts = session.query(Shift).filter(Shift.id.in_(shifts_ids)).all()
        return shifts


def remove_shift(shift_id: int):
    with get_db() as session:
        session.query(Shift).filter_by(id=shift_id).delete()
        session.commit()
