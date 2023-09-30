from typing import Type

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.models import Country, City
from src.schemas.address_schemas import CountryModel, CityModel


async def get_country(country_id: int, db: AsyncSession, user) -> Type[Country] | None:
    sq = select(Country).filter(Country.country_id == country_id)
    country = await db.execute(sq)
    return country.scalar_one_or_none()


async def create_country(body: CountryModel, db: AsyncSession) -> Country:
    # if user.user_role in ("superadmin", "admin", "moderator"):
    country = Country(country_ukr=body.country_ukr, country_eng=body.country_eng)
    db.add(country)
    await db.commit()
    await db.refresh(country)
    return country


async def update_country(country_id: int, body: CountryModel, db: AsyncSession, user) -> Country | None:
    # if user.user_role in ("superadmin", "admin", "moderator"):
    sq = select(Country).filter_by(country_id=country_id)
    result = await db.execute(sq)
    country = result.scalar_one_or_none()
    if country:
        country.country_ukr = body.country_ukr
        country.country_eng = body.country_eng
        await db.commit()
        await db.refresh(country)
    return country


async def remove_country(country_id: int, db: AsyncSession, user) -> Country | None:
    # if user.user_role in ("admin", "superadmin"):
    sq = select(Country).filter(Country.country_id == country_id)
    result = await db.execute(sq)
    country = result.scalar_one_or_none()
    if country:
        await db.delete(country)
        await db.commit()
    return country


async def get_city(city_id: int, db: AsyncSession, user) -> Type[City] | None:
    sq = select(City).filter(City.city_id == city_id)
    city = await db.execute(sq)
    return city.scalar_one_or_none()


async def create_city(body: CityModel, db: AsyncSession) -> City:
    # if user.user_role in ("superadmin", "admin", "moderator"):
    city = City(city_ukr=body.city_ukr, city_eng=body.city_eng, country_id=body.country_id)
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city


async def update_city(city_id: int, body: CityModel, db: AsyncSession, user) -> City | None:
    # if user.user_role in ("superadmin", "admin", "moderator"):
    sq = select(City).filter(City.city_id == city_id)
    result = await db.execute(sq)
    city = result.scalar_one_or_none()
    if city:
        city.city_ukr = body.city_ukr
        city.city_eng = body.city_eng
        await db.commit()
        await db.refresh(city)
    return city


async def remove_city(city_id: int, db: AsyncSession, user) -> City | None:
    # if user.user_role in ("admin", "superadmin"):
    sq = select(City).filter(City.city_id == city_id)
    result = await db.execute(sq)
    city = result.scalar_one_or_none()
    if city:
        await db.delete(city)
        await db.commit()
    return city
