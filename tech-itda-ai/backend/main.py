from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from database import Base, engine
import models

Base.metadata.create_all(bind=engine)

import anthropic
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.get("/")
def health_check():
    return {"status": "ok", "service": "테크잇다AI API"}

@app.get("/test-claude")
def test_claude():
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=100,
        messages=[
            {"role": "user", "content": "안녕! 테크잇다AI API 연동 테스트야. 한 줄로 답해줘."}
        ]
    )
    return {"response": message.content[0].text}
