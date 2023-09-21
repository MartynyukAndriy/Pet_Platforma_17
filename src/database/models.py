from datetime import datetime
import enum
from typing import List
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Enum, Integer
from sqlalchemy.orm import declarative_base, relationship
from src.database.db import engine


Base = declarative_base()


class Role(enum.Enum):
    admin = 'admin'
    moderator = 'moderator'
    user = 'user'


class Country(Base):
    __tablename__ = "countries"

    country_id = Column(Integer, primary_key=True)
    country_ukr = Column(String(50), nullable=False)
    country_eng = Column(String(50), nullable=False)
    cities = relationship("City", backref="country")

    def __str__(self):
        return self.country_eng


class City(Base):
    __tablename__ = "cities"

    city_id = Column(Integer, primary_key=True)
    city_ukr = Column(String(50), nullable=False)
    city_eng = Column(String(50), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.country_id"), nullable=False)
    users = relationship("User", backref="city")

    def __str__(self):
        return self.city_eng


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_role = Column('role', Enum(Role), default=Role.user)
    password = Column(String(255), nullable=False)
    name = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    country_id = Column(Integer, ForeignKey("countries.country_id"), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.city_id"), nullable=False)
    phone = Column(String(255))
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return f"User id: {self.user_id}"


Base.metadata.create_all(bind=engine)