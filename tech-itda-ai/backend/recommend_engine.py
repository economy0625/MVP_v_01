# 추천 엔진 — Rule 기반
# 기업 정보를 받아서 지원사업 점수를 계산하고 상위 3개를 추천

def calculate_match_score(company, program):
    score = 0
    reasons = []

    # Rule 1: 기업 단계 매칭 (40점)
    stage_map = {
        "예비창업": ["예비창업"],
        "초기":     ["초기", "예비창업"],
        "성장":     ["성장", "초기"],
    }
    allowed_stages = stage_map.get(company.get("company_stage", ""), [])
    if program.get("target_stage") in allowed_stages:
        score += 40
        reasons.append("기업 단계 일치")

    # Rule 2: TRL 범위 매칭 (30점)
    trl = company.get("tech_level", 1)
    trl_min = program.get("trl_min", 1)
    trl_max = program.get("trl_max", 9)
    if trl_min <= trl <= trl_max:
        score += 30
        reasons.append("기술 수준(TRL) 일치")

    # Rule 3: 지역 매칭 (20점)
    region = program.get("region", "전국")
    if region == "전국":
        score += 10
        reasons.append("전국 지원 가능")
    elif region == company.get("location", ""):
        score += 20
        reasons.append("지역 우선 사업")

    # Rule 4: 인증 보유 가산점 (10점)
    certs = company.get("certs", "")
    if "이노비즈" in certs:
        score += 7
        reasons.append("이노비즈 가산점")
    elif "벤처" in certs:
        score += 5
        reasons.append("벤처기업 가산점")
    elif "ISO" in certs:
        score += 3
        reasons.append("ISO 인증 가산점")

    return score, reasons


def recommend_programs(company, programs):
    results = []

    for program in programs:
        program_dict = {
            "id": str(program.id),
            "name": program.name,
            "agency": program.agency,
            "category": program.category,
            "target_stage": program.target_stage,
            "trl_min": program.trl_min,
            "trl_max": program.trl_max,
            "budget_min": program.budget_min,
            "budget_max": program.budget_max,
            "deadline": program.deadline,
            "region": program.region,
        }

        score, reasons = calculate_match_score(company, program_dict)

        if score > 0:
            results.append({
                "program": program_dict,
                "match_score": score,
                "reasons": reasons,
            })

    # 점수 높은 순으로 정렬 후 상위 3개 반환
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results[:3]