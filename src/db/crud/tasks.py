from datetime import datetime

from db.crud.users import get_user_by_phone_number
from src.db.connector import get_db
from src.db.models import Task, TaskResponse, UserTask


def add_task(title: str, description: str, requirements: str, score: int, start_date: datetime, end_date: datetime):
    with get_db() as session:
        task = Task(title=title, description=description, requirements=requirements,
                    score=score, start_date=start_date, end_date=end_date)
        session.add(task)
        session.commit()
        session.refresh(task)


def get_task_by_id(task_id: int) -> Task | None:
    with get_db() as session:
        return session.query(Task).filter_by(id=task_id).first()


def get_all_active_tasks() -> list[Task]:
    with get_db() as session:
        return session.query(Task).filter_by(is_active=True).all()


def get_user_tasks_by_phone_number(phone_number: str) -> list[Task]:
    with get_db() as session:
        # get user id
        user = get_user_by_phone_number(phone_number)
        # extract all shifts ids
        tasks_ids = [_.shift_id for _ in session.query(UserTask).filter_by(user_id=user.id).all()]
        # extract info about each shift
        tasks = session.query(Task).filter(Task.id.in_(tasks_ids)).all()
        return tasks


def response_to_task(task_id: int, user_id: int):
    with get_db() as session:
        response = TaskResponse(task_id=task_id, user_id=user_id)
        session.add(response)
        session.commit()
        session.refresh(response)


def get_all_not_approved_tasks_responses() -> list[TaskResponse]:
    with get_db() as session:
        return session.query(TaskResponse).filter_by(is_approved=False).all()


def approve_task_response(task_response_id: int):
    with get_db() as session:
        # update approve status
        session.query(TaskResponse).filter_by(id=task_response_id).update({'is_approved': True})
        session.commit()


def submit_task(task_id: int):
    with get_db() as session:
        # update completed status
        session.query(UserTask).filter_by(id=task_id).update({'is_completed': True})
        session.commit()


def check_task(task_id: int):
    with get_db() as session:
        # update checked status
        session.query(UserTask).filter_by(id=task_id).update({'is_checked': True})
        # TODO: update user scores


def remove_task(task_id: int):
    with get_db() as session:
        session.query(Task).filter_by(id=task_id).delete()
        session.commit()
