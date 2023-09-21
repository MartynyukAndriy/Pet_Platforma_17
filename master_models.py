from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, func
from sqlalchemy.orm import declarative_base, relationship, session

Base = declarative_base()


##########################################################
# Щоб не було помилки
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
##########################################################


class Admin(Base):
    __tablename__ = 'admin'
    admin_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    is_active = Column(Boolean, default=False)
    last_visit = Column(DateTime, default=func.now())


class MasterInfo(Base):
    __tablename__ = 'master_info'
    master_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False, index=True)
    description = Column(String, nullable=True)
    salon_name = Column(String, nullable=True)
    salon_address = Column(String, nullable=True)
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    is_active = Column(Boolean, default=False)
    plan_id = Column(Integer, ForeignKey('subscribe_plans.plan_id'))
    free_period = Column(Integer, nullable=True)
    plan_period = Column(Integer, nullable=True)
    subscribe_plan_rel = relationship("SubscribePlans", foreign_keys=[plan_id], backref="master_info")


class SubscribePlan(Base):
    __tablename__ = 'subscribe_plan'
    plan_id = Column(Integer, primary_key=True, index=True)
    subscribe_plan = Column(String, nullable=False)
    plan_period = Column(Integer, nullable=False)
    master_info = relationship("MasterInfo", backref="subscribe_plans")


class WorkPhoto(Base):
    __tablename__ = 'work_photos'
    work_photo_id = Column(Integer, primary_key=True, index=True)
    master_id = Column(Integer, ForeignKey('master_info.master_id'), nullable=False)
    work_photo_url = Column(String, nullable=True)


