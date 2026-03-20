# a0009_script.md - OAIS 스크립트 가이드

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2025-01-25 | 최초 생성 - oais 스킬 docstring 통합 |

---

## 1. 개요

OAIS(Orchestrated AI Skills) 스크립트는 `v/script/oais*_run.py` 형태로 구현된 자동화 스킬입니다.
이 문서는 각 스킬의 상세 사용법을 정리합니다.

---

## 2. 공통 모듈 (oais_common.py)

### 2.1 공통 import

```python
from oais_common import (
    # 경로 상수
    PROJECT_ROOT, DOC_DIR, TMP_DIR, DATA_DIR,
    TODO_FILE, HISTORY_FILE, PRD_FILE,
    # 로깅 함수
    get_logger, log_info, log_ok, log_warn, log_error, log_tip, log_dry_run,
    # 유틸리티
    show_help_if_no_args, ensure_dir, get_timestamp, get_date,
)
```

### 2.2 로깅 사용법

```python
# 간단한 출력 함수
log_info("처리 중...")
log_ok("완료")
log_warn("경고 메시지")
log_error("에러 발생")
log_tip("권장 사항")
log_dry_run("미리보기 모드")

# 로거 사용 (세밀한 제어)
logger = get_logger("oaischeck", verbose=True)
logger.debug("디버그 정보")
logger.info("정보")
logger.warning("경고")
logger.error("에러")
```

---

## 3. 스킬별 상세 가이드

### 3.1 oaisstart - 세션 시작 워크플로우

```
명령어:
    oaisstart run    세션 시작 체크리스트 출력

기능:
- v/guide/common_guide.md 로딩 확인
- 핵심 문서 상태 체크 (d0001_prd, d0004_todo, d0010_history)
- 동기화 체크리스트 제공
- 세션 준비 완료 템플릿 제공
```

### 3.2 oaisstop - 세션 종료 워크플로우

```
명령어:
    oaisstop run        2단계 종료 워크플로우 실행 (기본)
    oaisstop readme     README.md 업데이트만 수행 (1단계)
    oaisstop sync       doc/*.md 동기화만 수행 (2단계)

옵션:
    --dry-run           실제 파일 수정 없이 미리보기
    --no-commit         자동 커밋 생략
    --message [msg]     작업 내역 메시지 지정
```

### 3.3 oaischeck - 코드 분석 및 이슈 등록

```
명령어:
    oaischeck run           전체 코드 분석 실행
    oaischeck update        분석 결과를 d0004_todo.md에 반영
    oaischeck status        현재 이슈 현황 조회

옵션:
    --dry-run              미리보기만
    --scope [file|module]  분석 범위 지정
```

### 3.4 oaisfix - 이슈 수정 워크플로우

```
명령어:
    oaisfix run             d0004_todo.md 기반 자동 수정
    oaisfix status          수정 대상 이슈 조회
    oaisfix apply [id]      특정 이슈 수정 적용

옵션:
    --dry-run              미리보기만
    --priority [level]     우선순위 필터 (CRITICAL, ERROR, WARNING, INFO)
```

### 3.5 oaishistory - 변경 이력 관리

```
명령어:
    oaishistory run              이력 현황 조회 (기본)
    oaishistory run [태그] [제목] 이력 항목 추가
    oaishistory list             최근 이력 조회 (최근 10건)
    oaishistory create           d0010_history.md 신규 생성
    oaishistory search [키워드]  이력 검색
    oaishistory version          버전 목록 조회
    oaishistory sync             oaisfix 완료 항목 동기화

태그 종류:
    HOTFIX, BUGFIX, IMPROVE, ENHANCE, FEATURE, REFACTOR, DOCS, CONFIG

옵션:
    --dry-run              sync 시 미리보기만
    --force                create 시 기존 파일 덮어쓰기
```

### 3.6 oaiscommand - 명령어 관리

```
명령어:
    oaiscommand run         명령어 현황 조회
    oaiscommand sync        pyproject.toml 동기화
    oaiscommand list        등록된 명령어 목록

옵션:
    --dry-run              sync 시 미리보기만
```

### 3.7 oaissync - 프로젝트 동기화

```
명령어:
    oaissync run            전체 동기화 실행
    oaissync status         동기화 상태 조회
    oaissync push           변경 사항 푸시

옵션:
    --dry-run              미리보기만
    --push-only            푸시만 실행
```

### 3.8 oaisenv - 환경 분석

```
명령어:
    oaisenv run             환경 분석 및 d0009_env.md 생성

옵션:
    --dry-run              미리보기만
```

### 3.9 oaisreport - 리포트 생성

```
명령어:
    oaisreport run              신규 리포트 생성 (기본)
    oaisreport update [name]    기존 리포트 업데이트
    oaisreport list             생성된 리포트 목록 확인

옵션:
    --source [파일]        데이터 소스 지정 (기본: d0004_todo.md)
    --template [템플릿]    템플릿 지정 (weekly, monthly, custom)
    --format [형식]        출력 형식 (md, pdf, pptx)
    --out [경로]           출력 경로 지정
    --dry-run              미리보기만
```

### 3.10 oaishelp - 도움말

```
명령어:
    oaishelp                전체 스킬 목록
    oaishelp [스킬명]       특정 스킬 상세

옵션:
    --json                 JSON 형식 출력
```

---

## 4. 스크립트 작성 규칙

### 4.1 파일 구조

```python
#!/usr/bin/env python3
"""
oaisXXX_run.py - 간단한 설명 (1줄)
"""
import sys
from oais_common import (
    show_help_if_no_args, PROJECT_ROOT, DOC_DIR,
    log_info, log_ok, log_warn, log_error
)

def cmd_run():
    """run 서브명령어"""
    pass

def main():
    if show_help_if_no_args("oaisXXX", sys.argv[1:]):
        return
    # 명령어 처리

if __name__ == "__main__":
    sys.exit(main())
```

### 4.2 옵션 규칙

- `--dry-run`: 모든 수정 작업에서 미리보기 모드 지원
- `--force`: 덮어쓰기 등 위험한 작업에서 확인 건너뛰기
- `--verbose`: 상세 출력 (로깅 레벨 DEBUG)

### 4.3 출력 규칙

- `[OK]`: 성공
- `[INFO]`: 정보
- `[WARN]`: 경고
- `[ERROR]`: 에러
- `[TIP]`: 권장 사항
- `[DRY-RUN]`: 미리보기 모드

---

## 5. 참고

- 스킬 문서: `v/oais*.md`
- 스크립트 위치: `v/script/oais*_run.py`
- 공통 모듈: `v/script/oais_common.py`
