# oaissync view 출력 템플릿

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2026-01-12 | 초기 버전 생성 - cmd_view 출력 템플릿화 |

---

> oaissync view 명령어의 출력 형식을 정의하는 템플릿입니다.
> 변수는 `{variable_name}` 형식으로 사용합니다.

## 사용 변수

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `{source_project}` | 소스(현재) 프로젝트명 | 0001_vibe |
| `{target_project}` | 대상 프로젝트명 | 0004_SApp |
| `{env_status}` | 대상 Vibe 환경 상태 | Full / Partial / None |
| `{has_claude}` | .claude/ 존재 여부 | O / X |
| `{has_v}` | v/ 존재 여부 | O / X |
| `{summary_table}` | 요약 테이블 (동적 생성) | - |
| `{total_files}` | 총 파일 수 | 532 |
| `{diff_count}` | 차이 파일 수 | 8 |
| `{detail_table}` | 상세 차이점 테이블 (동적 생성) | - |
| `{no_diff_message}` | 차이 없을 때 메시지 | - |

---

## 템플릿 본문

```template
# oaissync view - 차이점 비교

## 비교 대상

| 항목 | 값 |
|------|-----|
| 소스 (현재) | `{source_project}` |
| 대상 | `{target_project}` |
| 대상 Vibe 상태 | {env_status} |
| .claude/ | {has_claude} |
| v/ | {has_v} |

## 요약

{summary_table}

**총 {total_files}개 파일 중 {diff_count}개 차이**

{detail_section}
```

---

## 섹션별 템플릿

### summary_table (요약 테이블)

```template
| 상태 | 기호 | 설명 | 개수 |
|------|------|------|------|
| SAME | == | 동일 | {same_count} |
{status_rows}
```

### status_rows (상태별 행)

| 상태 | 기호 | 설명 |
|------|------|------|
| ONLY_SOURCE | -> | 대상에 없음 -> 복사 필요 |
| ONLY_TARGET | <- | 현재에 없음 <- 가져오기 |
| NEWER_SOURCE | >> | 현재가 최신 -> 덮어쓰기 |
| NEWER_TARGET | << | 대상이 최신 <- 가져오기 |

### detail_section (상세 섹션)

#### 차이가 있을 때

```template
## 상세 차이점

| 상태 | 파일 | 소스 수정일 | 대상 수정일 |
|:----:|------|------------|------------|
{detail_rows}
```

#### 차이가 없을 때

```template
모든 파일이 동일합니다.
```

### detail_rows (상세 행)

```template
| {symbol} | `{file_path}` | {source_mtime} | {target_mtime} |
```

---

## 사용법

### Python 코드 예시

```python
from pathlib import Path

TEMPLATE_PATH = Path("v/template/oaissync_view.md")

def load_template():
    """템플릿 파일에서 본문 추출"""
    content = TEMPLATE_PATH.read_text(encoding='utf-8')
    # ```template ... ``` 블록 추출
    # 변수 치환 후 출력
    return content

def render_view(data: dict) -> str:
    """데이터로 템플릿 렌더링"""
    template = load_template()
    return template.format(**data)
```

---

## 관련 파일

- 스크립트: `v/script/oaissync_run.py`
- 스킬 문서: `v/oaissync.md`
