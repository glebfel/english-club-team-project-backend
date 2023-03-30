from datetime import datetime

import pytz

from db.crud.users import get_user_by_email, check_user_exist_decorator
from db.connector import get_db
from db.models import Shift, UserShift, ShiftReservation
from exceptions import DatabaseNotFoundError


def check_shift_exist_decorator(func):
    def wrapper(shift_id: int, *args, **kwargs):
        if not get_shift_by_id(shift_id):
            raise DatabaseNotFoundError('shift with id={} not found'.format(shift_id))
        return func(shift_id=shift_id, *args, **kwargs)

    return wrapper


def get_shift_by_id(shift_id: int) -> Shift | None:
    with get_db() as session:
        if not (shift := session.query(Shift).filter(Shift.id == shift_id).first()):
            raise DatabaseNotFoundError('Shift with id={} not found'.format(shift_id))
        return shift


def add_shift(name: str, start_date: datetime, end_date: datetime):
    # validate datetime
    if start_date > end_date:
        raise ValueError('Start date must be before end date')
    if datetime.now(pytz.utc) > end_date:
        raise ValueError('End date must be in the future')
    with get_db() as session:
        shift = Shift(name=name, start_date=start_date, end_date=end_date)
        session.add(shift)
        session.commit()
        session.refresh(shift)


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


@check_shift_exist_decorator
def reserve_shift(shift_id: int, user_id: int):
    with get_db() as session:
        reservation = ShiftReservation(shift_id=shift_id, user_id=user_id)
        session.add(reservation)
        session.commit()
        session.refresh(reservation)


def get_shift_reservation_by_id(shift_reservation_id: int) -> ShiftReservation | None:
    with get_db() as session:
        if not (shifts_reservations := session.query(ShiftReservation).filter(
                ShiftReservation.id == shift_reservation_id).first()):
            raise DatabaseNotFoundError('Shift reservation with id={} not found'.format(shift_reservation_id))
        return shifts_reservations


def check_shift_reservation_exist_decorator(func):
    def wrapper(shift_reservation_id: int, *args, **kwargs):
        if not get_shift_reservation_by_id(shift_reservation_id):
            raise DatabaseNotFoundError('Shift reservation with id={} not found'.format(shift_reservation_id))
        return func(shift_reservation_id=shift_reservation_id, *args, **kwargs)

    return wrapper


@check_shift_reservation_exist_decorator
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


@check_shift_exist_decorator
def remove_shift(shift_id: int):
    with get_db() as session:
        session.query(Shift).filter_by(id=shift_id).delete()
        session.commit()
