from datetime import datetime

from db.crud.users import get_user_by_phone_number
from src.db.connector import get_db
from src.db.models import Shift, UserShift, ShiftReservation


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


def get_user_shifts_by_phone_number(phone_number: str) -> list[Shift]:
    with get_db() as session:
        # get user id
        user = get_user_by_phone_number(phone_number)
        # extract all shifts ids
        shifts_ids = [_.shift_id for _ in session.query(UserShift).filter_by(user_id=user.id).all()]
        # extract info about each shift
        shifts = session.query(Shift).filter(Shift.id.in_(shifts_ids)).all()
        return shifts


def reserve_shift(shift_id: int, user_id: int):
    with get_db() as session:
        reservation = ShiftReservation(shift_id=shift_id, user_id=user_id)
        session.add(reservation)
        session.commit()
        session.refresh(reservation)


def approve_shift_reservation(shift_reservation_id: int):
    with get_db() as session:
        # update approve status
        session.query(ShiftReservation).filter_by(id=shift_reservation_id).update({'is_approved': True})
        # update shift participant count
        shift_id = session.query(ShiftReservation).filter_by(id=shift_reservation_id).first().shift_id
        session.query(Shift).filter_by(id=shift_id).update({'participant_count': Shift.participant_count + 1})
        session.commit()


def get_shifts_reservations() -> list[ShiftReservation]:
    with get_db() as session:
        # update shift participant count
        shifts_reservations = session.query(ShiftReservation).all()
        return shifts_reservations


def remove_shift(shift_id: int):
    with get_db() as session:
        session.query(Shift).filter_by(id=shift_id).delete()
        session.commit()
