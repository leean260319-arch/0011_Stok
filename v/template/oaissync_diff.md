# oaissync diff 출력 템플릿

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2026-01-12 | 초기 버전 생성 - cmd_diff 출력 템플릿화 |

---

> oaissync diff 명령어의 출력 형식을 정의하는 템플릿입니다.
> 파일명 미지정 시 모든 차이 파일을 순서대로 표시합니다.

## 사용 변수

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `{source_project}` | 소스(현재) 프로젝트명 | 0001_vibe |
| `{target_project}` | 대상 프로젝트명 | 0005_CCone |
| `{current_index}` | 현재 파일 인덱스 | 1 |
| `{total_count}` | 전체 차이 파일 수 | 36 |
| `{file_path}` | 파일 경로 | v/oaischeck.md |
| `{source_mtime}` | 소스 수정일 | 2026-01-06 11:16 |
| `{target_mtime}` | 대상 수정일 | 2025-12-30 11:02 |
| `{status}` | 비교 상태 | NEWER_SOURCE |
| `{status_symbol}` | 상태 기호 | >> |
| `{status_desc}` | 상태 설명 | 소스가 최신 |
| `{added_lines}` | 추가된 줄 수 | 11 |
| `{removed_lines}` | 삭제된 줄 수 | 0 |
| `{change_summary}` | 변경 요약 | 소스에 +11줄 추가 |
| `{diff_content}` | diff 내용 | (unified diff) |

---

## 템플릿 본문

### 전체 diff 헤더 (파일명 미지정 시)

```template
# oaissync diff - 전체 차이점 비교

## 비교 대상

| 항목 | 값 |
|------|-----|
| 소스 (현재) | `{source_project}` |
| 대상 | `{target_project}` |
| 차이 파일 수 | {total_count}개 |

---
```

### 개별 파일 diff

```template
## [{current_index}/{total_count}] {file_path}

| 항목 | 값 |
|------|-----|
| 소스 (현재) | `{source_project}` - {source_mtime} |
| 대상 | `{target_project}` - {target_mtime} |
| 비교 결과 | **{status_desc}** ({status_symbol}) |
| 변경 내용 | {change_summary} |

### 차이점

```diff
{diff_content}
```

---
```

### 상태별 설명

| 상태 | 기호 | 설명 | 변경 요약 형식 |
|------|------|------|---------------|
| ONLY_SOURCE | -> | 대상에 없음 | 소스에만 존재 (신규 파일) |
| ONLY_TARGET | <- | 소스에 없음 | 대상에만 존재 |
| NEWER_SOURCE | >> | 소스가 최신 | 소스에 +N줄 추가, -M줄 삭제 |
| NEWER_TARGET | << | 대상이 최신 | 대상에 +N줄 추가, -M줄 삭제 |

### 변경 요약 생성 규칙

1. **ONLY_SOURCE**: "소스에만 존재 (신규 파일, N줄)"
2. **ONLY_TARGET**: "대상에만 존재 (N줄)"
3. **NEWER_SOURCE**:
   - added > 0, removed == 0: "소스에 +{added}줄 추가 (대상에 없음)"
   - added == 0, removed > 0: "소스에서 -{removed}줄 삭제"
   - added > 0, removed > 0: "소스에 +{added}줄, -{removed}줄 변경"
4. **NEWER_TARGET**:
   - 위와 동일하지만 "대상" 기준으로 설명

---

## 관련 파일

- 스크립트: `v/script/oaissync_run.py`
- 스킬 문서: `v/oaissync.md`
- view 템플릿: `v/template/oaissync_view.md`
