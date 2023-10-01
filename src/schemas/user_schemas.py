import re
import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy.dialects.postgresql import UUID
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

    # @field_validator('password')
    # @classmethod
    # def validate_password(cls, password: str) -> str:
    #     pwd_pattern = r"((?=.*d)(?=.*[a-z])(?=.*[A-Z]).{8,})"
    #
    #     if re.match(pwd_pattern, password):
    #         return password
    #     raise ValueError("Password doesn't match requiments")
    #
    # #  (                Начало группы
    # #  (?=.*d)          Должен содержать цифру от 0 до 9
    # #  (?=.*[a-z])      Должен содержать символ латинницы в нижем регистре
    # #  (?=.*[A-Z])      Должен содержать символ латинницы в верхнем регистре
    # #  (?=.*[@#$%])     Должен содержать специальный символ из списка "@#$%"
    # #  .                Совпадает с предыдущими условиями
    # #  {8,20}           Длина - от 8 до 20 символов
    # #  )                Конец группы


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
        orm_mode = True

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
