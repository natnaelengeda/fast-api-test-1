# SQL
from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from db import Base


#SQLAlchemy model
class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    skills = Column(JSON)
    education = Column(JSON)
    experience = Column(JSON)
    raw_text = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())