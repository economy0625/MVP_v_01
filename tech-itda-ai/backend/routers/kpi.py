from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(prefix="/api/kpi", tags=["kpi"])


@router.post("/generate")
def generate_kpi(body: dict):
    # TODO: domain/kpi/ 연결 (KPI 자동 생성)
    return {
        "success": True,
        "data": {},
        "error": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.post("/validate")
def validate_kpi(body: dict):
    # TODO: domain/kpi/ 연결 (물리 검증)
    return {
        "success": True,
        "data": {},
        "error": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/{kpi_id}")
def get_kpi(kpi_id: str):
    # TODO: domain/kpi/ 연결
    return {
        "success": True,
        "data": {"id": kpi_id},
        "error": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
