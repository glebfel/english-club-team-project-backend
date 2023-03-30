from fastapi import APIRouter, Depends

from auth.dependencies import get_current_user, check_user_status
from db.crud.tasks import get_user_tasks_by_email, get_task_by_id, \
    get_all_active_tasks as get_all_active_tasks_db, \
    response_to_task as response_to_task_db, approve_task_response as approve_task_response_db, \
    get_all_not_approved_tasks_responses, submit_task as submit_task_db, \
    check_task as check_task_db, add_task as add_task_db, get_all_tasks as get_all_tasks_db
from tasks.schemas import TaskInfo, TaskResponse, BaseTask
from user.schemas import UserInfo
from utils import convert_sqlalchemy_row_to_dict, common_error_handler_decorator

tasks_router = APIRouter(tags=["Tasks"], prefix='/tasks')


@tasks_router.get("/my")
def get_my_tasks(current_user: UserInfo = Depends(get_current_user)) -> list[TaskInfo]:
    """Get tasks for current user"""
    return [TaskInfo(**convert_sqlalchemy_row_to_dict(task)) for task in get_user_tasks_by_email(current_user.email)]


@tasks_router.get('/all', dependencies=[Depends(check_user_status)])
def get_all_tasks() -> list[TaskInfo]:
    """Get all tasks (by admin)"""
    return [TaskInfo(**convert_sqlalchemy_row_to_dict(task)) for task in get_all_tasks_db()]


@tasks_router.get('/active', dependencies=[Depends(get_current_user)])
def get_all_active_tasks() -> list[TaskInfo]:
    """Get all active tasks"""
    return [TaskInfo(**convert_sqlalchemy_row_to_dict(task)) for task in get_all_active_tasks_db()]


@tasks_router.get("/responses", dependencies=[Depends(check_user_status)])
def get_not_approved_responses() -> list[TaskResponse]:
    """Get all not approved responses (by admin)"""
    return [TaskResponse(**convert_sqlalchemy_row_to_dict(response)) for response in
            get_all_not_approved_tasks_responses()]


@tasks_router.get('/{task_id}', dependencies=[Depends(get_current_user)])
@common_error_handler_decorator
def get_task(task_id: int) -> TaskInfo:
    """Get task by id"""
    return TaskInfo(**convert_sqlalchemy_row_to_dict(get_task_by_id(task_id)))


@tasks_router.get("/responses/for_check", dependencies=[Depends(check_user_status)])
def get_not_checked_responses() -> list[TaskResponse]:
    """Get all not approved responses (by admin)"""
    return [TaskResponse(**convert_sqlalchemy_row_to_dict(response)) for response in
            get_all_not_approved_tasks_responses()]


@tasks_router.post('/add')
@common_error_handler_decorator
def add_task(task: BaseTask, current_user: UserInfo = Depends(check_user_status)):
    """Add new task (by admin)"""
    add_task_db(**task.dict(), author_id=current_user.id)
    return {'status': 'success', 'message': 'Task added'}


@tasks_router.post('/response/{task_id}')
@common_error_handler_decorator
def response_to_task(task_id: int, current_user: UserInfo = Depends(get_current_user)):
    """Respond to task (by user)"""
    response_to_task_db(task_id, current_user.id)
    return {'status': 'success', 'message': 'Task response sent'}


@tasks_router.put('/responses/approve/{task_response_id}', dependencies=[Depends(check_user_status)])
@common_error_handler_decorator
def approve_response(task_response_id: int):
    """Approve user task response (by admin)"""
    approve_task_response_db(task_response_id)
    return {'status': 'success', 'message': 'Task response approved'}


@tasks_router.put('/submit/{task_id}')
@common_error_handler_decorator
def submit_task(task_id: int, current_user: UserInfo = Depends(get_current_user)):
    """Submit task (by user)"""
    submit_task_db(current_user.id, task_id)
    return {'status': 'success', 'message': 'Task submitted'}

@tasks_router.put('/check/{task_response_id}', dependencies=[Depends(get_current_user)])
@common_error_handler_decorator
def check_task(task_response_id: int):
    """Check task (by admin)"""
    check_task_db(task_response_id)
    return {'status': 'success', 'message': 'Task checked'}
