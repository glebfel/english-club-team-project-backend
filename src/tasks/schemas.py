from datetime import datetime

from pydantic import BaseModel


class Task(BaseModel):
    id: int
    name: str
    participants_number: int
    start_date: datetime
    end_date: datetime


class TaskResponse(BaseModel):
    id: int
    user_id: str
    task_id: int
    response_time: datetime
    is_approved: bool

