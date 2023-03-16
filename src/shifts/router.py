from fastapi import APIRouter, Depends

from src.auth.dependencies import get_current_user
from src.news.dependencies import check_user_status
from src.shifts.schemas import Shift

router = APIRouter(tags=["shifts"], prefix='/shifts')


@router.get("/upcoming", dependencies=[Depends(get_current_user)])
def get_upcoming_shifts() -> list[Shift]:
    return []


@router.get("/info", dependencies=[Depends(get_current_user)])
def get_shift_info() -> list[Shift]:
    return []


@router.post("/add", dependencies=[Depends(check_user_status)])
def add_shift(shift: Shift):
    pass
