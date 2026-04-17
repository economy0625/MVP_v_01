from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Company

router = APIRouter(prefix="/api/companies", tags=["companies"])

class CompanyCreate(BaseModel):
    name: str
    industry: str
    company_stage: str
    tech_level: int
    revenue: Optional[float] = 0
    employee_count: Optional[int] = 0
    location: str
    certs: Optional[str] = ""
    prior_rd_count: Optional[int] = 0

@router.post("/")
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return {"success": True, "data": {"id": str(db_company.id), "name": db_company.name}}

@router.get("/{company_id}")
def get_company(company_id: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="기업을 찾을 수 없습니다")
    return {"success": True, "data": company}

@router.get("/")
def get_companies(db: Session = Depends(get_db)):
    companies = db.query(Company).all()
    return {"success": True, "data": companies}