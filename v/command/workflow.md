# workflow - 워크플로우 생성

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2024-12-25 | 최초 생성 (sg/sc 통합) |
| v02 | 2025-01-25 | sc:workflow 상세 내용 통합 |
| v03 | 2026-01-25 | 컨텍스트 인식 자동 선택, 학습 모드 추가 (tm 통합) |

---

## 1. 개요

PRD 및 기능 요구사항으로부터 전문가 가이드와 함께 구조화된 구현 워크플로우를 생성합니다.

## 2. 사용법

```
workflow [prd-file|feature-description] [--persona expert] [--strategy systematic|agile|mvp] [--output roadmap|tasks|detailed]
```

## 3. 인자 및 옵션

| 인자/옵션 | 설명 |
|-----------|------|
| `prd-file` | PRD 파일 경로 또는 기능 설명 |
| `--persona` | 전문가 페르소나 지정 (architect, frontend, backend, security, devops) |
| `--strategy` | 워크플로우 전략 (systematic, agile, mvp) |
| `--output` | 출력 형식 (roadmap, tasks, detailed) |
| `--estimate` | 시간 및 복잡도 추정 포함 |
| `--dependencies` | 외부 의존성 및 통합 매핑 |
| `--risks` | 리스크 평가 및 완화 전략 포함 |
| `--parallel` | 병렬화 가능한 작업 스트림 식별 |
| `--milestones` | 마일스톤 기반 프로젝트 단계 생성 |

## 4. MCP 통합 플래그

| 플래그 | 용도 |
|--------|------|
| `--c7` | Context7 - 프레임워크 패턴 및 베스트 프랙티스 |
| `--sequential` | Sequential - 복잡한 다단계 분석 |
| `--magic` | Magic - UI 컴포넌트 워크플로우 계획 |
| `--all-mcp` | 모든 MCP 서버 활성화 |

## 5. 워크플로우 전략

### Systematic 전략 (기본)
1. **요구사항 분석**: PRD 구조 및 인수 기준 심층 분석
2. **아키텍처 계획**: 시스템 설계 및 컴포넌트 아키텍처
3. **의존성 매핑**: 내부/외부 의존성 식별
4. **구현 단계**: 명확한 산출물과 순차적 단계
5. **테스트 전략**: 각 단계별 포괄적 테스트 접근법
6. **배포 계획**: 프로덕션 롤아웃 및 모니터링 전략

### Agile 전략
1. **에픽 분해**: PRD를 사용자 스토리 및 에픽으로 변환
2. **스프린트 계획**: 반복 스프린트로 작업 구성
3. **MVP 정의**: 최소 실행 가능 제품 범위 식별
4. **반복 개발**: 지속적 전달 및 피드백 계획
5. **이해관계자 참여**: 정기적 검토 및 조정 주기
6. **회고 계획**: 내장된 개선 및 학습 주기

### MVP 전략
1. **핵심 기능 식별**: 필수 기능으로 축소
2. **빠른 프로토타이핑**: 신속한 검증 및 피드백에 집중
3. **기술 부채 계획**: 단기 해결책 및 향후 개선 식별
4. **검증 메트릭**: 성공 기준 및 측정 정의
5. **확장 로드맵**: MVP 후 기능 확장 계획
6. **사용자 피드백 통합**: 사용자 입력에 대한 구조화된 접근법

## 6. 전문가 페르소나 자동 활성화

### Frontend 워크플로우
- **UI/UX 분석**: 디자인 시스템 통합 및 컴포넌트 계획
- **상태 관리**: 데이터 흐름 및 상태 아키텍처
- **성능 최적화**: 번들 최적화 및 지연 로딩
- **접근성 준수**: WCAG 가이드라인 및 포용적 설계

### Backend 워크플로우
- **API 설계**: RESTful/GraphQL 엔드포인트 계획
- **데이터베이스 스키마**: 데이터 모델링 및 마이그레이션 전략
- **보안 구현**: 인증, 권한 부여 및 데이터 보호
- **성능 확장**: 캐싱, 최적화 및 부하 처리

### Architecture 워크플로우
- **시스템 설계**: 고수준 아키텍처 및 서비스 경계
- **기술 스택**: 프레임워크 및 도구 선택 근거
- **확장성 계획**: 성장 고려 및 병목 방지
- **DevOps 전략**: CI/CD 파이프라인 및 IaC

### Security 워크플로우
- **위협 모델링**: 보안 리스크 평가 및 공격 벡터
- **데이터 보호**: 암호화, 개인정보 보호 및 컴플라이언스
- **인증 전략**: 사용자 신원 및 접근 관리
- **보안 테스트**: 침투 테스트 및 취약점 평가

## 7. 출력 형식

