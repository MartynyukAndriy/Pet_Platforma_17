from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.address_schemas import CityResponse, CityModel
from src.repository import address as address_repository
from src.services.auth import auth_service
from src.services.roles import RolesAccess

access_get = RolesAccess([Role.superadmin, Role.admin, Role.moderator, Role.client, Role.master])
access_create = RolesAccess([Role.superadmin, Role.admin, Role.moderator, Role.client, Role.master])
access_update = RolesAccess([Role.superadmin, Role.admin, Role.moderator, Role.client, Role.master])
access_delete = RolesAccess([Role.superadmin, Role.admin])
access_block = RolesAccess([Role.superadmin, Role.admin])

router = APIRouter(prefix="/cities", tags=["Address"])


@router.get("/{city_id}", response_model=CityResponse, dependencies=[Depends(access_get)])
async def read_city(city_id: int, db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    city = await address_repository.get_city(city_id, db)
    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="City not found")
    return city


@router.post("/", response_model=CityResponse)
async def create_city(body: CityModel, db: Session = Depends(get_db)):
    city = await address_repository.create_city(body, db)
    if city is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="This city is not exists in the database or you don't have enough roots to update")
    return city


@router.put("/{city_id}", response_model=CityResponse, dependencies=[Depends(access_update)])
async def update_city(body: CityModel, city_id: int, db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    city = await address_repository.update_city(city_id, body, db, User)
    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="City not found or you don't have enough roots to update")
    return city


@router.delete("/{city_id}", response_model=CityResponse, dependencies=[Depends(access_delete)])
async def remove_city(city_id: int, db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    city = await address_repository.remove_city(city_id, db, User)
    if city is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="City not found or you don't have enough rules to delete")
    return city