from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(prefix="/api/experts", tags=["experts"])


@router.get("")
def list_experts():
    # TODO: domain/expert/ 연결
    return {
        "success": True,
        "data": [],
        "error": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.post("/match")
def match_expert(body: dict):
    # TODO: domain/expert/ 연결
    return {
        "success": True,
        "data": {},
        "error": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/{expert_id}")
def get_expert(expert_id: str):
    # TODO: domain/expert/ 연결
    return {
        "success": True,
        "data": {"id": expert_id},
        "error": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
