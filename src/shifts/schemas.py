from datetime import datetime

from pydantic import BaseModel

from user.schemas import UserInfo


class BaseShift(BaseModel):
    name: str
    number: str
    description: str
    start_date: datetime
    end_date: datetime


class ShiftInfo(BaseShift):
    id: int
    participants_number: int


class ShiftReservation(BaseModel):
    id: int
    user_info: UserInfo
    shift_info: ShiftInfo
    is_approved: bool
