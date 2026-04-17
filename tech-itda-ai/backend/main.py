from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# 1. 환경변수 로드
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# 2. DB 연결
from database import Base, engine

# 3. 모델 import (반드시 create_all 전에)
from models import Company, Program, Expert

# 4. 테이블 생성
print("테이블 생성 시작...")
Base.metadata.create_all(bind=engine)
print("테이블 생성 완료!")

# 5. 시드 데이터 (테이블 생성 완료 후)
from database import SessionLocal
from models import Program as ProgramModel

try:
    db = SessionLocal()
    count = db.query(ProgramModel).count()
    db.close()
    if count == 0:
        print("시드 데이터 실행...")
        from seed_data import seed, seed_experts
        seed()
        seed_experts()
        print("시드 데이터 완료!")
    else:
        print(f"시드 데이터 이미 있음: {count}개")
except Exception as e:
    print(f"시드 오류: {e}")

# 6. FastAPI 앱 생성
app = FastAPI(title="테크잇다AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers import companies, programs, recommend, score, kpi, plan, experts
app.include_router(companies.router)
app.include_router(programs.router)
app.include_router(recommend.router)
app.include_router(score.router)
app.include_router(kpi.router)
app.include_router(plan.router)
app.include_router(experts.router)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "테크잇다AI API"}