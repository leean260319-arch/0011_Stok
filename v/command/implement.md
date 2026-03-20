# implement - 기능 구현

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2024-12-25 | 최초 생성 (sg/sc 통합) |
| v02 | 2025-01-25 | sc:implement 상세 내용 통합 |
| v03 | 2026-01-25 | 태스크 유형별 전략, 진행 추적, 복구 패턴 추가 (tm 통합) |

---

## 1. 개요

지능적인 페르소나 활성화 및 MCP 통합을 통해 기능 및 코드를 구현합니다.

## 2. 사용법

```
implement [feature-description] [--type component|api|service|feature] [--framework <name>] [--safe]
```

## 3. 인자 및 옵션

| 인자/옵션 | 설명 |
|-----------|------|
| `feature-description` | 구현할 기능 설명 |
| `--type` | 구현 유형 (component, api, service, feature, module) |
| `--framework` | 사용할 프레임워크 지정 |
| `--safe` | 보수적 구현 접근법 사용 |
| `--iterative` | 검증 단계 포함 반복 개발 활성화 |
| `--with-tests` | 테스트 구현 포함 |
| `--documentation` | 구현과 함께 문서 생성 |
| `--tdd` | 테스트 주도 개발 모드 |
| `--incremental` | 점진적 구현 모드 |

## 4. 실행 단계

1. 구현 요구사항 분석 및 기술 컨텍스트 감지
2. 관련 페르소나 자동 활성화 (frontend, backend, security 등)
3. MCP 서버 조율 (Magic-UI, Context7-패턴, Sequential-복잡한 로직)
4. 베스트 프랙티스를 적용한 구현 코드 생성
5. 보안 및 품질 검증 적용
6. 테스트 권장사항 및 다음 단계 제공

## 5. 페르소나 자동 활성화 패턴

| 패턴 | 활성화 페르소나 |
|------|----------------|
| UI 컴포넌트, React/Vue/Angular | **frontend** |
| API, 서비스, DB 통합 | **backend** |
| 인증, 권한, 데이터 보호 | **security** |
| 시스템 설계, 모듈 구조 | **architect** |
| 최적화, 확장성 | **performance** |

## 6. MCP 서버 통합

| 서버 | 용도 |
|------|------|
| **Magic** | UI 컴포넌트 생성 및 디자인 시스템 |
| **Context7** | 프레임워크 패턴 및 라이브러리 문서 |
| **Sequential** | 복잡한 로직 및 다단계 구현 |

## 7. 도구 연동

### Claude
- **allowed-tools**: Read, Write, Edit, MultiEdit, Bash, Glob, TodoWrite, Task

### MCP 플래그
- `--c7`: Context7 활성화
- `--magic`: Magic 활성화
- `--seq`: Sequential 활성화

## 8. 사용 예시

```bash
# 사용자 인증 시스템 구현 (테스트 포함)
implement "사용자 인증 시스템" --type feature --with-tests

# React 대시보드 컴포넌트 구현
implement "대시보드 컴포넌트" --type component --framework react

# 사용자 관리 REST API 구현 (안전 모드)
implement "REST API for user management" --type api --safe

# 결제 처리 서비스 구현 (반복적)
implement "결제 처리 서비스" --type service --iterative
```

## 9. 태스크 유형별 전략

### Feature 태스크
1. 기존 패턴 리서치
2. 컴포넌트 아키텍처 설계
3. 테스트와 함께 구현
4. 시스템 통합
5. 문서 업데이트

### Bug Fix 태스크
1. 이슈 재현
2. 근본 원인 식별
3. 최소 수정 구현
4. 회귀 테스트 추가
5. 부작용 검증

### Refactoring 태스크
1. 현재 구조 분석
2. 점진적 변경 계획
3. 테스트 커버리지 유지
4. 단계별 리팩토링
5. 동작 불변 검증

## 10. 진행 상태 추적

```
Step 1/5: 컴포넌트 구조 설정 ✓
Step 2/5: 핵심 로직 구현 ✓
Step 3/5: 에러 핸들링 추가 ⚡ (진행 중)
Step 4/5: 테스트 작성 ⏳
Step 5/5: 통합 테스트 ⏳
```

### 품질 체크
- 린팅 및 포맷팅
- 테스트 실행
- 타입 체크
- 의존성 검증
- 성능 분석

## 11. 복구 패턴

| 상황 | 대응 |
|------|------|
| 구현 막힘 | 진단 분석 → 대안 제안 |
| 테스트 실패 | 근본 원인 분석 → 수정 |
| 의존성 충돌 | 버전 조정 → 대체 라이브러리 |
| 성능 문제 | 프로파일링 → 최적화 |

## 12. 구현 후 체크리스트

- [ ] PR 설명 생성
- [ ] 문서 업데이트
- [ ] 학습 내용 기록
- [ ] 후속 태스크 제안
- [ ] 태스크 관계 업데이트

## 13. 관련 스킬

- `v/oaisfix.md` - 코드 오류 자동 개선
- `v/oaistest.md` - 테스트 시나리오 작성
- `v/oaisdev.md` - TDD 개발

---
