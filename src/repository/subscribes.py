from src.database.models import SubscribePlan
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.schemas.subscribe_schemas import SubscribeModel


async def get_sub_plans(db: AsyncSession):
    sq = select(SubscribePlan)
    sq_res = await db.execute(sq)
    return sq_res.scalars().all()


async def get_sub_plan_by_id(plan_id: int, db: AsyncSession):
    sq = select(SubscribePlan).filter_by(plan_id=plan_id)
    sq_res = await db.execute(sq)
    return sq_res.scalar_one_or_none()


async def create_sub_plan(body: SubscribeModel, db: AsyncSession):
    new_plan = SubscribePlan(**body.model_dump())
    db.add(new_plan)
    await db.commit()
    await db.refresh(new_plan)
    return new_plan


async def update_sub_plan(plan_id: int, body: SubscribeModel, db: AsyncSession):
    sq = select(SubscribePlan).filter_by(plan_id=plan_id)
    sq_res = await db.execute(sq)
    s_plan = sq_res.scalar_one_or_none()
    if s_plan:
        s_plan.subscribe_plan = body.subscribe_plan
        s_plan.plan_period = body.plan_period
        await db.commit()
        await db.refresh(s_plan)
    return s_plan


async def delete_sub_plan(plan_id: int, db: AsyncSession):
    sq = select(SubscribePlan).filter_by(plan_id=plan_id)
    sq_res = await db.execute(sq)
    deleted_plan = sq_res.scalar_one_or_none()
    if deleted_plan:
        await db.delete(deleted_plan)
        await db.commit()
    return deleted_plan
