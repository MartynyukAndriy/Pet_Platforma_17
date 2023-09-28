from pydantic import BaseModel, Field


class ServiceModel(BaseModel):
    service_ua: str = Field(min_length=2)
    service_en: str = Field(min_length=2)


class ServiceResponse(BaseModel):
    service_id: int = 1
    service_ua: str = 'Перукарські послуги'
    service_en: str = 'Hairdressing services'

    class Config:
        orm_mode = True
