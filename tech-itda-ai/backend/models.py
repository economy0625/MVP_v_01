from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    industry = Column(String)
    company_stage = Column(String)
    tech_level = Column(Integer)
    revenue = Column(Float)
    location = Column(String)

class Program(Base):
    __tablename__ = "programs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    agency = Column(String)
    category = Column(String)
    target_stage = Column(String)
    trl_min = Column(Integer)
    trl_max = Column(Integer)
    deadline = Column(String)