from fastapi import APIRouter, Depends, HTTPException, status

from db.crud.users import get_user_by_email, update_user_by_email
from auth.dependencies import get_current_user, check_user_status
from user.schemas import UserInfo, UpdateInfo

user_router = APIRouter(tags=["Users"], prefix='/user')


@user_router.get("/info/{email}", dependencies=[Depends(check_user_status)])
def get_user_info(email: str) -> UserInfo:
    """Get user info by email (required admin rights)"""
    if not (user := get_user_by_email(email)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserInfo(**user.dict())


@user_router.get("/all", dependencies=[Depends(check_user_status)])
def get_all_users_info() -> list[UserInfo]:
    """Get all users info (required admin rights)"""
    return [UserInfo(**user.dict()) for user in get_all_users_info()]


@user_router.get("/me")
def get_me_info(current_user: UserInfo = Depends(get_current_user)) -> UserInfo:
    """Get current user info"""
    return current_user


@user_router.put("/update-me")
def update_my_info(user_info: UpdateInfo, current_user: UserInfo = Depends(get_current_user)):
    """Update current user info"""
    updatable_fields = {}
    for i in user_info.dict():
        if user_info.dict()[i]:
            updatable_fields.update({i: user_info.dict()[i]})
    update_user_by_email(current_user.email, **updatable_fields)
    return {'status': 'success', 'message': 'User info updated'}


@user_router.put("/update", dependencies=[Depends(check_user_status)])
def update_user(email: str, user_info: UpdateInfo):
    """Update user info by email (required admin rights)"""
    updatable_fields = {}
    for i in user_info.dict():
        if user_info.dict()[i]:
            updatable_fields.update({i: user_info.dict()[i]})
    update_user_by_email(email, **updatable_fields)
    return {'status': 'success', 'message': 'User info updated'}
