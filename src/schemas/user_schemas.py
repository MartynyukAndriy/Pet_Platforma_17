import re
from datetime import date
import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from uuid import uuid4
from src.database.models import Role
from typing_extensions import Annotated


class UserModel(BaseModel):
    user_role: Role = 'client'
    password: str = Field(min_length=8)
    name: str = Field(min_length=5, max_length=30)
    email: EmailStr
    country_id: int = Field(1, gt=0)
    city_id: int = Field(1, gt=0)
    phone: str
    avatar: Optional[str] = Field(None)
    birthday: date


class UserRes(BaseModel):
    user_id: uuid.UUID = Field(default_factory=lambda: uuid4().hex)
    user_role: Role = 'client'
    password: str
    name: str
    email: str
    country_id: int
    city_id: int
    phone: str
    avatar: Optional[str] = Field(None)
    birthday: date

    class Config:
        from_attributes = True


class MasterModel(BaseModel):
    user_role: Role = 'master'
    password: str = Field(min_length=8)
    name: str = Field(min_length=5, max_length=30)
    email: EmailStr
    country_id: int = Field(1, gt=0)
    city_id: int = Field(1, gt=0)
    phone: str
    avatar: Optional[str] = Field(None)
    description: Optional[str]
    salon_name: Optional[str]
    salon_address: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]



class MasterResponse(BaseModel):
    master_id: uuid.UUID = Field(default_factory=lambda: uuid4().hex)
    user_id: uuid.UUID = Field(default_factory=lambda: uuid4().hex)
    description: Optional[str]
    salon_name: Optional[str]
    salon_address: Optional[str]
    longitude: Optional[float]
    latitude: Optional[float]
    is_active: bool

    class Config:
        from_attributes = True


class AdminModel(UserModel):
    user_id: uuid.UUID = Field(default_factory=lambda: uuid4().hex)
    user_role: Role = 'admin'
    is_active: bool = True


class AdminResponse(UserRes):
    admin_id: uuid.UUID = Field(default_factory=lambda: uuid4().hex)
    user_role: Role = 'admin'
    is_active: bool

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: str
    email: EmailStr


class UserBlackList(BaseModel):
    banned: Optional[bool] = False

    class Config:
        from_attributes = True


class UserBlacklistResponse(BaseModel):
    user_id: uuid.UUID = Field(default_factory=lambda: uuid4().hex)
    name: str = "Oksana"
    email: EmailStr = "oksana@gmail.com"
    role: Role = "client"
    banned: Optional[bool] = False

    class Config:
        from_attributes = True
