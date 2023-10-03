from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import List


from src.database.db import get_db
from src.database.models import Role
from src.schemas.subscribe_schemas import SubscribeModel, SubscribeResponse
from src.repository import subscribes
from src.services.roles import RolesAccess

router = APIRouter(prefix='/subscribe_plans', tags=["Subscribe_plans"])

access_get = RolesAccess([Role.superadmin, Role.admin, Role.moderator])
access_create = RolesAccess([Role.superadmin, Role.admin, Role.moderator])
access_update = RolesAccess([Role.superadmin, Role.admin, Role.moderator])
access_delete = RolesAccess([Role.superadmin, Role.admin])
access_block = RolesAccess([Role.superadmin, Role.admin])


@router.get('/', response_model=List[SubscribeResponse], dependencies=[Depends(access_get)])
async def get_subscribe_plans(db: AsyncSession = Depends(get_db)): #_: User = Depends(auth_service.get_current_user)
    subscribe_plans = await subscribes.get_sub_plans(db)
    if not subscribe_plans:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not Found'
        )
    return subscribe_plans


@router.get('/{plan_id}', response_model=SubscribeResponse) #dependencies=[Depends(access_get)]
async def get_subscribe_plan_by_id(plan_id: int, db: AsyncSession = Depends(get_db)): #_: User = Depends(auth_service.get_current_user)
    subscribe_plan = await subscribes.get_sub_plan_by_id(plan_id, db)
    if not subscribe_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not Found'
        )
    return subscribe_plan


@router.post('/', response_model=SubscribeResponse, status_code=status.HTTP_201_CREATED) #dependencies=[Depends(access_get)]
async def create_subscribe_plan(body: SubscribeModel, db: AsyncSession = Depends(get_db)): #_: User = Depends(auth_service.get_current_user)
    new_subscribe_plan = await subscribes.create_sub_plan(body, db)
    return new_subscribe_plan


@router.put('/{plan_id}', response_model=SubscribeResponse) #dependencies=[Depends(access_get)]
async def update_subscribe_plan(plan_id: int, body: SubscribeModel, db: AsyncSession = Depends(get_db)): #_: User = Depends(auth_service.get_current_user)
    updated_subscribe_plan = await subscribes.update_sub_plan(plan_id, body, db)
    if not updated_subscribe_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not Found'
        )
    return updated_subscribe_plan


@router.delete('/{plan_id}', response_model=SubscribeResponse) #dependencies=[Depends(access_get)]
async def delete_subscribe_plan(plan_id: int, db: AsyncSession = Depends(get_db)): #_: User = Depends(auth_service.get_current_user)
    deleted_subscribe_plan = await subscribes.delete_sub_plan(plan_id, db)
    if not deleted_subscribe_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not Found'
        )
    return deleted_subscribe_plan
