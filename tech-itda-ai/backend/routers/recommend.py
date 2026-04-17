from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Company, Program
from recommend_engine import recommend_programs

router = APIRouter(prefix="/api/recommend", tags=["recommend"])

@router.post("/")
def get_recommendations(company_id: str, db: Session = Depends(get_db)):
    # 기업 정보 조회
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="기업을 찾을 수 없습니다")

    # 전체 지원사업 조회
    programs = db.query(Program).all()

    # 기업 정보를 딕셔너리로 변환
    company_dict = {
        "company_stage": company.company_stage,
        "tech_level": company.tech_level,
        "location": company.location,
        "certs": company.certs or "",
    }

    # 추천 엔진 실행
    recommendations = recommend_programs(company_dict, programs)

    return {
        "success": True,
        "company_name": company.name,
        "data": recommendations
    }