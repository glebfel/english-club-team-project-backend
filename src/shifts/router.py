from datetime import datetime

import pytz
from fastapi import APIRouter, Depends

from auth.dependencies import get_current_user, check_user_status
from db.crud.shifts import get_all_shifts, get_shift_by_id, \
    add_shift as add_shift_db, get_user_shifts_by_email, \
    approve_shift_reservation as approve_shift_reservation_db, reserve_shift as reserve_shift_db, \
    get_shifts_reservations
from shifts.schemas import ShiftInfo, ShiftReservation, BaseShift
from user.schemas import UserInfo
from utils import convert_sqlalchemy_row_to_dict, common_error_handler_decorator

shifts_router = APIRouter(tags=["Shifts"], prefix='/shifts')


@shifts_router.get("/upcoming", dependencies=[Depends(get_current_user)])
def get_upcoming_shifts() -> list[ShiftInfo]:
    """Get all upcoming shifts"""
    return [ShiftInfo(**convert_sqlalchemy_row_to_dict(shift)) for shift in get_all_shifts()
            if shift.start_date > datetime.now(pytz.utc)]


@shifts_router.get("/info/{shift_id}", dependencies=[Depends(get_current_user)])
@common_error_handler_decorator
def get_shift_info(shift_id: int) -> ShiftInfo:
    """Get shift info by id"""
    return ShiftInfo(**convert_sqlalchemy_row_to_dict(get_shift_by_id(shift_id)))


@shifts_router.get("/my")
def get_my_shifts(current_user: UserInfo = Depends(get_current_user)) -> list[ShiftInfo]:
    """Get shifts for current user"""
    return [ShiftInfo(**convert_sqlalchemy_row_to_dict(shift)) for shift in
            get_user_shifts_by_email(current_user.email)]


@shifts_router.get("/reservations")
def show_shift_reservations() -> list[ShiftReservation]:
    """Show all shifts reservations (required admin rights)"""
    return [ShiftReservation(**convert_sqlalchemy_row_to_dict(reservation)) for reservation in
            get_shifts_reservations()]


@shifts_router.post("/add", dependencies=[Depends(check_user_status)])
@common_error_handler_decorator
def add_shift(shift: BaseShift):
    """Add new shift (required admin rights)"""
    add_shift_db(shift.name, shift.start_date, shift.end_date)
    return {'status': 'success', 'message': 'Shift added'}


@shifts_router.post("/reserve/{shift_id}")
@common_error_handler_decorator
def reserve_shift(shift_id: int, current_user: UserInfo = Depends(get_current_user)):
    """Reserve shift """
    reserve_shift_db(shift_id=shift_id, user_id=current_user.id)
    return {'status': 'success', 'message': 'Shift reservation sent for approval'}


@shifts_router.put("/approve/{shift_reservation_id}", dependencies=[Depends(check_user_status)])
@common_error_handler_decorator
def approve_shift_reservation(shift_reservation_id: int, ):
    """Approve shift reservation (required admin rights)"""
    approve_shift_reservation_db(shift_reservation_id=shift_reservation_id)
    return {'status': 'success', 'message': 'Shift reservation approved'}
