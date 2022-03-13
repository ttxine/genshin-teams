from fastapi import APIRouter, Depends, HTTPException

from src.app.auth.models import User
from src.app.user.schemas import UserOut, UserUpdate
from src.app.user.services import user_service
from src.app.auth.permissions import get_current_active_user


user_router = APIRouter(tags=['user'])


@user_router.get('/{pk}', response_model=UserOut)
async def read_user(pk: int):
    user = await user_service.get_object_or_404(pk=pk)
    return user


@user_router.get('/me', response_model=UserOut)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@user_router.put('/me/update', response_model=UserOut)
async def update_user_me(schema: UserUpdate = Depends(), current_user: User = Depends(get_current_active_user)):
    return await user_service.update(schema, pk=current_user.pk)
