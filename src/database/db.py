from fastapi import HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.conf.config import settings


SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except HTTPException:
        db.rollback()
    finally:
        db.close()

