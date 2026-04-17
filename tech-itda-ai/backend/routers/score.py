from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Company
from scoring_engine import calculate_score

router = APIRouter(prefix="/api/score", tags=["score"])

@router.post("/")
def get_score(company_id: str, db: Session = Depends(get_db)):
    # 기업 정보 조회
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="기업을 찾을 수 없습니다")

    # 기업 정보를 딕셔너리로 변환
    company_dict = {
        "industry": company.industry,
        "tech_level": company.tech_level,
        "revenue": company.revenue,
        "prior_rd_count": company.prior_rd_count,
        "certs": company.certs or "",
        "company_stage": company.company_stage,
    }

    # 점수 계산
    result = calculate_score(company_dict)

    return {
        "success": True,
        "company_name": company.name,
        "data": result
    }