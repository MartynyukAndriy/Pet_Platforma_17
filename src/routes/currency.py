from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import List
from sqlalchemy import select

from src.database.db import get_db
from src.database.models import User, Role, Currency
from src.schemas.currency_schemas import CurrencyModel, CurrencyGetResponse
from src.repository import currency as repository_currency
from src.services.auth import auth_service
from src.services.roles import RolesAccess

router = APIRouter(prefix='/currency', tags=["currency"])

access_get = RolesAccess([Role.superadmin, Role.admin, Role.moderator, Role.client, Role.master])
access_create = RolesAccess([Role.superadmin, Role.admin, Role.moderator])
access_update = RolesAccess([Role.superadmin, Role.admin, Role.moderator, Role.client, Role.master])
access_delete = RolesAccess([Role.superadmin, Role.admin])
access_block = RolesAccess([Role.superadmin, Role.admin])


@router.get("/currencies", response_model=List[CurrencyGetResponse]) #dependencies=[Depends(access_get)]
async def get_currencies(db: AsyncSession = Depends(get_db)): #_: User = Depends(auth_service.get_current_user)
    currencies = await repository_currency.get_currencies(db)
    if not currencies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")
    return currencies


@router.get("/{currency_id}", response_model=CurrencyGetResponse) #dependencies=[Depends(access_get)]
async def get_currencies(currency_id: int, db: AsyncSession = Depends(get_db)): #_: User = Depends(auth_service.get_current_user)
    currency = await repository_currency.get_currency_by_id(currency_id, db)
    if not currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")
    return currency


@router.post('/', response_model=CurrencyGetResponse, status_code=status.HTTP_201_CREATED) #dependencies=[Depends(access_create)]
async def create_currency(body: CurrencyModel, db: AsyncSession = Depends(get_db)):
    new_currency = await repository_currency.create_currency(body, db)
    if not new_currency:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")
    return new_currency


@router.put('/{currency_id}', response_model=CurrencyGetResponse)
async def update_currency(currency_id: int, body: CurrencyModel, db: AsyncSession = Depends(get_db)):
    updated_currency = await repository_currency.update_currency(currency_id, body, db)
    if not updated_currency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found"
        )
    return updated_currency


@router.delete('/{currency_id}', response_model=CurrencyGetResponse)
async def delete_currency(currency_id: int, db: AsyncSession = Depends(get_db)):
    deleted_currency = await repository_currency.delete_currency(currency_id, db)
    if not deleted_currency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Not Found'
        )
    return deleted_currency
