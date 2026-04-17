from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
from models import Company, Program
import anthropic
import os
import json

router = APIRouter(prefix="/api/plan", tags=["plan"])

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

class PlanGenerateRequest(BaseModel):
    company_id: str
    program_id: str
    tech_goal: str
    kpis: Optional[List[str]] = []

@router.post("/generate")
def generate_plan(request: PlanGenerateRequest, db: Session = Depends(get_db)):
    # 기업 정보 조회
    company = db.query(Company).filter(
        Company.id == request.company_id
    ).first()
    if not company:
        raise HTTPException(status_code=404, detail="기업을 찾을 수 없습니다")

    # 지원사업 정보 조회
    program = db.query(Program).filter(
        Program.id == request.program_id
    ).first()
    if not program:
        raise HTTPException(status_code=404, detail="지원사업을 찾을 수 없습니다")

    kpi_text = "\n".join([f"- {k}" for k in request.kpis]) if request.kpis else "- KPI 미입력"

    prompt = f"""
당신은 정부 R&D 지원사업 사업계획서 전문 작성가입니다.
아래 정보를 바탕으로 사업계획서 초안을 작성해주세요.

[기업 정보]
- 기업명: {company.name}
- 업종: {company.industry}
- 기업 단계: {company.company_stage}
- 기술 수준(TRL): {company.tech_level}
- 지역: {company.location}
- 보유 인증: {company.certs or "없음"}

[지원사업 정보]
- 사업명: {program.name}
- 주관기관: {program.agency}
- 사업 유형: {program.category}

[기술 목표]
{request.tech_goal}

[KPI]
{kpi_text}

아래 6개 섹션으로 사업계획서 초안을 작성해주세요.
각 섹션은 200~300자 분량으로 작성하세요.
모든 내용은 구체적이고 정량적으로 작성하세요.

반드시 아래 JSON 형식으로만 답하세요:

{{
  "sections": [
    {{
      "title": "1. 사업 개요 및 필요성",
      "content": "내용"
    }},
    {{
      "title": "2. 기술 개발 목표",
      "content": "내용"
    }},
    {{
      "title": "3. 개발 내용 및 방법",
      "content": "내용"
    }},
    {{
      "title": "4. 추진 일정",
      "content": "내용"
    }},
    {{
      "title": "5. 기대 성과 및 활용 방안",
      "content": "내용"
    }},
    {{
      "title": "6. 보유 역량 및 수행 체계",
      "content": "내용"
    }}
  ]
}}
"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )

    import re
    try:
        response_text = message.content[0].text.strip()
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            plan_data = json.loads(json_match.group())
        else:
            plan_data = json.loads(response_text)
    except Exception as e:
        plan_data = {"sections": [], "error": f"파싱 오류: {str(e)}"}

    return {
        "success": True,
        "company_name": company.name,
        "program_name": program.name,
        "data": plan_data
    }