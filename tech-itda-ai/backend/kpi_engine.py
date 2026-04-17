# KPI 물리 검증 엔진
# 분야별 물리 수식으로 KPI 달성 가능성을 판정

PHYSICS_RULES = {
    "경량화": {
        "max_reduction": 30,
        "unit": "%",
        "formula": "밀도 × 체적 = 질량",
        "description": "일반 금속 소재 기준 최대 30% 경량화 가능 (소재 변경 없이)",
        "tip": "소재를 탄소섬유/알루미늄으로 변경 시 최대 50%까지 가능"
    },
    "강도": {
        "max_improvement": 40,
        "unit": "%",
        "formula": "σ = F/A (응력 = 힘/단면적)",
        "description": "열처리/합금 기준 최대 40% 강도 향상 가능",
        "tip": "소재 변경 시 더 높은 강도 달성 가능"
    },
    "에너지효율": {
        "max_improvement": 30,
        "unit": "%",
        "formula": "η = W_out / W_in × 100",
        "description": "일반적인 공정 최적화로 최대 30% 효율 향상 가능",
        "tip": "시스템 전체 재설계 시 더 높은 효율 달성 가능"
    },
    "생산성": {
        "max_improvement": 50,
        "unit": "%",
        "formula": "생산성 = 산출량 / 투입량",
        "description": "공정 자동화 기준 최대 50% 생산성 향상 가능",
        "tip": "스마트팩토리 도입 시 더 높은 생산성 달성 가능"
    },
    "불량률": {
        "max_reduction": 80,
        "unit": "%",
        "formula": "불량률 = 불량품 수 / 전체 생산량 × 100",
        "description": "공정 개선으로 불량률 최대 80% 감소 가능",
        "tip": "AI 품질검사 도입 시 추가 개선 가능"
    },
}

def validate_kpi(field: str, target_value: float, unit: str) -> dict:
    """KPI 물리 검증"""
    rule = PHYSICS_RULES.get(field)

    if not rule:
        return {
            "status": "검증불가",
            "message": f"{field} 분야는 자동 검증이 어렵습니다. 전문가 검토를 권장합니다.",
            "formula": "-",
            "needs_expert_review": True
        }

    max_val = rule.get("max_improvement") or rule.get("max_reduction", 100)

    if target_value <= max_val:
        return {
            "status": "달성가능",
            "message": f"물리적으로 달성 가능한 범위입니다. (상한: {max_val}{unit})",
            "formula": rule["formula"],
            "description": rule["description"],
            "needs_expert_review": False
        }
    else:
        corrected = max_val * 0.8  # 안전 마진 20%
        return {
            "status": "보정필요",
            "message": f"목표값이 물리적 한계를 초과합니다. {corrected}{unit}으로 조정을 권장합니다.",
            "formula": rule["formula"],
            "description": rule["description"],
            "corrected_value": corrected,
            "tip": rule["tip"],
            "needs_expert_review": True
        }


def get_supported_fields() -> list:
    """지원하는 물리 검증 분야 목록"""
    return list(PHYSICS_RULES.keys())