from sqlalchemy import Column, String, Integer
from .database import Base

class Job(Base):
    __tablename__ = "Jobs"

    Company = Column(String, nullable = False)
    Role = Column(String, nullable = False)
    Location = Column(String, nullable = False)
    Date_Posted = Column(String, nullable = False)
    Link = Column(String, nullable = False, primary_key = True)    
    Days = Column(Integer, nullable = False)
