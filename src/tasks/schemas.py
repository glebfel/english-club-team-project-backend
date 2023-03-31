from datetime import datetime

from pydantic import BaseModel, Field


class BaseTask(BaseModel):
    title: str
    description: str
    points: int
    start_date: datetime = Field(default_factory=datetime.now)
    end_date: datetime


class TaskInfo(BaseTask):
    id: int
    author_email: str
    is_active: bool


class TaskAnswer(BaseModel):
    answer: str


class TaskResponse(BaseModel):
    id: int
    answer: str = Field(default=None)
    user_email: str
    task_id: int
    response_time: datetime
    is_approved: bool
    is_completed: bool
    is_checked: bool
