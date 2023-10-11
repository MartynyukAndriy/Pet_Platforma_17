import asyncio
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User, MasterInfo, MastersToServices
from src.schemas.user_schemas import MasterModel


async def create_master(body: MasterModel, db: AsyncSession):
    new_user = User(
        password=body.password,
        name=body.name,
        email=body.email,
        country_id=body.country_id,
        city_id=body.city_id,
        phone=body.phone,
        avatar=body.avatar,
        role="master"
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # create master
    new_master = MasterInfo(
        user_id=new_user.user_id,
        salon_name=body.salon_name,
        salon_address=body.salon_address
    )
    db.add(new_master)
    await db.commit()
    await db.refresh(new_master)

    if body.masters_to_services:
        for serv in body.masters_to_services:
            offer = MastersToServices(
                master_id=new_master.master_id,
                service_id=serv.service_id,
                service_category_id=serv.service_category_id,
                service_price=serv.price
            )
            db.add(offer)

        await db.commit()

    sq = select(User).join(MasterInfo)
    result = await db.execute(sq)
    master = result.first()
    return master


async def get_master_info(user_id, db: AsyncSession):
    sq = select(User).join(MasterInfo).filter_by(user_id=user_id)
    result = await db.execute(sq)
    master = result.scalar_one_or_none()
    return master
