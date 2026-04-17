from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from dotenv import load_dotenv
import models
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# 테이블 자동 생성
Base.metadata.create_all(bind=engine)

# 시드 데이터 자동 실행
from seed_data import seed, seed_experts
seed()
seed_experts()

app = FastAPI(title="테크잇다AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://mvp-v-01.vercel.app",
        "https://mvp-v-01-git-main-economy0625s-projects.vercel.app",
        "*"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 연결
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