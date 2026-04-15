from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(prefix="/api/plan", tags=["plan"])


@router.post("/generate")
async def generate_plan(body: dict):
    # TODO: domain/planning/ 연결 (LLM 비동기 호출)
    return {
        "success": True,
        "data": {},
        "error": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/{plan_id}")
def get_plan(plan_id: str):
    # TODO: domain/planning/ 연결
    return {
        "success": True,
        "data": {"id": plan_id},
        "error": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.put("/{plan_id}")
def update_plan(plan_id: str, body: dict):
    # TODO: domain/planning/ 연결
    return {
        "success": True,
        "data": {"id": plan_id},
        "error": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
