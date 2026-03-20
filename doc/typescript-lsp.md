# typescript-lsp - TypeScript 언어 서버 플러그인

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2026-01-23 | 초기 작성 |

---

## 1. 개요

| 항목 | 내용 |
|------|------|
| 플러그인명 | typescript-lsp |
| 역할 | TypeScript 언어 서버 |
| 제공자 | claude-plugins-official |

TypeScript Language Server Protocol을 활용한 고급 코드 분석 및 편집을 지원하는 플러그인입니다.

---

## 2. 설치

```bash
/plugin install typescript-lsp@claude-plugins-official
```

---

## 3. 주요 기능

| 기능 | 설명 |
|------|------|
| 타입 체크 | 실시간 TypeScript 타입 검증 |
| 자동 완성 | 컨텍스트 기반 코드 자동 완성 |
| 정의 이동 | 심볼 정의로 이동 |
| 참조 찾기 | 심볼 사용처 검색 |
| 리팩토링 | 이름 변경, 추출 등 리팩토링 |
| 진단 | 오류/경고 진단 |

---

## 4. 사용법

### 4.1 타입 체크

```bash
# 프로젝트 타입 체크
/typescript-lsp check

# 특정 파일 타입 체크
/typescript-lsp check src/index.ts
```

### 4.2 진단 조회

```bash
# 현재 파일 진단
/typescript-lsp diagnostics
```

---

## 5. LSP 기능 목록

| 기능 | 설명 |
|------|------|
| textDocument/completion | 자동 완성 |
| textDocument/hover | 호버 정보 |
| textDocument/definition | 정의로 이동 |
| textDocument/references | 참조 찾기 |
| textDocument/rename | 이름 변경 |
| textDocument/formatting | 코드 포맷팅 |

---

## 6. 지원 파일 형식

| 확장자 | 지원 |
|--------|------|
| .ts | Full |
| .tsx | Full |
| .js | Partial |
| .jsx | Partial |

---

## 7. 관련 문서

- `doc/pyright-lsp.md` - Python 타입 체크 플러그인
- `v/oaischeck.md` - 코드 품질 체크 스킬
