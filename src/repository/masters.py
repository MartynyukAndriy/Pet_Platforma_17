from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User, MasterInfo
from src.schemas.user_schemas import MasterModel


async def create_master(body: MasterModel, db: AsyncSession):
    new_user = User(password=body.password,
                    name=body.name,
                    email=body.email,
                    country_id=body.country_id,
                    city_id=body.city_id,
                    phone=body.phone,
                    avatar=body.avatar,
                    user_role="master"
                    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # when we saved user we get his user_id
    sq = select(User).filter_by(email=body.email)
    result = await db.execute(sq)
    user = result.scalar_one_or_none()

    new_master = MasterInfo(user_id=user.user_id,
                            description=body.description,
                            salon_name=body.salon_name,
                            salon_address=body.salon_address,
                            longitude=body.longitude,
                            latitude=body.latitude,
                            is_active=True
                            )
    db.add(new_master)
    await db.commit()
    await db.refresh(new_master)
    return new_master


async def get_master_info(user_id, db: AsyncSession):
    sq = select(User).join(MasterInfo).filter_by(user_id=user_id)
    result = await db.execute(sq)
    master = result.scalar_one_or_none()
    return master
