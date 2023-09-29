from src.database.models import ServiceCategories, Service
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.schemas.service_category_schemas import ServiceCategoryModel


async def get_service_categories(db: AsyncSession):
    sq = select(ServiceCategories)
    sq_res = await db.execute(sq)
    return sq_res.scalars().all()


async def get_service_category_by_id(service_category_id: int, db: AsyncSession):
    sq = select(ServiceCategories).filter_by(service_category_id=service_category_id)
    sq_res = await db.execute(sq)
    return sq_res.scalar_one_or_none()


async def get_service_category_by_service_id(service_id: int, db: AsyncSession):
    sq = select(ServiceCategories).filter_by(service_id=service_id)
    sq_res = await db.execute(sq)
    return sq_res.scalars().all()


async def create_service_category(body: ServiceCategoryModel, db: AsyncSession):
    sq_1 = select(Service).filter_by(service_id=body.service_id)
    sq_res = await db.execute(sq_1)
    service = sq_res.scalar_one_or_none()
    if service:
        new_service_category = ServiceCategories(**body.model_dump())
        db.add(new_service_category)
        await db.commit()
        await db.refresh(new_service_category)
        return new_service_category
    return None


async def update_service_category(service_category_id: int, body: ServiceCategoryModel, db: AsyncSession):
    sq_1 = select(Service).filter_by(service_id=body.service_id)
    sq_1_res = await db.execute(sq_1)
    service = sq_1_res.scalar_one_or_none()
    if service:
        sq_2 = select(ServiceCategories).filter_by(service_category_id=service_category_id)
        sq_2_res = await db.execute(sq_2)
        service_category_to_update = sq_2_res.scalar_one_or_none()
        if service_category_to_update:
            service_category_to_update.service_id = body.service_id
            service_category_to_update.service_category_ua = body.service_category_ua
            service_category_to_update.service_category_en = body.service_category_en
            await db.commit()
            await db.refresh(service_category_to_update)
        return service_category_to_update
    return None


async def delete_service_category(service_category_id: int, db: AsyncSession):
    sq = select(ServiceCategories).filter_by(service_category_id=service_category_id)
    sq_res = await db.execute(sq)
    deleted_service_category = sq_res.scalar_one_or_none()
    if deleted_service_category:
        await db.delete(deleted_service_category)
        await db.commit()
    return deleted_service_category

