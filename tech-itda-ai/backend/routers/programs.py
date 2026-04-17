from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Program

router = APIRouter(prefix="/api/programs", tags=["programs"])

@router.get("/")
def get_programs(db: Session = Depends(get_db)):
    programs = db.query(Program).all()
    return {"success": True, "data": programs}