from datetime import datetime

import pytz as pytz
from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound

from db.crud.users import get_user_by_email, check_user_exist_decorator
from db.connector import get_db
from db.models import Task, TaskResponse, User
from exceptions import DatabaseElementNotFoundError


def check_task_exist_decorator(func):
    def wrapper(task_id: int, *args, **kwargs):
        if not get_task_by_id(task_id):
            raise DatabaseElementNotFoundError('Task with id={} not found'.format(task_id))
        return func(task_id, *args, **kwargs)

    return wrapper


def check_task_response_exist_decorator(func):
    def wrapper(task_response_id: int, *args, **kwargs):
        if not get_task_response_by_id(task_response_id):
            raise DatabaseElementNotFoundError('Task with id={} not found'.format(task_response_id))
        return func(task_response_id, *args, **kwargs)

    return wrapper


def add_task(start_date: datetime, end_date: datetime, **kwargs):
    # validate datetime and check if task already start
    if start_date > end_date:
        raise ValueError('Start date must be before end date')
    if datetime.now(pytz.utc) > end_date:
        raise ValueError('End date must be in the future')
    is_active = True if start_date < datetime.now(pytz.utc) < end_date else False
    with get_db() as session:
        task = Task(start_date=start_date, end_date=end_date, is_active=is_active, **kwargs)
        session.add(task)
        session.commit()
        session.refresh(task)


def get_task_by_id(task_id: int) -> Task | None:
    with get_db() as session:
        if not (task := session.query(Task).filter_by(id=task_id).first()):
            raise DatabaseElementNotFoundError('Task with id={} not found'.format(task_id))
        return task


def get_all_tasks() -> list[Task]:
    with get_db() as session:
        return session.query(Task).all()


def get_all_active_tasks() -> list[Task]:
    # get all tasks and check if they are active
    with get_db() as session:
        for task in get_all_tasks():
            if task.start_date < datetime.now(pytz.utc) < task.end_date:
                session.query(Task).filter_by(id=task.id).update({'is_active': True})
            else:
                session.query(Task).filter_by(id=task.id).update({'is_active': False})
        session.commit()
        return session.query(Task).filter_by(is_active=True).all()


@check_user_exist_decorator
def get_user_tasks_by_email(email: str) -> list[Task]:
    with get_db() as session:
        # get user id
        user = session.query(User).filter_by(email=email).first()
        return user.tasks


@check_task_exist_decorator
def response_to_task(task_id: int, user_id: int):
    with get_db() as session:
        user = session.query(User).filter_by(id=user_id).first()
        task = session.query(Task).filter_by(id=task_id).first()
        user.tasks.append(task)
        session.commit()


def get_task_response_by_id(task_response_id: int) -> TaskResponse | None:
    with get_db() as session:
        if not (task_response := session.query(TaskResponse).filter_by(id=task_response_id).first()):
            raise DatabaseElementNotFoundError('Task response with id={} not found'.format(task_response_id))
        return task_response


def get_all_not_approved_tasks_responses() -> list[TaskResponse]:
    with get_db() as session:
        return session.query(TaskResponse).filter_by(is_approved=False).all()


def get_all_not_checked_tasks_responses() -> list[TaskResponse]:
    with get_db() as session:
        return session.query(TaskResponse).filter(
            (TaskResponse.is_approved == True) & (TaskResponse.is_completed == True) &
            (TaskResponse.is_checked == False)).all()


@check_task_response_exist_decorator
def approve_task_response(task_response_id: int):
    try:
        with get_db() as session:
            # update approve status
            session.query(TaskResponse).filter_by(id=task_response_id).update({'is_approved': True})
            session.commit()
    except NoResultFound:
        raise DatabaseElementNotFoundError('Task response with id={} not found'.format(task_response_id))


def submit_task(user_id: int, task_id: int, task_answer: str):
    try:
        with get_db() as session:
            # update completed status
            session.query(TaskResponse).filter(
                and_(TaskResponse.task_id == task_id, TaskResponse.user_id == user_id)).update({'is_completed': True,
                                                                                                'answer': task_answer})
            session.commit()
    except NoResultFound:
        raise DatabaseElementNotFoundError(
            'Task response to task with id={0} and user with id={1} not found'.format(task_id, user_id))


@check_task_response_exist_decorator
def check_task(task_response_id: int):
    try:
        with get_db() as session:
            # update checked status
            task_response_query = session.query(TaskResponse).filter_by(id=task_response_id)
            task_response_query.update({'is_checked': True})
            # update user scores
            task_response = task_response_query.first()
            task = session.query(Task).filter_by(id=task_response.task_id).first()
            session.query(User).filter_by(id=task_response.user_id).update({'points': User.points + task.points})
            session.commit()
    except NoResultFound:
        raise DatabaseElementNotFoundError(
            'Task response with id={} not found'.format(task_response_id))


@check_task_exist_decorator
def remove_task(task_id: int):
    with get_db() as session:
        session.query(Task).filter_by(id=task_id).delete()
        session.commit()
