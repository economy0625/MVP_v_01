from database import SessionLocal, Base, engine
from models import Program

Base.metadata.create_all(bind=engine)

programs = [
    {
        "name": "예비창업패키지",
        "agency": "중소벤처기업부",
        "category": "창업",
        "target_stage": "예비창업",
        "trl_min": 1, "trl_max": 5,
        "budget_min": 5000, "budget_max": 10000,
        "deadline": "2025-03-31", "region": "전국"
    },
    {
        "name": "초기창업패키지",
        "agency": "중소벤처기업부",
        "category": "창업",
        "target_stage": "초기",
        "trl_min": 3, "trl_max": 6,
        "budget_min": 10000, "budget_max": 30000,
        "deadline": "2025-04-30", "region": "전국"
    },
    {
        "name": "TIPS",
        "agency": "중소벤처기업부",
        "category": "R&D",
        "target_stage": "초기",
        "trl_min": 4, "trl_max": 7,
        "budget_min": 50000, "budget_max": 100000,
        "deadline": "2025-05-31", "region": "전국"
    },
    {
        "name": "소부장 강소기업",
        "agency": "산업통상자원부",
        "category": "R&D",
        "target_stage": "성장",
        "trl_min": 5, "trl_max": 8,
        "budget_min": 100000, "budget_max": 500000,
        "deadline": "2025-06-30", "region": "전국"
    },
    {
        "name": "디딤돌 창업과제",
        "agency": "중소벤처기업부",
        "category": "R&D",
        "target_stage": "초기",
        "trl_min": 2, "trl_max": 5,
        "budget_min": 5000, "budget_max": 15000,
        "deadline": "2025-04-15", "region": "전국"
    },
    {
        "name": "대구테크노파크 지역특화",
        "agency": "대구테크노파크",
        "category": "사업화",
        "target_stage": "초기",
        "trl_min": 4, "trl_max": 7,
        "budget_min": 5000, "budget_max": 20000,
        "deadline": "2025-05-15", "region": "대구"
    },
    {
        "name": "스케일업 팁스",
        "agency": "중소벤처기업부",
        "category": "R&D",
        "target_stage": "성장",
        "trl_min": 6, "trl_max": 9,
        "budget_min": 100000, "budget_max": 200000,
        "deadline": "2025-07-31", "region": "전국"
    },
    {
        "name": "산업부 R&D 기술개발",
        "agency": "산업통상자원부",
        "category": "R&D",
        "target_stage": "성장",
        "trl_min": 5, "trl_max": 9,
        "budget_min": 200000, "budget_max": 1000000,
        "deadline": "2025-08-31", "region": "전국"
    }
]

def seed():
    db = SessionLocal()
    try:
        existing = db.query(Program).count()
        if existing > 0:
            print(f"이미 {existing}개의 사업 데이터가 있습니다.")
            return
        for p in programs:
            program = Program(**p)
            db.add(program)
        db.commit()
        print(f"✅ {len(programs)}개 지원사업 데이터 입력 완료")
    finally:
        db.close()

if __name__ == "__main__":
    seed()