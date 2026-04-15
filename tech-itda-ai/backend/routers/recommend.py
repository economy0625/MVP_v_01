from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(prefix="/api/recommend", tags=["recommend"])


@router.post("")
def run_recommend(body: dict):
    # TODO: domain/recommendation/ 연결
    return {
        "success": True,
        "data": {},
        "error": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/{result_id}")
def get_recommend_result(result_id: str):
    # TODO: domain/recommendation/ 연결
    return {
        "success": True,
        "data": {"id": result_id},
        "error": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
