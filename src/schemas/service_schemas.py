from typing import Optional

from pydantic import BaseModel, Field
from src.schemas.service_category_schemas import ServiceCategoryCreateMaster


class ServiceModel(BaseModel):
    service_ua: str = Field(min_length=2)
    service_en: str = Field(min_length=2)


class ServiceResponse(BaseModel):
    service_id: int = 1
    service_ua: str = 'Перукарські послуги'
    service_en: str = 'Hairdressing services'

    class Config:
        from_attributes = True


class ServiceCreateMaster(ServiceModel):
    service_categories: list[ServiceCategoryCreateMaster]