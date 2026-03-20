# code-review - PR/코드 리뷰 자동화 플러그인

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2026-01-23 | 초기 작성 |

---

## 1. 개요

| 항목 | 내용 |
|------|------|
| 플러그인명 | code-review |
| 역할 | PR/코드 리뷰 자동화 |
| 제공자 | claude-plugins-official |

Pull Request 및 코드 변경사항을 자동으로 분석하여 리뷰를 제공하는 플러그인입니다.

---

## 2. 설치

```bash
/plugin install code-review@claude-plugins-official
```

---

## 3. 주요 기능

| 기능 | 설명 |
|------|------|
| PR 분석 | Pull Request의 변경사항 분석 |
| 코드 품질 검토 | 코드 품질, 가독성, 유지보수성 검토 |
| 보안 취약점 탐지 | 잠재적 보안 이슈 식별 |
| 개선 제안 | 코드 개선 방안 제안 |
| 커밋 메시지 검토 | 커밋 메시지 품질 평가 |

---

## 4. 사용법

### 4.1 PR 리뷰

```bash
# 현재 브랜치의 변경사항 리뷰
/code-review

# 특정 PR 리뷰 (GitHub)
/code-review PR#123
```

### 4.2 파일 리뷰

```bash
# 특정 파일 리뷰
/code-review src/main.py
```

---

## 5. 관련 문서

- `doc/commit-commands.md` - Git 커밋 메시지 생성 플러그인
- `v/oaisenv.md` - 환경 점검 스킬
