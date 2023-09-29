import json
from typing import Type, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from starlette import status

from src.database.models import Country, City
from src.schemas.address_schemas import CountryModel, CityModel, CityResponse
from src.services.auth import auth_service


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
    if user.user_role in ("admin", "superadmin"):
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
    if user.user_role in ("admin", "superadmin"):
        city = db.execute(select(City)).filter(City.city_id == city_id).first()
        db.delete(city)
        await db.commit()
    return city


# async def add_cities_to_ukraine(json_file_path: str, db: Session, user) -> Optional[CityResponse]:
#     if user.user_role in ("admin", "superadmin"):
#         try:
#             with open(json_file_path, "r", encoding="utf-8") as json_file:
#                 data = json.load(json_file)
#
#             # Знайдемо країну "Ukraine" у базі даних
#             ukraine = await db.execute(Country.__table__.select().where(Country.country_ukr == "Ukraine"))
#             ukraine = await ukraine.scalar()
#
#             if ukraine:
#                 # Перевіримо наявність міст та їх додавання
#                 for city_id, city_data in data.items():
#                     city_ukr = city_data.get("ua")
#                     city_eng = city_data.get("en")
#
#                     # Перевіримо, чи існує місто з такою назвою у базі даних
#                     existing_city = await db.execute(
#                         City.__table__.select().where(City.city_ukr == city_ukr)
#                     )
#                     existing_city = await existing_city.scalar()
#
#                     if not existing_city:
#                         city = City(city_ukr=city_ukr, city_eng=city_eng, country_id=ukraine.country_id)
#                         db.add(city)
#
#                 await db.commit()
#                 return CityResponse(city_id=city.city_id, city_ukr=city.city_ukr, city_eng=city.city_eng)
#             else:
#                 raise Exception("Країна 'Ukraine' не знайдена в базі даних.")
#
#         except Exception as e:
#             await db.rollback()
#             raise e
