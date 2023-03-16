from datetime import datetime

from src.db.connector import get_db
from src.db.models import Shift


def add_shift(name: str, start_date: datetime, end_date: datetime):
    with get_db() as session:
        shift = Shift(name=name, start_date=start_date, end_date=end_date)
        session.add(shift)
        session.commit()
        session.refresh(shift)


def get_shift_by_id(shift_id: int) -> Shift | None:
    with get_db() as session:
        return session.query(Shift).filter_by(id=shift_id).first()


def get_all_shifts() -> [Shift]:
    with get_db() as session:
        return session.query(Shift).all()


def remove_shift(shift_id: int):
    with get_db() as session:
        session.query(Shift).filter_by(id=shift_id).delete()
        session.commit()
