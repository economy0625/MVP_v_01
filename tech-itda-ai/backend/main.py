from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="테크잇다AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 연결
from routers import companies, programs, recommend, score
app.include_router(companies.router)
app.include_router(programs.router)
app.include_router(recommend.router)
app.include_router(score.router)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "테크잇다AI API"}