from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

from database import Base, engine

# 모든 모델 명시적으로 import
from models import Company, Program, Expert

# 테이블 강제 생성
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# 시드 데이터 실행
try:
    from seed_data import seed, seed_experts
    seed()
    seed_experts()
    print("✅ 시드 데이터 완료")
except Exception as e:
    print(f"시드 오류: {e}")

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