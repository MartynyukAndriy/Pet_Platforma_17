from datetime import datetime
import enum

import uuid
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Enum, Integer, func, Float, Table
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.schema import Table


Base = declarative_base()


class Role(enum.Enum):
    client = 'client'
    master = 'master'
    admin = 'admin'
    moderator = 'moderator'
    superadmin = 'superadmin'


class Country(Base):
    __tablename__ = "countries"

    country_id = Column(Integer, primary_key=True)
    country_ukr = Column(String(255), nullable=False)
    country_eng = Column(String(255), nullable=False)
    cities = relationship("City", backref="country")

    def __str__(self):
        return self.country_eng


class City(Base):
    __tablename__ = "cities"

    city_id = Column(Integer, primary_key=True)
    city_ukr = Column(String(255), nullable=False)
    city_eng = Column(String(255), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.country_id"), nullable=False)
    users = relationship("User", backref="city")

    def __str__(self):
        return self.city_eng


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_role = Column('role', Enum(Role), default=Role.client)
    password = Column(String(255), nullable=False)
    name = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    country_id = Column(Integer, ForeignKey("countries.country_id"), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.city_id"), nullable=False)
    phone = Column(String(255))
    avatar = Column(String(255), nullable=True)
    birthday = Column(DateTime, nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return f"User:{self.email}"


class Admin(Base):
    __tablename__ = 'admin'
    admin_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False, default=uuid.uuid4)
    is_active = Column(Boolean, default=False)
    last_visit = Column(DateTime, default=func.now())


class SubscribePlan(Base):
    __tablename__ = 'subscribe_plans'
    plan_id = Column(Integer, primary_key=True, index=True)
    subscribe_plan = Column(String, nullable=False)
    plan_period = Column(Integer, nullable=False)


class MasterInfo(Base):
    __tablename__ = 'master_info'
    master_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False, index=True, default=uuid.uuid4)
    description = Column(String, nullable=True)
    salon_name = Column(String, nullable=True)
    salon_address = Column(String, nullable=True)
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    plan_id = Column(Integer, ForeignKey('subscribe_plans.plan_id'))
    free_period = Column(Integer, nullable=True)
    plan_period = Column(Integer, nullable=True)
    subscribe_plan_rel = relationship("SubscribePlan", foreign_keys=[plan_id], backref="master_info")


class WorkPhoto(Base):
    __tablename__ = 'work_photos'
    work_photo_id = Column(Integer, primary_key=True, index=True)
    master_id = Column(UUID(as_uuid=True), ForeignKey('master_info.master_id'), nullable=False, default=uuid.uuid4)
    work_photo_url = Column(String, nullable=True)


class UserResponse(Base):
    __tablename__ = 'user_responses'
    id = Column(Integer, primary_key=True, index=True)
    master_id = Column(UUID(as_uuid=True), ForeignKey('master_info.master_id'), nullable=False, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False, index=True, default=uuid.uuid4)
    rate = Column(Integer, nullable=True)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Service(Base):
    __tablename__ = 'services'
    service_id = Column(Integer, primary_key=True, index=True)
    service_ua = Column(String, nullable=True)
    service_en = Column(String, nullable=True)


class ServiceCategories(Base):
    __tablename__ = 'service_categories'
    service_category_id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey('services.service_id'), nullable=False)
    service_category_ua = Column(String, nullable=True)
    service_category_en = Column(String, nullable=True)


class Currency(Base):
    __tablename__ = 'currencies'
    currency_id = Column(Integer, primary_key=True, index=True)
    currency = Column(String, nullable=False)


users_m2m_services = Table(
    'masters_m2m_services',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('master_id', UUID(as_uuid=True), ForeignKey('master_info.master_id'), default=uuid.uuid4),
    Column('service_id', Integer, ForeignKey('services.service_id'), nullable=False),
    Column('service_category_id', Integer, ForeignKey('service_categories.service_category_id'), nullable=False),
    Column('service_description', String, nullable=True),
    Column('service_price', Float, nullable=False),
    Column('service_sale_price', Float, nullable=True),
    Column('discount', Float, nullable=True),
    Column('currency_id', Integer, ForeignKey('currencies.currency_id')),
)
