from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.address_schemas import CountryResponse, CountryModel
from src.repository import address as address_repository
from src.services.auth import auth_service
from src.services.roles import RolesAccess

access_get = RolesAccess([Role.superadmin, Role.admin, Role.moderator, Role.client, Role.master])
# access_create = RolesAccess([Role.superadmin, Role.admin, Role.moderator, Role.client, Role.master])
access_update = RolesAccess([Role.superadmin, Role.admin, Role.moderator, Role.client, Role.master])
access_delete = RolesAccess([Role.superadmin, Role.admin])
access_block = RolesAccess([Role.superadmin, Role.admin])

router = APIRouter(prefix="/countries", tags=["Address"])


@router.get("/{country_id}", response_model=CountryResponse, dependencies=[Depends(access_get)])
async def read_country(country_id: int, db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    country = await address_repository.get_country(country_id, db)
    if country is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")
    return country


@router.post("/", response_model=CountryResponse)
async def create_country(body: CountryModel, db: Session = Depends(get_db)):
    country = await address_repository.create_country(body, db)
    if country is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This country is not exists in the database or you don't have enough roots to update")
    return country


@router.put("/{country_id}", response_model=CountryResponse, dependencies=[Depends(access_update)])
async def update_country(body: CountryModel, country_id: int, db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    country = await address_repository.update_country(country_id, body, db, User)
    if country is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Country not found or you don't have enough roots to update")
    return country


@router.delete("/{country_id}", response_model=CountryResponse, dependencies=[Depends(access_delete)])
async def remove_country(country_id: int, db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    country = await address_repository.remove_country(country_id, db, User)
    if country is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Country not found or you don't have enough rules to delete")
    return country
