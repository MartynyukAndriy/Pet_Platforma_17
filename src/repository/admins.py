import logging

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.models import Admin, User, Role
from src.schemas.user_schemas import AdminModel, UserModel


async def get_admin_by_email(email: str, db: AsyncSession) -> Admin | None:
    sq = select(Admin).join(User).filter(User.email == email)
    result = await db.execute(sq)
    admin = result.scalar_one_or_none()
    logging.info(admin)
    return admin


async def create_admin_from_client(user_id: int, db: AsyncSession) -> Admin:
    user = await db.get(User, user_id)

    if user:
        existing_admin = await db.execute(select(Admin).filter_by(user_id=user_id))
        existing_admin = existing_admin.scalar_one_or_none()

        if existing_admin:
            # Якщо адмін існує і має is_active == False, то змінюємо його на активного
            if not existing_admin.is_active:
                existing_admin.is_active = True
                await db.commit()
                await db.refresh(existing_admin)
                return existing_admin
            else:
                raise HTTPException(status_code=400, detail="Admin already exists for this user")
        else:
            # Якщо адміна немає, то створюємо нового
            user.user_role = Role.admin
            new_admin = Admin(user_id=user.user_id, is_active=True)
            db.add(new_admin)
            await db.commit()
            await db.refresh(new_admin)
            return new_admin
    else:
        raise HTTPException(status_code=404, detail="User not found")


async def create_client_from_admin(admin_id: int, db: AsyncSession) -> User:
    admin = await db.get(Admin, admin_id)

    if admin:
        user = await db.get(User, admin.user_id)

        if user:
            if user.user_role == Role.client:
                raise HTTPException(status_code=400, detail="User is already a client")

            admin.is_active = False
            user.user_role = Role.client
            await db.commit()
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    else:
        raise HTTPException(status_code=404, detail="Admin not found")


# async def block(email: str, body: AdminModel, db: AsyncSession):
#     admin = await get_admin_by_email(email, db)
#     if admin:
#         admin.banned = body.banned
#     await db.commit()
#     return admin


async def get_all_clients(db: AsyncSession) -> list[UserModel]:
    sq = select(User).filter(User.user_role == Role.client)
    result = await db.execute(sq)
    clients = result.scalars().all()
    return clients


async def get_all_masters(db: AsyncSession) -> list[UserModel]:
    sq = select(User).filter(User.user_role == Role.master)
    result = await db.execute(sq)
    masters = result.scalars().all()
    return masters

