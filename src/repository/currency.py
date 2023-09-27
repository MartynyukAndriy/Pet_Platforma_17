from src.database.models import Currency
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.schemas.currency_schemas import CurrencyModel


async def get_currencies(db: AsyncSession):
    sq = select(Currency)
    currencies = await db.execute(sq)
    res_currencies = currencies.scalars().all()
    return res_currencies


async def get_currency_by_id(currency_id: int, db):
    sq = select(Currency).filter_by(currency_id=currency_id)
    currency = await db.execute(sq)
    return currency.scalars().first()


async def create_currency(body: CurrencyModel, db: AsyncSession):
    new_currency = Currency(**body.dict())
    db.add(new_currency)
    await db.commit()
    await db.refresh(new_currency)
    return new_currency


async def update_currency(currency_id: int, body: CurrencyModel, db: AsyncSession):
    sq = select(Currency).filter_by(currency_id=currency_id)
    sq_res = await db.execute(sq)
    updated_currency = sq_res.scalar_one_or_none()
    if updated_currency:
        updated_currency.currency = body.currency
        await db.commit()
        await db.refresh(updated_currency)
    return updated_currency


async def delete_currency(currency_id: int, db: AsyncSession):
    sq = select(Currency).filter_by(currency_id=currency_id)
    sq_res = await db.execute(sq)
    deleted_currency = sq_res.scalar_one_or_none()
    if deleted_currency:
        await db.delete(deleted_currency)
        await db.commit()
    return deleted_currency

