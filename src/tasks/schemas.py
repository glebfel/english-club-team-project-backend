from datetime import datetime

from pydantic import BaseModel, Field


class BaseTask(BaseModel):
    title: str
    description: str
    points: int
    start_date: datetime = Field(default_factory=datetime.now)
    end_date: datetime
    is_active: bool = Field(default=True)


class TaskInfo(BaseTask):
    id: int
    author_id: int


class TaskResponse(BaseModel):
    id: int
    answer: str
    user_id: str
    task_id: int
    response_time: datetime
    is_approved: bool
    is_completed: bool
    is_checked: bool
