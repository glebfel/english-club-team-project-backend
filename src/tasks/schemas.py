from datetime import datetime

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int
    title: str
    description: str
    author_id: int
    points: int
    participants_number: int = Field(default=0)
    start_date: datetime
    end_date: datetime
    is_active: bool


class TaskIn(Task):
    title: str
    description: str
    points: int
    start_date: datetime = Field(default_factory=datetime.now)
    end_date: datetime
    is_active: bool = Field(default=True)


class TaskResponse(BaseModel):
    id: int
    answer: str
    user_id: str
    task_id: int
    response_time: datetime
    is_approved: bool
    is_completed: bool
    is_checked: bool
