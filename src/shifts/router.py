from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper

from auth.dependencies import get_current_user, check_user_status
from db.crud.shifts import get_all_shifts, get_shift_by_id, \
    add_shift as add_shift_db, get_user_shifts_by_email, \
    approve_shift_reservation as approve_shift_reservation_db, reserve_shift as reserve_shift_db, \
    get_shifts_reservations
from shifts.schemas import ShiftInfo, ShiftReservation, BaseShift
from user.schemas import UserInfo
from utils import convert_sqlalchemy_row_to_dict

shifts_router = APIRouter(tags=["Shifts"], prefix='/shifts')


@shifts_router.get("/upcoming", dependencies=[Depends(get_current_user)])
def get_upcoming_shifts() -> list[ShiftInfo]:
    """Get all upcoming shifts"""
    return [ShiftInfo(**convert_sqlalchemy_row_to_dict(shift)) for shift in get_all_shifts()
            if shift.start_date > datetime.now()]


@shifts_router.get("/info/{shift_id}", dependencies=[Depends(get_current_user)])
def get_shift_info(shift_id: int) -> ShiftInfo:
    """Get shift info by id"""
    if not (shift := get_shift_by_id(shift_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shift not found")
    return ShiftInfo(**convert_sqlalchemy_row_to_dict(shift))


@shifts_router.get("/my")
def get_my_shifts(current_user: UserInfo = Depends(get_current_user)) -> list[ShiftInfo]:
    """Get shifts for current user"""
    return [ShiftInfo(**convert_sqlalchemy_row_to_dict(shift)) for shift in get_user_shifts_by_email(current_user.email)]


@shifts_router.post("/add", dependencies=[Depends(check_user_status)])
def add_shift(shift: BaseShift):
    """Add new shift (required admin rights)"""
    try:
        add_shift_db(shift.name, shift.start_date, shift.end_date)
        return {'status': 'success', 'message': 'Shift added'}
    except ValueError as e:
        arg = 'start_date' if 'Start date must be before end date' in str(e) else 'end_date'
        raise RequestValidationError([ErrorWrapper(e, ('body', arg))])


@shifts_router.post("/reserve/{shift_id}")
def reserve_shift(shift_id: int, current_user: UserInfo = Depends(get_current_user)):
    """Reserve shift """
    reserve_shift_db(shift_id=shift_id, user_id=current_user.id)
    return {'status': 'success', 'message': 'Shift added'}


@shifts_router.get("/reservations")
def show_shift_reservations() -> list[ShiftReservation]:
    """Show all shifts reservations (required admin rights)"""
    return [ShiftReservation(**convert_sqlalchemy_row_to_dict(reservation)) for reservation in get_shifts_reservations()]


@shifts_router.put("/approve/{shift_reservation_id}", dependencies=[Depends(check_user_status)])
def approve_shift_reservation(shift_reservation_id: int, ):
    """Approve shift reservation (required admin rights)"""
    approve_shift_reservation_db(shift_reservation_id=shift_reservation_id)
    return {'status': 'success', 'message': 'Shift added'}
