from src.database.models import Service
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.schemas.service_schemas import ServiceModel


async def get_services(db: AsyncSession):
    sq = select(Service)
    sq_res = await db.execute(sq)
    return sq_res.scalars().all()


async def get_service_by_id(service_id: int, db: AsyncSession):
    sq = select(Service).filter_by(service_id=service_id)
    sq_res = await db.execute(sq)
    return sq_res.scalar_one_or_none()


async def create_service(body: ServiceModel, db: AsyncSession):
    new_service = Service(**body.model_dump())
    db.add(new_service)
    await db.commit()
    await db.refresh(new_service)
    return new_service


async def update_service(service_id: int, body: ServiceModel, db: AsyncSession):
    sq = select(Service).filter_by(service_id=service_id)
    sq_res = await db.execute(sq)
    service = sq_res.scalar_one_or_none()
    if service:
        service.service_ua = body.service_ua
        service.service_en = body.service_en
        await db.commit()
        await db.refresh(service)
    return service


async def delete_service(service_id: int, db: AsyncSession):
    sq = select(Service).filter_by(service_id=service_id)
    sq_res = await db.execute(sq)
    deleted_service = sq_res.scalar_one_or_none()
    if deleted_service:
        await db.delete(deleted_service)
        await db.commit()
    return deleted_service
