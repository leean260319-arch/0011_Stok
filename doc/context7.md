# context7 - 라이브러리 문서 조회 플러그인

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2026-01-23 | 초기 작성 |

---

## 1. 개요

| 항목 | 내용 |
|------|------|
| 플러그인명 | context7 |
| 역할 | 라이브러리 문서 조회 |
| 제공자 | claude-plugins-official |

외부 라이브러리/프레임워크의 공식 문서를 실시간으로 조회하여 최신 API 정보를 제공하는 플러그인입니다.

---

## 2. 설치

```bash
/plugin install context7@claude-plugins-official
```

---

## 3. 주요 기능

| 기능 | 설명 |
|------|------|
| 문서 조회 | 라이브러리 공식 문서 실시간 조회 |
| API 레퍼런스 | 함수, 클래스, 메서드 정보 제공 |
| 버전별 문서 | 특정 버전 문서 조회 가능 |
| 예제 코드 | 공식 예제 코드 제공 |
| 마이그레이션 가이드 | 버전 업그레이드 가이드 |

---

## 4. 사용법

### 4.1 문서 조회

```bash
# React 문서 조회
use context7 for React hooks

# pandas 특정 함수 조회
use context7 for pandas DataFrame.merge
```

### 4.2 MCP 서버 연동

context7-mcp 서버가 설치된 경우 자동으로 MCP 도구 사용:

```
mcp__context7__resolve_library_id
mcp__context7__get_library_docs
```

---

## 5. 지원 라이브러리

| 카테고리 | 라이브러리 |
|---------|-----------|
| JavaScript | React, Vue, Angular, Node.js |
| Python | pandas, numpy, Django, FastAPI |
| Database | PostgreSQL, MongoDB, Redis |
| Cloud | AWS, GCP, Azure |

---

## 6. 관련 문서

- `.mcp.json` - MCP 서버 설정 (context7-mcp)
- `v/oaisenv.md` - 환경 점검 스킬
