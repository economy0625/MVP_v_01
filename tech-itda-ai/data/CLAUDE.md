# Data — 데이터 스키마 정의

## 목적
테크잇다AI 플랫폼의 핵심 데이터 구조를 정의한다.
모든 도메인 로직의 입력/출력은 이 스키마를 기준으로 동작한다.

---

## 핵심 엔티티 3개

### 1. Company (기업)
```
id              UUID
name            기업명
industry        업종 (KSIC 코드)
company_stage   단계: 예비창업 / 초기 / 성장 / 중견
tech_level      TRL: 1~9
revenue         연매출 (만원)
employee_count  직원 수
certs           보유 인증 목록 (배열)
location        지역
prior_rd_count  R&D 수행 이력 건수
created_at      등록일
```

### 2. Program (지원사업)
```
id              UUID
name            사업명
agency          주관기관
category        유형: 창업 / R&D / 사업화 / 실증
target_stage    대상 기업 단계
trl_range       적합 TRL 범위
budget_min      최소 지원금
budget_max      최대 지원금
deadline        접수 마감일
eval_criteria   평가 항목 (JSON)
region          지역 제한 (없으면 전국)
```

### 3. Application (지원 신청)
```
id              UUID
company_id      기업 FK
program_id      사업 FK
score           선정 확률 점수
kpis            생성된 KPI 목록 (JSON)
plan_draft      계획서 초안 (TEXT)
expert_id       매칭 전문가 FK (nullable)
status          진행 상태: draft / submitted / selected / rejected
created_at      생성일
```

---

## 데이터 입력 최소 요구 항목

기업 온보딩 시 필수 입력 (5개):
1. 기업명
2. 업종
3. 기업 단계
4. TRL 수준
5. 지역

→ 나머지는 선택 입력 (점수 향상에 활용)

---

## 샘플 데이터 위치

- `sample_data.md` → 기업 3개사, 사업 5개, 신청 예시 포함
- 테스트 시 반드시 샘플 데이터 기준으로 검증

---

## Claude 작업 규칙

- 스키마 변경 시 반드시 company_schema.md / program_schema.md 수정
- 필드 추가 시 backend/database_schema.md 마이그레이션 항목 추가
- 스키마와 실제 DB 구조 항상 동기화 유지
- MVP에서 불필요한 필드 추가 금지 (최소화 원칙)
