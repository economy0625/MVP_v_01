from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Railway 환경에서는 DATABASE_URL 환경변수 직접 사용
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
    DATABASE_URL = os.environ.get("DATABASE_URL")

print(f"DATABASE_URL: {DATABASE_URL[:30]}...")  # 디버그용

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()