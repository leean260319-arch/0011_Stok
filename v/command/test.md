# test - 테스트 실행

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2025-12-25 | 최초 생성 (sg/sc 통합) |
| v02 | 2026-01-25 | 테스트 생성, 프레임워크별 가이드, 베스트 프랙티스 추가 |

---

## 1. 개요

테스트를 실행하고, 테스트 리포트를 생성하며, 테스트 커버리지를 유지합니다.

## 2. 사용법

```
test [type] [--coverage] [--watch] [--filter <pattern>]
```

## 3. 인자 및 옵션

| 인자/옵션 | 설명 |
|-----------|------|
| `type` | 테스트 유형 (unit, integration, e2e, all) |
| `--coverage` | 커버리지 리포트 생성 |
| `--watch` | 파일 변경 감시 모드 |
| `--filter` | 테스트 필터 패턴 |
| `--parallel` | 병렬 테스트 실행 |
| `--verbose` | 상세 출력 |

## 4. 실행 단계

1. 테스트 환경 설정 확인
2. 테스트 대상 파일 탐색
3. 테스트 프레임워크 감지 및 실행
4. 결과 수집 및 분석
5. 커버리지 리포트 생성 (옵션)
6. 실패 테스트 상세 보고

## 5. 도구 연동

### Claude
- **allowed-tools**: Bash, Read, Glob, TodoWrite

### Gemini
- **MCP 플래그**: --seq, --c7, --verbose, --quiet

## 6. 테스트 생성 (generate)

### 사용법
```bash
test generate [file-path|component-name]
```

### 생성 프로세스
1. 대상 파일/컴포넌트 구조 분석
2. 테스트 가능한 함수, 메서드, 동작 식별
3. 프로젝트 내 기존 테스트 패턴 조사
4. 프로젝트 명명 규칙에 따른 테스트 파일 생성
5. setup/teardown 포함 테스트 케이스 구현
6. 필요한 mock 및 유틸리티 추가

### 테스트 유형

**Unit Tests**:
- 다양한 입력으로 개별 함수 테스트
- 컴포넌트 렌더링 및 prop 처리
- 상태 관리 및 라이프사이클 메서드
- 유틸리티 함수 엣지 케이스

**Integration Tests**:
- 컴포넌트 상호작용 테스트
- Mock 응답 기반 API 통합
- 서비스 레이어 통합
- E2E 사용자 워크플로우

## 7. 프레임워크별 가이드

### Python (pytest)
```bash
uv run pytest tests/ -v
uv run pytest --cov=src --cov-report=html
uv run pytest -k "test_user"
```

### JavaScript/TypeScript (Jest/Vitest)
```bash
npm run test
npm run test:coverage
npm run test -- --watch
```

### 프레임워크별 테스트
| 프레임워크 | 도구 |
|-----------|------|
| React | React Testing Library |
| Vue | Vue Test Utils |
| Angular | TestBed |
| Node.js | Supertest (API) |

## 8. 베스트 프랙티스

### 테스트 구조
- 동작을 설명하는 명확한 테스트명
- AAA 패턴 (Arrange, Act, Assert)
- describe 블록으로 관련 테스트 그룹화
- 테스트 격리를 위한 setup/teardown

### Mock 전략
- 외부 의존성 및 API 호출 mock
- 테스트 데이터 생성용 factory 사용
- 비동기 작업 적절한 cleanup
- 결정적 테스트를 위한 타이머/날짜 mock

### 커버리지 목표
| 영역 | 목표 |
|------|------|
| 전체 코드 | 80%+ |
| 핵심 비즈니스 로직 | 100% |
| 에러 시나리오 | 90%+ |
| 경계값 테스트 | 필수 |

## 9. 관련 스킬

- `v/oaistest.md` - 통합 테스트 가이드
- `v/oaischeck.md` - 코드 에러 체크
- `v/oaisdev.md` - TDD 개발

---
