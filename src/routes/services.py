from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import List
from sqlalchemy import select

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.service_schemas import ServiceModel, ServiceResponse
from src.repository import services as repository_services
from src.services.auth import auth_service
from src.services.roles import RolesAccess

router = APIRouter(prefix='/services', tags=["services"])

access_get = RolesAccess([Role.superadmin, Role.admin, Role.moderator, Role.client, Role.master])
access_create = RolesAccess([Role.superadmin, Role.admin, Role.moderator])
access_update = RolesAccess([Role.superadmin, Role.admin, Role.moderator, Role.client, Role.master])
access_delete = RolesAccess([Role.superadmin, Role.admin])
access_block = RolesAccess([Role.superadmin, Role.admin])


@router.get('/', response_model=List[ServiceResponse]) #dependencies=[Depends(access_get)]
async def get_services(db:AsyncSession = Depends(get_db)): #_: User = Depends(auth_service.get_current_user)
    services = await repository_services.get_services(db)
    if not services:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not Found'
        )
    return services


@router.get('/{service_id}', response_model=ServiceResponse) #dependencies=[Depends(access_get)]
async def get_service_by_id(service_id: int, db: AsyncSession = Depends(get_db)): #_: User = Depends(auth_service.get_current_user)
    service = await repository_services.get_service_by_id(service_id, db)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not Found'
        )
    return service


@router.post('/', response_model=ServiceResponse, status_code=status.HTTP_201_CREATED) #dependencies=[Depends(access_get)]
async def create_service(body: ServiceModel, db: AsyncSession = Depends(get_db)): #_: User = Depends(auth_service.get_current_user)
    new_service = await repository_services.create_service(body, db)
    return new_service


@router.put('/{service_id}', response_model=ServiceResponse) #dependencies=[Depends(access_get)]
async def update_service(service_id: int, body: ServiceModel, db: AsyncSession = Depends(get_db)): #_: User = Depends(auth_service.get_current_user)
    updated_service = await repository_services.update_service(service_id, body, db)
    if not updated_service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not Found'
        )
    return updated_service


@router.delete('/{service_id}', response_model=ServiceResponse) #dependencies=[Depends(access_get)]
async def delete_service(service_id: int, db: AsyncSession = Depends(get_db)): #_: User = Depends(auth_service.get_current_user)
    deleted_service = await repository_services.delete_service(service_id, db)
    if not deleted_service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not Found'
        )
    return deleted_service
