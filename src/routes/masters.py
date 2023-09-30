import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.background import BackgroundTasks

from src.conf.messages import AuthMessages
from src.database.db import get_db
from src.database.models import Role, User
from src.repository import users as repository_users
from src.repository import masters as repository_masters
from src.schemas.user_schemas import MasterResponse, MasterModel
from src.services.auth import auth_service
from src.services.email import send_email
from src.services.roles import RolesAccess

access_get = RolesAccess([Role.superadmin, Role.admin, Role.moderator, Role.client, Role.master])
access_create = RolesAccess([Role.superadmin, Role.admin, Role.moderator, Role.client, Role.master])
access_update = RolesAccess([Role.superadmin, Role.admin, Role.moderator, Role.client, Role.master])
access_delete = RolesAccess([Role.superadmin, Role.admin])
access_block = RolesAccess([Role.superadmin, Role.admin])

router = APIRouter(prefix="/masters", tags=["Masters profile"])


@router.get("/{user_id}/", response_model=MasterResponse)
async def master_profile_info(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):

    master_info = await repository_masters.get_master_info(user_id, db)
    if master_info is None:
        raise HTTPException(status_code=404, detail="Master not found")
    return master_info

#
# @router.get("/me/", response_model=MasterResponse)
# async def read_masters_me(current_user: User = Depends(auth_service.get_current_user)):
#
#     return current_user
