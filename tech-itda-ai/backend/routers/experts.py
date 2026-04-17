from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Expert, Company

router = APIRouter(prefix="/api/experts", tags=["experts"])

def calculate_expert_match(company, expert):
    score = 0
    reasons = []

    # 분야 매칭
    expert_fields = expert.fields.split(",") if expert.fields else []
    if company.industry:
        for field in expert_fields:
            if field.strip() in company.industry or company.industry in field.strip():
                score += 40
                reasons.append(f"{field.strip()} 분야 일치")
                break

    # 지역 매칭
    if expert.location == company.location:
        score += 30
        reasons.append("같은 지역")
    elif expert.location == "전국":
        score += 10

    # 등급 가산점
    if expert.grade == "넥서스인증":
        score += 20
        reasons.append("넥서스 인증 전문가")
    elif expert.grade == "골드":
        score += 15
        reasons.append("골드 등급")
    elif expert.grade == "실버":
        score += 10

    # 평점 가산점
    if expert.rating >= 4.8:
        score += 10
        reasons.append(f"평점 {expert.rating}")
    elif expert.rating >= 4.5:
        score += 5

    return score, reasons

# 전문가 목록 조회
@router.get("/")
def get_experts(db: Session = Depends(get_db)):
    experts = db.query(Expert).all()
    result = []
    for e in experts:
        result.append({
            "id": str(e.id),
            "name": e.name,
            "grade": e.grade,
            "fields": e.fields,
            "rating": e.rating,
            "location": e.location,
            "career": e.career,
            "available": e.available,
        })
    return {"success": True, "data": result}

# 기업 맞춤 전문가 매칭
@router.post("/match")
def match_experts(company_id: str, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        return {"success": False, "message": "기업을 찾을 수 없습니다"}

    experts = db.query(Expert).filter(Expert.available == "가능").all()

    results = []
    for expert in experts:
        score, reasons = calculate_expert_match(company, expert)
        if score > 0:
            results.append({
                "expert": {
                    "id": str(expert.id),
                    "name": expert.name,
                    "grade": expert.grade,
                    "fields": expert.fields,
                    "rating": expert.rating,
                    "location": expert.location,
                    "career": expert.career,
                },
                "match_score": score,
                "reasons": reasons,
            })

    results.sort(key=lambda x: x["match_score"], reverse=True)

    return {
        "success": True,
        "company_name": company.name,
        "data": results[:3]
    }