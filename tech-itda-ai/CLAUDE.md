# Tech-Itda AI — 루트 프로젝트 지도

## 1. 프로젝트 목적
테크잇다AI는 제조기업의 정부지원사업 선정 가능성을 높이기 위한 AI 기반 의사결정 플랫폼이다.
"물리 법칙을 아는 AI가 계획서를 써준다"는 메시지로 예비창업패키지 합격 및 초기 기업 고객을 확보한다.

핵심 기능 (우선순위 순):
1. 지원사업 추천 및 알림
2. 선정 확률 예측
3. KPI 자동 생성 + 물리 검증 (특허 핵심)
4. 사업계획서 초안 생성
5. 전문가(넥서스) 연결

---

## 2. MVP 범위 (Phase 1 — 출시~3개월)

포함:
- 기업 정보 입력
- 지원사업 추천 (Rule 기반)
- 선정 확률 예측 (scoring 기반)
- KPI 자동 생성 + 물리 모델 검증
- 사업계획서 초안 생성 (LLM 기반)

제외 (Phase 2 이후):
- 자동 크롤링
- MES / 센서 데이터 연동
- ML 기반 예측 모델 고도화
- 정산 증빙 자동화
- R&D PMS 수행 관리

---

## 3. 전체 서비스 플로우

```
기업 입력 → 지원사업 추천 → 선정 확률 예측 → KPI 생성 → 계획서 초안 → 전문가 연결
```

단계별 담당 도메인:
| 단계 | 도메인 폴더 |
|------|------------|
| 기업 입력 | data/ |
| 추천 | domain/recommendation/ |
| 확률 예측 | domain/scoring/ |
| KPI 생성 | domain/kpi/ |
| 계획서 초안 | domain/planning/ |
| 전문가 연결 | domain/expert/ |

---

## 4. 개발 원칙

1. 복잡한 AI보다 Rule 기반 우선 (초기 단계)
2. 빠른 실행이 정확성보다 중요
3. 모든 로직은 explainable 해야 함
4. 사용자 입력은 최소화
5. ML 모델 도입 금지 (MVP 단계)

---

## 5. 로드맵

| Phase | 기간 | 핵심 기능 |
|-------|------|----------|
| Phase 1 (MVP) | 0~3개월 | KPI 생성 + 물리검증 + 계획서 초안 |
| Phase 2 | 3~9개월 | 전문가 매칭 + 선정 확률 고도화 |
| Phase 3 | 9개월~ | R&D PMS + 정산 증빙 + SaaS 구독 |

---

## 6. Claude 작업 규칙

- 변경 전 반드시 해당 도메인 CLAUDE.md 먼저 확인
- 새로운 기능은 domain/ 폴더 기준으로 추가
- 로직 수정 시 해당 domain/CLAUDE.md 업데이트 필수
- API 변경 시 backend/api_spec.md 반드시 수정
- MVP 범위를 벗어난 기능 추가 금지
- 과도한 추상화 금지

---

## 7. 핵심 파일 맵

```
/CLAUDE.md                          ← 지금 이 파일 (전체 지도)
/domain/recommendation/CLAUDE.md   ← 추천 엔진 핵심 로직
/domain/scoring/CLAUDE.md          ← 점수·확률 계산 엔진
/domain/kpi/CLAUDE.md              ← KPI 생성 + 물리검증 (특허)
/domain/planning/CLAUDE.md         ← 계획서 초안 생성
/domain/expert/CLAUDE.md           ← 전문가 매칭
/backend/CLAUDE.md                 ← API 구조
/data/CLAUDE.md                    ← 데이터 스키마
```