### Roadmap 형식 (`--output roadmap`)
```
# 기능 구현 로드맵
## Phase 1: 기반 (1-2주)
- [ ] 아키텍처 설계 및 기술 선택
- [ ] 데이터베이스 스키마 설계 및 설정
- [ ] 기본 프로젝트 구조 및 CI/CD 파이프라인

## Phase 2: 핵심 구현 (3-6주)
- [ ] API 개발 및 인증
- [ ] 프론트엔드 컴포넌트 및 사용자 인터페이스
- [ ] 통합 테스트 및 보안 검증
```

### Tasks 형식 (`--output tasks`)
```
# 구현 태스크
## Epic: 사용자 인증 시스템
### Story: 사용자 등록
- [ ] 등록 폼 UI 컴포넌트 설계
- [ ] 백엔드 등록 API 구현
- [ ] 이메일 인증 워크플로우 추가
```

### Detailed 형식 (`--output detailed`)
```
# 상세 구현 워크플로우
## 태스크: 사용자 등록 API 구현
**페르소나**: Backend Developer
**예상 시간**: 8시간
**의존성**: 데이터베이스 스키마, 인증 서비스

### 구현 단계:
1. **API 엔드포인트 설정** (1시간)
2. **데이터베이스 통합** (2시간)
3. **보안 조치** (3시간)
4. **테스트** (2시간)
```

## 8. 고급 기능

### 의존성 분석
- **내부 의존성**: 컴포넌트 및 기능 간 결합 식별
- **외부 의존성**: 서드파티 서비스 및 API 매핑
- **기술 의존성**: 프레임워크 버전, 데이터베이스 요구사항
- **인프라 의존성**: 클라우드 서비스, 배포 요구사항

### 리스크 평가 및 완화
- **기술 리스크**: 복잡성, 성능 및 확장성 우려
- **일정 리스크**: 의존성 병목 및 리소스 제약
- **보안 리스크**: 데이터 보호 및 컴플라이언스 취약점
- **완화 전략**: 대체 계획 및 대안 접근법

### 병렬 작업 스트림 식별
- **독립 컴포넌트**: 동시 개발 가능한 기능
- **공유 의존성**: 조정이 필요한 공통 컴포넌트
- **크리티컬 패스 분석**: 다른 작업을 차단하는 병목

## 9. 도구 연동

### Claude
- **allowed-tools**: Read, Write, Edit, Glob, Grep, TodoWrite, Task, mcp__sequential-thinking__sequentialthinking, mcp__context7__context7

### 페르소나 통합
- architect, analyzer, frontend, backend, security, devops, project-manager

### MCP 서버
- Sequential, Context7, Magic

## 10. 사용 예시

```bash
# PRD 파일에서 워크플로우 생성
workflow docs/feature-100-prd.md --strategy systematic --c7 --sequential --estimate

# 프론트엔드 중심 워크플로우 생성
workflow "실시간 분석 대시보드" --persona frontend --magic --output detailed

# 리스크 평가 포함 MVP 계획
workflow user-authentication-system --strategy mvp --risks --parallel --milestones

# 의존성 포함 백엔드 API 워크플로우
workflow payment-processing-api --persona backend --dependencies --c7 --output tasks
```

## 11. 품질 게이트

### 워크플로우 완성도 확인
- **요구사항 커버리지**: 모든 PRD 요구사항 반영 확인
- **인수 기준**: 테스트 가능한 성공 기준 검증
- **기술 타당성**: 구현 복잡성 및 리스크 평가
- **리소스 정렬**: 팀 역량 및 일정과 워크플로우 매칭

### 성공 메트릭
| 메트릭 | 목표 |
|--------|------|
| 구현 성공률 | >90% |
| 일정 정확도 | <20% 오차 |
| 요구사항 커버리지 | 100% |
| 워크플로우 생성 시간 | <30초 |

## 12. 컨텍스트 인식 자동 선택

### 이전 명령어 기반 추천

| 이전 명령어 | 추천 워크플로우 |
|------------|----------------|
| `status` | Daily standup 시작 |
| `complete` | 다음 태스크 찾기 |
| `list pending` | Sprint planning |
| `expand` | Complexity analysis |
| `init` | Onboarding workflow |

### 상황 기반 자동 선택

| 상황 | 추천 |
|------|------|
| 아침 시간 | Daily standup |
| 대기 태스크 다수 | Sprint planning |
| 블로킹 태스크 존재 | Dependency resolution |
| 금요일 | Weekly review |

### 워크플로우 체이닝

```
1. 현재 상태 분석
2. 주요 워크플로우 실행
3. 후속 액션 제안
4. 코딩 환경 준비
```

## 13. 학습 모드

### 패턴 트래킹
- 명령어 시퀀스 기록
- 시간대별 선호도 분석
- 일반적인 워크플로우 기억
- 사용자 스타일 적응

### 감지된 플로우 예시
```
아침: standup → next → start
점심 후: status → continue task
하루 끝: complete → commit → status
```

## 14. 관련 스킬

- `v/oaisplan.md` - 구현 계획 생성
- `v/oaisprd.md` - PRD 문서 생성
- `v/oaisdev.md` - 개발 워크플로우

---
