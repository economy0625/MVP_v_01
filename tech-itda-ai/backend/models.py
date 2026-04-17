from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from datetime import datetime
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
    employee_count = Column(Integer)
    location = Column(String)
    certs = Column(String)
    prior_rd_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Program(Base):
    __tablename__ = "programs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    agency = Column(String)
    category = Column(String)
    target_stage = Column(String)
    trl_min = Column(Integer)
    trl_max = Column(Integer)
    budget_min = Column(Float)
    budget_max = Column(Float)
    deadline = Column(String)
    region = Column(String, default="전국")

class Expert(Base):
    __tablename__ = "experts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    grade = Column(String, default="일반")
    fields = Column(String)
    programs = Column(String)
    rating = Column(Float, default=4.0)
    location = Column(String)
    career = Column(String)
    available = Column(String, default="가능")