from fastapi import APIRouter, Depends

from src.app.auth.models import User
from src.app.user.schemas import UserOut, UserUpdate
from src.app.user.services import user_service
from src.app.auth.permissions import get_current_active_user


user_router = APIRouter(prefix='/me', tags=['User'])


@user_router.get('', response_model=UserOut)
async def get_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@user_router.patch('/update', response_model=UserOut)
async def update_user_me(schema: UserUpdate = Depends(), current_user: User = Depends(get_current_active_user)):
    return await user_service.update(schema, pk=current_user.pk)
