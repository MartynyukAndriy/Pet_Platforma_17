from typing import Optional

from pydantic import BaseModel, Field


class CityModel(BaseModel):
    country_id: int
    city_ukr: str
    city_eng: str


class CityResponse(BaseModel):
    city_id: int
    country_id: int
    city_ukr: str
    city_eng: str

    class Config:
        from_attributes = True


class CountryModel(BaseModel):
    country_ukr: str
    country_eng: str


class CountryResponse(BaseModel):
    country_id: int
    country_ukr: str
    country_eng: str


    class Config:
        from_attributes = True


