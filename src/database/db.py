from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DatabaseError


# from src.conf.config import settings
# SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url
# engine = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True, echo=True)
# SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Тимчасово, для тестування в SQLite:
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except HTTPException:
        db.rollback()
    finally:
        db.close()
