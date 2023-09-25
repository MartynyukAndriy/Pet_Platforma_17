from sqlalchemy.ext.asyncio import create_async_engine
from src.conf.config import settings
from src.database.models import Country

async def add_ukraine():
    engine = create_async_engine(settings.sqlalchemy_database_url)
    async with engine.begin() as conn:
        ukraine = Country(country_ukr="Україна", country_eng="Ukraine")
        conn.add(ukraine)
        await conn.commit()

async def main():
    await add_ukraine()

# Викликайте головну функцію в асинхронному середовищі
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

