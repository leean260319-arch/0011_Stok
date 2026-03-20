# oaissync list 출력 템플릿

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2026-01-15 | 초기 버전 생성 - cmd_list 출력 템플릿화 |
| v02 | 2026-01-15 | 박스 테이블 형식으로 변경 |

---

> oaissync list 명령어의 출력 형식을 정의하는 템플릿입니다.
> 변수는 `{variable_name}` 형식으로 사용합니다.

## 사용 변수

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `{scan_path}` | 스캔 경로 | D:\resilio\3_code |
| `{project_rows}` | 프로젝트 목록 행 (동적 생성) | - |
| `{total_count}` | 총 프로젝트 수 | 27 |
| `{full_count}` | Full 상태 프로젝트 수 | 7 |
| `{partial_count}` | Partial 상태 프로젝트 수 | 6 |
| `{none_count}` | None 상태 프로젝트 수 | 14 |
| `{sync_needed_count}` | 동기화 필요 프로젝트 수 | 2 |

---

## 템플릿 본문

```template
# oaissync list - 프로젝트 목록

스캔 경로: `{scan_path}`

{table_output}

총 {total_count}개 프로젝트 발견

## 상태 설명
- Full: vibe 환경 완전 구축 (.claude/ AND v/)
- Partial: 부분 구축 (.claude/ OR v/)
- None: vibe 환경 없음 (새로 구축 가능)

## Sync 컬럼
- OK: 동기화 완료 (차이 없음)
- 숫자: 동기화 필요 (차이 파일 수)
- -: 비교 불가 (Full 상태 아님)
```

## 박스 테이블 형식

테이블은 박스 문자를 사용하여 렌더링됩니다:

```
┌────┬─────────────────────────────────┬─────────┬──────────┬─────┬──────┐
│ #  │ Project                         │ Status  │ .claude/ │ v/  │ Sync │
├────┼─────────────────────────────────┼─────────┼──────────┼─────┼──────┤
│  1 │ 0000_python                     │ Full    │    O     │  O  │  OK  │
│  2 │ 0002_paper                      │ Full    │    O     │  O  │  61  │
└────┴─────────────────────────────────┴─────────┴──────────┴─────┴──────┘
```

---

## 섹션별 템플릿

### project_rows (프로젝트 행)

```template
| {index} | {project_name} | {status} | {has_claude} | {has_v} | {sync_status} |
```

### 행 변수

| 변수명 | 설명 | 값 |
|--------|------|-----|
| `{index}` | 순번 | 1, 2, 3... |
| `{project_name}` | 프로젝트명 | 0001_vibe |
| `{status}` | 환경 상태 | Full / Partial / None |
| `{has_claude}` | .claude/ 존재 | O / X |
| `{has_v}` | v/ 존재 | O / X |
| `{sync_status}` | 동기화 상태 | OK / 숫자 / - |

### status 값 정의

| 값 | 조건 | 설명 |
|-----|------|------|
| Full | .claude/ AND v/ | 완전 구축 |
| Partial | .claude/ XOR v/ | 부분 구축 |
| None | 둘 다 없음 | 미구축 |

### sync_status 값 정의

| 값 | 조건 | 설명 |
|-----|------|------|
| OK | diff_count == 0 | 동기화 완료 |
| 숫자 | diff_count > 0 | 차이 파일 수 |
| - | status != Full | 비교 불가 |

---

## 출력 예시

```
# oaissync list - 프로젝트 목록

스캔 경로: `D:\resilio\3_code`

┌────┬──────────────┬─────────┬──────────┬─────┬──────┐
│ #  │ Project      │  Status │ .claude/ │  v/ │ Sync │
├────┼──────────────┼─────────┼──────────┼─────┼──────┤
│  1 │ 0000_sandbox │   None  │    X     │  X  │  -   │
│  2 │ 0002_paper   │   Full  │    O     │  O  │  3   │
│  3 │ 0003_GPU     │ Partial │    O     │  X  │  -   │
│  4 │ 0004_SApp    │   Full  │    O     │  O  │  OK  │
│  5 │ 0005_CCone   │   Full  │    O     │  O  │  2   │
└────┴──────────────┴─────────┴──────────┴─────┴──────┘

총 5개 프로젝트 발견

## 상태 설명
- Full: vibe 환경 완전 구축 (.claude/ AND v/)
- Partial: 부분 구축 (.claude/ OR v/)
- None: vibe 환경 없음 (새로 구축 가능)

## Sync 컬럼
- OK: 동기화 완료 (차이 없음)
- 숫자: 동기화 필요 (차이 파일 수)
- -: 비교 불가 (Full 상태 아님)
```

---

## 사용법

### Python 코드 예시

```python
from pathlib import Path

TEMPLATE_PATH = Path("v/template/oaissync_list.md")

def load_template():
    """템플릿 파일에서 본문 추출"""
    content = TEMPLATE_PATH.read_text(encoding='utf-8')
    # ```template ... ``` 블록 추출
    import re
    match = re.search(r'```template\n(.*?)\n```', content, re.DOTALL)
    if match:
        return match.group(1)
    return ""

def render_project_row(index: int, project: dict) -> str:
    """프로젝트 행 렌더링"""
    return f"| {index} | {project['name']} | {project['status']} | {project['has_claude']} | {project['has_v']} | {project['sync']} |"

def render_list(scan_path: str, projects: list) -> str:
    """프로젝트 목록 렌더링"""
    template = load_template()

    rows = "\n".join([
        render_project_row(i+1, p) for i, p in enumerate(projects)
    ])

    return template.format(
        scan_path=scan_path,
        project_rows=rows,
        total_count=len(projects)
    )
```

---

## 관련 파일

- 스크립트: `v/script/oaissync_run.py`
- 스킬 문서: `v/oaissync.md`
- 관련 템플릿: `v/template/oaissync_view.md`, `v/template/oaissync_diff.md`
