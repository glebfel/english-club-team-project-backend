from fastapi import APIRouter, Depends

from auth.dependencies import get_current_user, check_user_status
from db.crud.users import get_user_by_email, update_user_by_email, get_all_users
from user.schemas import UserInfo, UpdateUserInfo
from utils import convert_sqlalchemy_row_to_dict, common_error_handler_decorator

user_router = APIRouter(tags=["Users"], prefix='/user')


@user_router.get("/info/{email}", dependencies=[Depends(check_user_status)])
@common_error_handler_decorator
def get_user_info(email: str) -> UserInfo:
    """Get user info by email (required admin rights)"""
    return UserInfo(**convert_sqlalchemy_row_to_dict(get_user_by_email(email)))


@user_router.get("/all", dependencies=[Depends(check_user_status)])
def get_all_users_info() -> list[UserInfo]:
    """Get all users info (required admin rights)"""
    return [UserInfo(**convert_sqlalchemy_row_to_dict(user)) for user in get_all_users()]


@user_router.get("/me")
def get_me_info(current_user: UserInfo = Depends(get_current_user)) -> UserInfo:
    """Get current user info"""
    return current_user


@user_router.put("/update-me")
def update_my_info(user_info: UpdateUserInfo, current_user: UserInfo = Depends(get_current_user)):
    """Update current user info"""
    updatable_fields = {}
    for i in user_info.dict():
        if user_info.dict()[i]:
            updatable_fields.update({i: user_info.dict()[i]})
    update_user_by_email(current_user.email, **updatable_fields)
    return {'status': 'success', 'message': 'User info updated'}


@user_router.put("/update", dependencies=[Depends(check_user_status)])
@common_error_handler_decorator
def update_user(email: str, user_info: UpdateUserInfo):
    """Update user info by email (required admin rights)"""
    updatable_fields = {}
    for i in user_info.dict():
        if user_info.dict()[i]:
            updatable_fields.update({i: user_info.dict()[i]})
    update_user_by_email(email, **updatable_fields)
    return {'status': 'success', 'message': 'User info updated'}
