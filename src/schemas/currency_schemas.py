from pydantic import BaseModel, Field


class CurrencyModel(BaseModel):
    currency: str = Field(min_length=2)


class CurrencyGetResponse(BaseModel):
    currency_id: int = 1
    currency: str = 'ua'

    class Config:
        orm_mode = True



