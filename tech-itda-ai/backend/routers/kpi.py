from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models import Company
from kpi_engine import validate_kpi, get_supported_fields
import anthropic
import os
import json
import re

router = APIRouter(prefix="/api/kpi", tags=["kpi"])

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class KpiGenerateRequest(BaseModel):
    company_id: str
    tech_goal: str

class KpiValidateRequest(BaseModel):
    field: str
    target_value: float
    unit: str

# KPI 자동 생성
@router.post("/generate")
def generate_kpi(request: KpiGenerateRequest, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.id == request.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="기업을 찾을 수 없습니다")

    prompt = f"""
당신은 R&D 지원사업 전문가입니다.
아래 기업 정보와 기술 목표를 바탕으로 정량적인 KPI를 3개 생성해주세요.

기업 정보:
- 업종: {company.industry}
- 기업 단계: {company.company_stage}
- 기술 수준(TRL): {company.tech_level}
- 기술 목표: {request.tech_goal}

반드시 아래 JSON 형식으로만 답하세요. 다른 텍스트나 설명 없이 JSON만 출력하세요.

{{
  "kpis": [
    {{
      "name": "KPI 이름",
      "target": "정량 목표 수치와 단위",
      "verification": "검증 방법",
      "period": "달성 기간",
      "field": "불량률"
    }},
    {{
      "name": "KPI 이름",
      "target": "정량 목표 수치와 단위",
      "verification": "검증 방법",
      "period": "달성 기간",
      "field": "생산성"
    }},
    {{
      "name": "KPI 이름",
      "target": "정량 목표 수치와 단위",
      "verification": "검증 방법",
      "period": "달성 기간",
      "field": "에너지효율"
    }}
  ]
}}

field 값은 반드시 경량화/강도/에너지효율/생산성/불량률 중 하나여야 합니다.
"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        response_text = message.content[0].text.strip()

        # JSON 블록 추출
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            kpi_data = json.loads(json_match.group())
        else:
            kpi_data = json.loads(response_text)

    except Exception as e:
        kpi_data = {"kpis": [], "error": f"파싱 오류: {str(e)}", "raw": response_text}

    return {
        "success": True,
        "company_name": company.name,
        "tech_goal": request.tech_goal,
        "data": kpi_data
    }

# KPI 물리 검증
@router.post("/validate")
def validate_kpi_endpoint(request: KpiValidateRequest):
    result = validate_kpi(request.field, request.target_value, request.unit)
    return {
        "success": True,
        "data": result
    }

# 지원 분야 목록
@router.get("/fields")
def get_fields():
    return {
        "success": True,
        "data": get_supported_fields()
    }