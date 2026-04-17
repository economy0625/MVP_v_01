import math

def calculate_score(company):
    score = 0
    breakdown = {}
    deductions = []
    feedback = []

    # 1. 문제 정의 (20점) — 업종 명확성
    if company.get("industry") and company.get("industry") != "기타":
        breakdown["문제 정의"] = 16
        score += 16
    else:
        breakdown["문제 정의"] = 10
        score += 10
        feedback.append("업종을 더 구체적으로 입력하면 점수가 올라갑니다")

    # 2. 기술성 (20점) — TRL 수준
    trl = company.get("tech_level", 1)
    if trl >= 7:
        breakdown["기술성"] = 18
        score += 18
    elif trl >= 4:
        breakdown["기술성"] = 14
        score += 14
    else:
        breakdown["기술성"] = 8
        score += 8
        feedback.append("TRL 수준을 높이면 기술성 점수가 올라갑니다")

    # 3. 사업성 (20점) — 매출 규모
    revenue = company.get("revenue", 0) or 0
    if revenue >= 50000:
        breakdown["사업성"] = 18
        score += 18
    elif revenue >= 10000:
        breakdown["사업성"] = 14
        score += 14
    elif revenue > 0:
        breakdown["사업성"] = 10
        score += 10
    else:
        breakdown["사업성"] = 6
        score += 6
        feedback.append("매출 정보를 입력하면 사업성 점수가 올라갑니다")

    # 4. 수행역량 (20점) — R&D 이력 + 인증
    capability = 0
    prior_rd = company.get("prior_rd_count", 0) or 0
    certs = company.get("certs", "") or ""

    if prior_rd >= 3:
        capability += 12
    elif prior_rd >= 1:
        capability += 8
    else:
        capability += 0
        deductions.append("R&D 수행 이력 없음 (-8점)")
        feedback.append("R&D 수행 이력이 있으면 수행역량 점수가 크게 올라갑니다")

    if "이노비즈" in certs:
        capability += 8
    elif "벤처" in certs:
        capability += 6
    elif "ISO" in certs:
        capability += 4
    else:
        feedback.append("벤처기업 또는 이노비즈 인증을 받으면 가산점이 있습니다")

    breakdown["수행역량"] = min(capability, 20)
    score += breakdown["수행역량"]

    # 5. 계획 타당성 (20점) — 기업 단계 적합성
    stage = company.get("company_stage", "")
    if stage == "성장":
        breakdown["계획 타당성"] = 16
        score += 16
    elif stage == "초기":
        breakdown["계획 타당성"] = 14
        score += 14
    elif stage == "예비창업":
        breakdown["계획 타당성"] = 12
        score += 12
    else:
        breakdown["계획 타당성"] = 8
        score += 8

    # 감점 요소
    if prior_rd == 0:
        score = max(0, score - 8)

    # sigmoid 함수로 확률 변환 (0~100%)
    probability = round(1 / (1 + math.exp(-(score - 50) / 15)) * 100, 1)

    return {
        "total_score": score,
        "probability": probability,
        "breakdown": breakdown,
        "deductions": deductions,
        "feedback": feedback,
    }