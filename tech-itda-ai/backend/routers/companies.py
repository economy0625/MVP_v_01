from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(prefix="/api/companies", tags=["companies"])


@router.post("")
def create_company(body: dict):
    # TODO: domain/data/ 연결
    return {
        "success": True,
        "data": {},
        "error": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/{company_id}")
def get_company(company_id: str):
    # TODO: domain/data/ 연결
    return {
        "success": True,
        "data": {"id": company_id},
        "error": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.put("/{company_id}")
def update_company(company_id: str, body: dict):
    # TODO: domain/data/ 연결
    return {
        "success": True,
        "data": {"id": company_id},
        "error": None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
