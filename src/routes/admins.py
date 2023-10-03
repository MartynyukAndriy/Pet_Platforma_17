from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.db import get_db
from src.database.models import Admin, Role, User
from src.repository.admins import create_admin_from_client, get_all_clients, get_all_masters, \
    create_client_from_admin, get_all_admins
from src.schemas.user_schemas import AdminModel, UserModel, AdminResponse, UserRes
from src.services.roles import RolesAccess

access_get = RolesAccess([Role.superadmin, Role.admin, Role.client])
access_create = RolesAccess([Role.superadmin, Role.admin, Role.client])
access_update = RolesAccess([Role.superadmin, Role.admin, Role.client])
access_delete = RolesAccess([Role.superadmin, Role.admin, Role.client])
access_block = RolesAccess([Role.superadmin, Role.admin, Role.client])

router = APIRouter(prefix="/admins", tags=["Admin"])


@router.post("/to_admin", response_model=AdminResponse, dependencies=[Depends(access_create)])
async def create_admin_from_client_route(user_id: int, db: AsyncSession = Depends(get_db)):
    to_admin = await create_admin_from_client(user_id, db)
    return to_admin


@router.post("/to_client", response_model=UserRes, dependencies=[Depends(access_get)])
async def create_client_from_admin_route(admin_id: int, db: AsyncSession = Depends(get_db)):
    to_client = await create_client_from_admin(admin_id, db)
    return to_client


@router.get("/clients/", response_model=list[UserModel], dependencies=[Depends(access_get)])
async def get_all_clients_route(db: AsyncSession = Depends(get_db)):
    clients = await get_all_clients(db)
    if len(clients) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clients not found")
    else:
        return clients


@router.get("/masters/", response_model=list[UserModel], dependencies=[Depends(access_get)])
async def get_all_masters_route(db: AsyncSession = Depends(get_db)):
    masters = await get_all_masters(db)
    if len(masters) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Masters not found")
    else:
        return masters


@router.get("/admins/", response_model=list[UserModel], dependencies=[Depends(access_get)])
async def get_all_admins_route(db: AsyncSession = Depends(get_db)):
    admins = await get_all_admins(db)
    if len(admins) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admins not found")
    else:
        return admins