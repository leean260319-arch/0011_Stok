# commit-commands - Git 커밋 메시지 생성 플러그인

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2026-01-23 | 초기 작성 |

---

## 1. 개요

| 항목 | 내용 |
|------|------|
| 플러그인명 | commit-commands |
| 역할 | Git 커밋 메시지 생성 |
| 제공자 | claude-plugins-official |

변경사항을 분석하여 Conventional Commits 형식의 커밋 메시지를 자동 생성하는 플러그인입니다.

---

## 2. 설치

```bash
/plugin install commit-commands@claude-plugins-official
```

---

## 3. 주요 기능

| 기능 | 설명 |
|------|------|
| 커밋 메시지 생성 | 변경사항 기반 커밋 메시지 자동 생성 |
| Conventional Commits | feat, fix, docs, style 등 표준 형식 지원 |
| 다국어 지원 | 한국어/영어 커밋 메시지 생성 |
| 변경사항 요약 | 변경 파일 및 내용 요약 |

---

## 4. 사용법

### 4.1 커밋 생성

```bash
# 변경사항 커밋 (메시지 자동 생성)
/commit

# 메시지 지정 커밋
/commit -m "feat: 새 기능 추가"
```

### 4.2 커밋 + 푸시

```bash
/commit-push-pr
```

---

## 5. 커밋 메시지 형식

```
<type>(<scope>): <subject>

<body>

<footer>
```

| Type | 설명 |
|------|------|
| feat | 새로운 기능 |
| fix | 버그 수정 |
| docs | 문서 변경 |
| style | 코드 포맷팅 |
| refactor | 리팩토링 |
| test | 테스트 추가/수정 |
| chore | 빌드, 설정 변경 |

---

## 6. 관련 문서

- `doc/code-review.md` - PR/코드 리뷰 자동화 플러그인
- `v/oaiscommit.md` - 커밋 스킬
