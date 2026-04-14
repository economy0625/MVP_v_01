# Frontend — UI 구조

## 목적
기업 사용자가 최소한의 입력으로 추천, 확률, KPI, 계획서까지
끊김 없이 흐르는 UX를 제공한다.

---

## 기술 스택 (MVP)

| 구분 | 기술 |
|------|------|
| 프레임워크 | Next.js 14 (App Router) |
| 스타일 | Tailwind CSS |
| 상태 관리 | Zustand |
| API 통신 | Axios |
| 배포 | Vercel |

---

## 핵심 페이지 구조

```
/                          랜딩 페이지
/onboarding                기업 정보 입력 (최소 5개 항목)
/recommend                 지원사업 추천 결과
/score                     선정 확률 대시보드
/kpi                       KPI 생성 + 물리검증 결과
/plan                      사업계획서 초안 편집기
/expert                    전문가 매칭 요청
/dashboard                 전체 현황 대시보드
```

---

## 핵심 UX 원칙

1. 사용자 입력 최소화 → 단계별 입력, 자동완성 최대화
2. 결과는 즉시 시각화 (로딩 스피너 → 결과 카드)
3. 각 단계에서 "다음 단계" 유도 CTA 명확히 배치
4. 선정 확률은 게이지 차트로 직관적 표현
5. 모바일 반응형 필수 (대표 사용 환경 고려)

---

## 핵심 컴포넌트

| 컴포넌트 | 역할 |
|----------|------|
| CompanyForm | 기업 정보 입력 폼 |
| ProgramCard | 추천 사업 카드 |
| ScoreGauge | 선정 확률 게이지 |
| KpiTable | KPI 목록 + 물리검증 결과 |
| PlanEditor | 계획서 WYSIWYG 편집기 |
| ExpertCard | 전문가 프로필 카드 |

---

## Claude 작업 규칙

- 새 페이지 추가 시 wireframe.md에 와이어프레임 먼저 작성
- 컴포넌트 추가 시 components.md 업데이트
- 백엔드 API 변경 연동 시 backend/api_spec.md 확인 후 수정
- MVP에서는 디자인 완성도보다 기능 작동 우선
