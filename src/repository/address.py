from typing import Type

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.database.models import Country, City
from src.schemas.address_schemas import CountryModel, CityModel


async def get_country(country_id: int, db: Session) -> Type[Country] | None:
    country = select(Country).filter_by(country_id=country_id)
    return country


async def create_country(body: CountryModel, db: Session) -> Country:
    country = Country(country_ukr=body.country_ukr, country_eng=body.country_eng)
    db.add(country)
    await db.commit()
    await db.refresh(country)
    return country


async def update_country(country_id: int, body: CountryModel, db: Session, user) -> Country | None:
    if user.user_role in ("superadmin", "admin", "moderator"):
        country = select(Country).filter(Country.country_id == country_id).first()
        country.country_ukr = body.country_ukr
        country.country_eng = body.country_eng
        await db.commit()
    return country


async def remove_country(country_id: int, db: Session, user) -> Country | None:
    if user.role in ("admin", "superadmin"):
        country = select(Country).filter(Country.country_id == country_id).first()
        db.delete(country)
        await db.commit()
    return country


async def get_city(city_id: int, db: Session) -> Type[City] | None:
    return select(City).filter(City.city_id == city_id).first()


async def create_city(body: CityModel, db: Session) -> City:
    city = City(city_ukr=body.city_ukr, city_eng=body.city_eng, country_id=body.country_id)
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city


async def update_city(city_id: int, body: CityModel, db: Session, user) -> City | None:
    if user.user_role in ("superadmin", "admin", "moderator"):
        city = select(City).filter(City.city_id == city_id).first()
        city.city_ukr = body.city_ukr
        city.city_eng = body.city_eng
        await db.commit()
    return city


async def remove_city(city_id: int, db: Session, user) -> City | None:
    if user.role in ("admin", "superadmin"):
        city = db.execute(select(City)).filter(City.city_id == city_id).first()
        db.delete(city)
        await db.commit()
    return city
