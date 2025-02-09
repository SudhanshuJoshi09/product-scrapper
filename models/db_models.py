from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)


class ScrapingRecord(Base):
    __tablename__ = "scraping_records"
    id = Column(Integer, primary_key=True, index=True)
    page_number = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Scheduler(Base):
    __tablename__ = "scheduler"
    id = Column(Integer, primary_key=True, index=True)
    scraping_record = Column(Integer, ForeignKey("scraping_records.id"))
    created_time = Column(DateTime, default=datetime.datetime.utcnow)
    execution_time = Column(DateTime)
    status = Column(String, default="scheduled")
    count = Column(Integer, default=0)
