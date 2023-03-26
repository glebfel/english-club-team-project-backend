from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import NoResultFound

from db.crud.tasks import get_user_tasks_by_email, get_task_by_id, \
    get_all_active_tasks as get_all_active_tasks_db, \
    response_to_task as response_to_task_db, approve_task_response as approve_task_response_db, \
    get_all_not_approved_tasks_responses, submit_task as submit_task_db, \
    check_task as check_task_db, add_task as add_task_db
from auth.dependencies import get_current_user, check_user_status
from tasks.schemas import TaskInfo, TaskResponse, BaseTask
from user.schemas import UserInfo
from utils import convert_sqlalchemy_row_to_dict

tasks_router = APIRouter(tags=["Tasks"], prefix='/tasks')


@tasks_router.post('/add')
def add_task(task: BaseTask, current_user: UserInfo = Depends(check_user_status)):
    """Add new task (by admin)"""
    add_task_db(**task.dict(), author_id=current_user.id)
    return {'status': 'success', 'message': 'Task added'}


@tasks_router.get("/my")
def get_my_tasks(current_user: UserInfo = Depends(get_current_user)) -> list[TaskInfo]:
    """Get tasks for current user"""
    return [TaskInfo(**convert_sqlalchemy_row_to_dict(task)) for task in get_user_tasks_by_email(current_user.email)]


@tasks_router.get('/{task_id}', dependencies=[Depends(get_current_user)])
def get_task(task_id: int) -> TaskInfo:
    """Get task by id"""
    task = get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')
    return task


@tasks_router.get('/all', dependencies=[Depends(get_current_user)])
def get_all_tasks() -> list[TaskInfo]:
    """Get all active tasks"""
    return get_all_active_tasks_db()


@tasks_router.post('/response/{task_id}')
def response_to_task(task_id: int, current_user: UserInfo = Depends(get_current_user)):
    """Respond to task (by user)"""
    try:
        response_to_task_db(task_id, current_user.id)
    except NoResultFound:
        raise HTTPException(status_code=status.status.HTTP_404_NOT_FOUND, detail='Task not found')
    return {'status': 'success', 'message': 'Task completed'}


@tasks_router.put('/responses/approve/{response_id}', dependencies=[Depends(check_user_status)])
def approve_response(response_id: int):
    """Approve task response (by admin)"""
    try:
        approve_task_response_db(response_id)
    except NoResultFound:
        raise HTTPException(status_code=status.status.HTTP_404_NOT_FOUND, detail='Task not found')
    return {'status': 'success', 'message': 'Task response approved'}


@tasks_router.get("/responses", dependencies=[Depends(check_user_status)])
def get_not_approved_responses() -> list[TaskResponse]:
    """Get all not approved responses (by admin)"""
    return [TaskResponse(**convert_sqlalchemy_row_to_dict(response)) for response in
            get_all_not_approved_tasks_responses()]


@tasks_router.put('/submit/{task_id}')
def submit_task(task_id: int, current_user: UserInfo = Depends(get_current_user)):
    """Submit task (by user)"""
    try:
        submit_task_db(current_user.id, task_id)
    except NoResultFound:
        raise HTTPException(status_code=status.status.HTTP_404_NOT_FOUND, detail='Task not found')
    return {'status': 'success', 'message': 'Task submitted'}


@tasks_router.get("/responses/for_check", dependencies=[Depends(check_user_status)])
def get_not_checked_responses() -> list[TaskResponse]:
    """Get all not approved responses (by admin)"""
    return [TaskResponse(**convert_sqlalchemy_row_to_dict(response)) for response in
            get_all_not_approved_tasks_responses()]


@tasks_router.put('/check/{task_response_id}', dependencies=[Depends(get_current_user)])
def check_task(task_id: int):
    """Check task (by admin)"""
    try:
        check_task_db(task_id)
    except NoResultFound:
        raise HTTPException(status_code=status.status.HTTP_404_NOT_FOUND, detail='Task not found')
    return {'status': 'success', 'message': 'Task checked'}
