from fastapi import APIRouter, Depends, HTTPException, status

from db.crud.users import get_user_by_phone_number, update_user_by_phone_number
from src.auth.dependencies import get_current_user, check_user_status
from user.schemas import UserInfo, UpdateInfo

router = APIRouter(tags=["Users info"], prefix='/user')


@router.get("/info", dependencies=[Depends(check_user_status)])
def get_user_info(phone_number: str) -> UserInfo:
    """
    Get user info by phone number (required admin permission)
    :param phone_number: user phone number
    :return: user info
    """
    if not (user := get_user_by_phone_number(phone_number)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserInfo(**user.dict())


@router.get("/me")
def get_me_info(current_user: UserInfo = Depends(get_current_user)) -> UserInfo:
    """Get current user info"""
    return current_user


@router.post("/update", dependencies=[Depends(get_current_user)])
def update_my_info(user_info: UpdateInfo):
    """Update current user info"""
    updatable_fields = {}
    for i in user_info.dict():
        if user_info.dict()[i]:
            updatable_fields.update({i: user_info.dict()[i]})
    update_user_by_phone_number(**updatable_fields)
