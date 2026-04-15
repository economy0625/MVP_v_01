from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(prefix="/api/score", tags=["score"])


@router.post("")
def calculate_score(body: dict):
    # TODO: domain/scoring/ 연결
    return {
        "success": True,
        "data": {},
        "error": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/{result_id}")
def get_score_result(result_id: str):
    # TODO: domain/scoring/ 연결
    return {
        "success": True,
        "data": {"id": result_id},
        "error": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
