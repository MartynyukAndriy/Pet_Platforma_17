import uuid

from pydantic import BaseModel, Field


class MasterToServiceModel(BaseModel):
    service_category_id: int = Field(ge=0, default=1)
    service_sale_price: float = Field(ge=0, default=100.00)
    discount: float = Field(ge=0)


class MasterToServiceResponse(BaseModel):
    id: int
    service_sale_price: float = Field(ge=0, default=100.00)
    discount: float = Field(ge=0)

    class Config:
        from_attributes = True
