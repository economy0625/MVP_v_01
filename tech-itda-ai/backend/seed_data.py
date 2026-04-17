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

    from models import Expert

experts = [
    {
        "name": "김철수 박사",
        "grade": "넥서스인증",
        "fields": "소재,경량화,자동차부품",
        "programs": "소부장,산업부R&D,TIPS",
        "rating": 4.9,
        "location": "대구",
        "career": "POSTECH 소재공학 박사. 경량화 소재 분야 20년 경력. 소부장 과제 10건 수행.",
        "available": "가능"
    },
    {
        "name": "이영희 박사",
        "grade": "넥서스인증",
        "fields": "ICT,스마트팩토리,AI",
        "programs": "TIPS,초기창업패키지,디딤돌",
        "rating": 4.8,
        "location": "서울",
        "career": "KAIST 전산학 박사. 스마트팩토리 AI 솔루션 전문. 창업 경험 2회.",
        "available": "가능"
    },
    {
        "name": "박민준 박사",
        "grade": "넥서스인증",
        "fields": "화학,에너지,바이오",
        "programs": "산업부R&D,소부장,스케일업",
        "rating": 4.7,
        "location": "대구",
        "career": "서울대 화학공학 박사. 에너지 효율화 전문. 특허 15건 보유.",
        "available": "가능"
    },
    {
        "name": "최지훈 박사",
        "grade": "골드",
        "fields": "제조업,생산성,품질관리",
        "programs": "예비창업패키지,초기창업패키지,TIPS",
        "rating": 4.6,
        "location": "경북",
        "career": "연세대 산업공학 박사. 제조 공정 최적화 전문. 중소기업 컨설팅 200건.",
        "available": "가능"
    },
    {
        "name": "정수연 박사",
        "grade": "골드",
        "fields": "전자전기,반도체,센서",
        "programs": "소부장,산업부R&D,스케일업",
        "rating": 4.5,
        "location": "서울",
        "career": "성균관대 전자공학 박사. 반도체 센서 분야 15년 경력. 기술이전 5건.",
        "available": "가능"
    },
]

def seed_experts():
    db = SessionLocal()
    try:
        existing = db.query(Expert).count()
        if existing > 0:
            print(f"이미 {existing}명의 전문가 데이터가 있습니다.")
            return
        for e in experts:
            expert = Expert(**e)
            db.add(expert)
        db.commit()
        print(f"✅ {len(experts)}명 전문가 데이터 입력 완료")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
    seed_experts()