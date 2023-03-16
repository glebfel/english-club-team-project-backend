from fastapi import Depends, HTTPException, status

from src.auth.dependencies import get_current_user
from src.auth.schemas import UserInfo


async def check_user_status(user: UserInfo = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Current user has no permission to do this action")
