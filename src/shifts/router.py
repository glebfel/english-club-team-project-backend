from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.dependencies import get_current_user, check_user_status
from src.db.crud.shifts import get_all_shifts, get_shift_by_id, \
    add_shift as add_shift_db, get_user_shifts_by_phone_number, \
    approve_shift_reservation as approve_shift_reservation_db, reserve_shift as reserve_shift_db
from src.shifts.schemas import Shift
from user.schemas import UserInfo

shifts_router = APIRouter(tags=["Shifts"], prefix='/shifts')


@shifts_router.get("/upcoming", dependencies=[Depends(get_current_user)])
def get_upcoming_shifts() -> list[Shift]:
    """Get all upcoming shifts"""
    return [shift for shift in get_all_shifts() if shift.start_date > datetime.now()]


@shifts_router.get("/info", dependencies=[Depends(get_current_user)])
def get_shift_info(shift_id: int) -> Shift | None:
    """Get shift info by id"""
    if not (shift := get_shift_by_id(shift_id)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shift not found")
    return Shift(**shift.dict())


@shifts_router.get("/my")
def get_my_shifts(current_user: UserInfo = Depends(get_current_user)) -> list[Shift]:
    """Get shifts for current user"""
    return [Shift(**shift.dict()) for shift in get_user_shifts_by_phone_number(current_user.phone_number)]


@shifts_router.post("/add", dependencies=[Depends(check_user_status)])
def add_shift(shift: Shift):
    """Add new shift (required admin permission)"""
    add_shift_db(shift.name, shift.start_date, shift.end_date)
    return {'status': 'success', 'message': 'Shift added'}


@shifts_router.post("/reserve")
def reserve_shift(shift_id: int, current_user: UserInfo = Depends(get_current_user)):
    """Reserve shift """
    reserve_shift_db(shift_id=shift_id, user_id=current_user.id)
    return {'status': 'success', 'message': 'Shift added'}


@shifts_router.post("/approve", dependencies=[Depends(check_user_status)])
def approve_shift_reservation(shift_reservation_id: int, ):
    """Approve shift reservation (required admin permission)"""
    approve_shift_reservation_db(shift_reservation_id=shift_reservation_id)
    return {'status': 'success', 'message': 'Shift added'}
