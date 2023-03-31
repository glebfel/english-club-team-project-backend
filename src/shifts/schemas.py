from datetime import datetime

from pydantic import BaseModel


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
    shift_id: int
    user_id: int
    is_approved: bool
