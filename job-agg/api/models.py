from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime, timezone
from .database import Base

#models.py defines two tables within our PostgreSQL DB


class Job(Base):
    __tablename__ = "Jobs"

    Company = Column(String, nullable = False)
    Role = Column(String, nullable = False)
    Date_Found = Column(DateTime, nullable = False)
    Location = Column(String, nullable = False)
    Link = Column(String, nullable = False, primary_key = True)    


class Resume(Base):
    __tablename__ = "Resume"

    id = Column(Integer, nullable = False, primary_key = True)
    Content = Column(String, nullable = False)
    Normalized = Column(String, nullable = False)
