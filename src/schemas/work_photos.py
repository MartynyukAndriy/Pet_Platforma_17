import uuid

from pydantic import BaseModel, Field


class WorkPhotoModel(BaseModel):
    master_id: uuid.UUID = Field(default_factory=lambda: uuid.uuid4().hex)
    work_photo_url: str


class WorkPhotoResponse(BaseModel):
    work_photo_id: int
    master_id: uuid.UUID = Field(default_factory=lambda: uuid.uuid4().hex)
    work_photo_url: str

    class Config:
        from_attributes = True
