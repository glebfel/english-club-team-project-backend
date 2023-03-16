from datetime import datetime

from pydantic import BaseModel


class Shift(BaseModel):
    id: int
    name: str
    participants_number: int
    start_date: datetime
    end_date: datetime


class ShiftReservation(BaseModel):
    id: int
    shift_id: int
    user_id: int
    is_approved: bool
