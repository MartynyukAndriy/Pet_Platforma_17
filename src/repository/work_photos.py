import os
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import WorkPhoto
from src.schemas.work_photos import WorkPhotoModel
from fastapi import HTTPException, UploadFile


# Create WorkPhoto
async def create_work_photo_repo(db: AsyncSession, work_photo: WorkPhotoModel, files: List[UploadFile]):
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Cannot upload more than 10 photos")
    for file in files:
        if file.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
            raise HTTPException(status_code=400, detail="Invalid file type")
        # Save the file
        with open(os.path.join("uploads", file.filename), "wb") as buffer:
            buffer.write(await file.read())
    db_work_photo = WorkPhoto(**work_photo.dict())
    db.add(db_work_photo)
    await db.commit()
    await db.refresh(db_work_photo)
    return db_work_photo


# Get WorkPhoto by ID
async def get_work_photo_by_id_repo(db: AsyncSession, work_photo_id: int):
    return db.query(WorkPhoto).filter(WorkPhoto.work_photo_id == work_photo_id).first()


# Get WorkPhotos by Master ID
async def get_work_photos_by_master_id_repo(db: AsyncSession, master_id: str):
    return db.query(WorkPhoto).filter(WorkPhoto.master_id == master_id).all()


# Delete WorkPhoto by ID
async def delete_work_photo_by_id_repo(db: AsyncSession, work_photo_id: int):
    db_work_photo = await db.query(WorkPhoto).filter(WorkPhoto.work_photo_id == work_photo_id).first()
    if db_work_photo:
        await db.delete(db_work_photo)
        await db.commit()
        return True
    return False