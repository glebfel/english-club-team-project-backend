from fastapi import APIRouter, Depends, HTTPException, status

from db.crud.users import get_user_by_phone_number, update_user_by_phone_number
from src.auth.dependencies import get_current_user, check_user_status
from user.schemas import UserInfo, UpdateInfo

user_router = APIRouter(tags=["Users"], prefix='/user')


@user_router.get("/info", dependencies=[Depends(check_user_status)])
def get_user_info(phone_number: str) -> UserInfo:
    """Get user info by phone number (required admin permission)"""
    if not (user := get_user_by_phone_number(phone_number)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserInfo(**user.dict())


@user_router.get("/all", dependencies=[Depends(check_user_status)])
def get_all_users_info() -> list[UserInfo]:
    """Get all users info (required admin permission)"""
    return [UserInfo(**user.dict()) for user in get_all_users_info()]


@user_router.get("/me")
def get_me_info(current_user: UserInfo = Depends(get_current_user)) -> UserInfo:
    """Get current user info"""
    return current_user


@user_router.put("/update")
def update_my_info(user_info: UpdateInfo, current_user: UserInfo = Depends(get_current_user)):
    """Update current user info"""
    updatable_fields = {}
    for i in user_info.dict():
        if user_info.dict()[i]:
            updatable_fields.update({i: user_info.dict()[i]})
    update_user_by_phone_number(current_user.phone_number, **updatable_fields)
    return {'status': 'success', 'message': 'User info updated'}
