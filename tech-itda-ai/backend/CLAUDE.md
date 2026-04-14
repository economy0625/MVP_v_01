# Backend — API 서버 구조

## 목적
테크잇다AI 플랫폼의 핵심 도메인 로직을 REST API로 제공한다.
MVP 단계에서는 단순하고 빠른 구현을 우선한다.

---

## 기술 스택 (MVP)

| 구분 | 기술 |
|------|------|
| 언어 | Python 3.11 |
| 프레임워크 | FastAPI |
| DB | PostgreSQL |
| ORM | SQLAlchemy |
| LLM 연동 | Anthropic Claude API |
| 배포 | Docker + AWS EC2 |

---

## API 엔드포인트 구조

### 기업 (Company)
```
POST   /api/companies          기업 정보 등록
GET    /api/companies/{id}     기업 조회
PUT    /api/companies/{id}     기업 정보 수정
```

### 추천 (Recommendation)
```
POST   /api/recommend          지원사업 추천 실행
GET    /api/recommend/{id}     추천 결과 조회
```

### 점수 (Scoring)
```
POST   /api/score              선정 확률 계산
GET    /api/score/{id}         점수 결과 조회
```

### KPI
```
POST   /api/kpi/generate       KPI 자동 생성
POST   /api/kpi/validate       물리 검증 실행
GET    /api/kpi/{id}           KPI 조회
```

### 계획서 (Planning)
```
POST   /api/plan/generate      계획서 초안 생성
GET    /api/plan/{id}          계획서 조회
PUT    /api/plan/{id}          계획서 수정
```

### 전문가 (Expert)
```
GET    /api/experts            전문가 목록 조회
POST   /api/experts/match      전문가 매칭 요청
GET    /api/experts/{id}       전문가 프로필 조회
```

---

## 응답 공통 형식

```json
{
  "success": true,
  "data": {},
  "error": null,
  "timestamp": "2025-01-01T00:00:00Z"
}
```

---

## 개발 원칙

1. 각 도메인 로직은 domain/ 폴더에서 처리, API는 라우팅만 담당
2. LLM 호출은 비동기(async) 처리
3. 에러는 반드시 로깅 + 사용자 친화적 메시지 반환
4. MVP에서는 인증 단순화 (JWT 기본)

---

## Claude 작업 규칙

- API 추가/수정 시 반드시 api_spec.md 업데이트
- DB 스키마 변경 시 database_schema.md 수정 후 마이그레이션
- 새 엔드포인트는 domain/ 로직 먼저 완성 후 연결
- MVP 범위 외 엔드포인트 추가 금지
