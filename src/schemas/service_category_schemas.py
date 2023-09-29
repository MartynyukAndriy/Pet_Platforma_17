from pydantic import BaseModel, Field


class ServiceCategoryModel(BaseModel):
    service_id: int = Field(ge=1)
    service_category_ua: str = Field(min_length=2)
    service_category_en: str = Field(min_length=2)


class ServiceCategoryResponse(BaseModel):
    service_category_id: int = 1
    service_id: int = 1
    service_category_ua: str = 'Стрижка чоловіча'
    service_category_en: str = "Men's haircut"

    class Config:
        from_attributes = True
