from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import List

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.service_category_schemas import ServiceCategoryModel, ServiceCategoryResponse
from src.repository import service_categories as repository_service_categories
from src.services.roles import RolesAccess
# from sqlalchemy.orm import Session
# from src.services.auth import auth_service
# from sqlalchemy import select


router = APIRouter(prefix='/service_categories', tags=['service_categories'])

access_get = RolesAccess([Role.superadmin, Role.admin, Role.moderator, Role.client, Role.master])
access_create = RolesAccess([Role.superadmin, Role.admin, Role.moderator])
access_update = RolesAccess([Role.superadmin, Role.admin, Role.moderator, Role.client, Role.master])
access_delete = RolesAccess([Role.superadmin, Role.admin])
access_block = RolesAccess([Role.superadmin, Role.admin])


@router.get('/', response_model=List[ServiceCategoryResponse]) #dependencies=[Depends(access_get)]
async def get_service_categories(db: AsyncSession = Depends(get_db)): #_: User = Depends(auth_service.get_current_user)
    service_categories = await repository_service_categories.get_service_categories(db)
    if not service_categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not Found'
        )
    return service_categories


@router.get('/{service_category_id}', response_model=ServiceCategoryResponse) #dependencies=[Depends(access_get)]
async def get_service_categories_by_id(service_category_id: int, db: AsyncSession = Depends(get_db)): #_: User = Depends(auth_service.get_current_user)
    service_category = await repository_service_categories.get_service_category_by_id(service_category_id, db)
    if not service_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not Found'
        )
    return service_category


@router.get('/{service_id}', response_model=List[ServiceCategoryResponse]) #dependencies=[Depends(access_get)]
async def get_service_categories_by_service_id(service_id: int, db: AsyncSession = Depends(get_db)): #_: User = Depends(auth_service.get_current_user)
    service_categories = await repository_service_categories.get_service_category_by_service_id(service_id, db)
    if not service_categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not Found'
        )
    return service_categories


@router.post('/', response_model=ServiceCategoryResponse) #dependencies=[Depends(access_get)]
async def create_service_category(body: ServiceCategoryModel, db: AsyncSession = Depends(get_db)): #_: User = Depends(auth_service.get_current_user)
    new_service_category = await repository_service_categories.create_service_category(body, db)
    if not new_service_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not Found'
        )
    return new_service_category


@router.put('/{service_category_id}', response_model=ServiceCategoryResponse) #dependencies=[Depends(access_get)]
async def update_service_category(service_category_id: int, body: ServiceCategoryModel, db: AsyncSession = Depends(get_db)): #_: User = Depends(auth_service.get_current_user)
    updated_service_category = await repository_service_categories.update_service_category(service_category_id, body, db)
    if not updated_service_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not Found'
        )
    return updated_service_category

@router.delete('/{service_category_id}', response_model=ServiceCategoryResponse) #dependencies=[Depends(access_get)]
async def delete_service_category(service_category_id: int, db: AsyncSession = Depends(get_db)): #_: User = Depends(auth_service.get_current_user)
    deleted_service_category = await repository_service_categories.delete_service_category(service_category_id, db)
    if not deleted_service_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not Found'
        )
    return deleted_service_category
