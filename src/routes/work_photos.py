from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from typing import List
from src.database.db import get_db
from src.database.models import Role
from src.schemas.work_photos import WorkPhotoModel, WorkPhotoResponse
from src.repository import work_photos
from src.services.roles import RolesAccess

router = APIRouter(prefix='/work_photos', tags=["Work_photos"])
access_get = RolesAccess([Role.superadmin, Role.admin, Role.moderator])
access_create = RolesAccess([Role.superadmin, Role.admin, Role.moderator])
access_update = RolesAccess([Role.superadmin, Role.admin, Role.moderator])
access_delete = RolesAccess([Role.superadmin, Role.admin])
access_block = RolesAccess([Role.superadmin, Role.admin])


# Create WorkPhoto
@router.post("/work-photos/", response_model=WorkPhotoResponse)
async def create_work_photo(work_photo: WorkPhotoModel, files: List[UploadFile] = File(...),
                            db: AsyncSession = Depends(get_db)):
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Cannot upload more than 10 photos")
    for file in files:
        if file.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
            raise HTTPException(status_code=400, detail="Invalid file type")
    db_work_photo = await work_photos.create_work_photo_repo(db, work_photo, files)
    return db_work_photo


@router.get("/work-photos/{work_photo_id}/", response_model=WorkPhotoResponse)
async def get_work_photo(work_photo_id: int, db: AsyncSession = Depends(get_db)):
    db_work_photo = await work_photos.get_work_photo_by_id_repo(db, work_photo_id)
    if db_work_photo is None:
        raise HTTPException(status_code=404, detail="WorkPhoto not found")
    return db_work_photo


@router.get("/work-photos/master/{master_id}/", response_model=List[WorkPhotoResponse])
async def get_work_photos_by_master_id(master_id: str, db: AsyncSession = Depends(get_db)):
    db_work_photos = await work_photos.get_work_photos_by_master_id_repo(db, master_id)
    return db_work_photos


@router.delete("/work-photos/{work_photo_id}/", response_model=dict)
async def delete_work_photo(work_photo_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await work_photos.delete_work_photo_by_id_repo(db, work_photo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="WorkPhoto not found")
    return {"message": "WorkPhoto deleted successfully"}
