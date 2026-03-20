# oaisreport 가이드

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v09 | 2026-01-22 | Word 기능 분리 → `v/guide/oaisword_guide.md` |
| v08 | 2026-01-17 | algorithm 서브명령어 사용 예시 추가 |
| v07 | 2026-01-07 | mermaid 다이어그램 지원 추가 (--pandoc 옵션) |
| v06 | 2026-01-07 | write 서브명령어 사용 예시 추가 |
| v05 | 2026-01-07 | pdf, pdf --pandoc 서브명령어 추가 |
| v04 | 2026-01-07 | --pandoc 옵션 추가 (LaTeX 수식 지원) |
| v03 | 2026-01-06 | 템플릿 명명 규칙 추가 (oaisreport_*.md 패턴) |

---

> 스킬 정의: `v/oaisreport.md` | 공통 가이드: `v/guide/common_guide.md` | Word: `v/guide/oaisword_guide.md`

## 1. 출력 경로 규칙

> **핵심 원칙**: 리포트는 항상 원본 파일과 동일한 폴더에, 동일한 파일명으로, 확장자만 변경하여 생성

### 1.1 경로 변환 규칙

| 원본 파일 | 리포트 출력 |
|----------|------------|
| `doc/d0004_todo.md` | `doc/d0004_todo.html` |
| `doc/d0001_prd.md` | `doc/d0001_prd.pdf` |
| `doc/d0100_survey.md` | `doc/d0100_survey.pptx` |

### 1.2 확장자 매핑

| 출력 포맷 | 확장자 |
|----------|-------|
| HTML | `.html` |
| PDF | `.pdf` |
| PowerPoint | `.pptx` |
| Markdown | `_report.md` |

> **Note**: MD→MD 변환 시 `_report` 접미사 추가로 원본과 구분
> **Word 변환**: `v/guide/oaisword_guide.md` 참조

---

## 2. 사용 예시

### 2.1 PDF 변환

```bash
oaisreport pdf doc/d0001_prd.md
# → doc/d0001_prd.pdf

# LaTeX 수식 + mermaid 다이어그램 포함 문서 변환 (pandoc 사용)
oaisreport pdf doc/d0102_가상논문.md --pandoc
# → doc/d0102_가상논문.pdf (수식 LaTeX + mermaid PNG 변환)
```

### 2.2 논문 작성 (write)

```bash
# 특정 섹션 작성/확장
oaisreport write doc/d0102_가상논문.md --section "3.1 아키텍처 개요"

# 기존 내용 다듬기 (문체, 명확성)
oaisreport write doc/d0102_가상논문.md --refine

# 전체 논문 검토
oaisreport write doc/d0102_가상논문.md --review

# 영어 학술 문체로 작성
oaisreport write doc/d0102_가상논문.md --section "Abstract" --lang en --style academic
```

### 2.3 HTML 변환

```bash
oaisreport run --source doc/d0004_todo.md --format html
# → doc/d0004_todo.html
```

### 2.4 알고리즘 코드 분석 (algorithm)

```bash
# 기본 사용: ps 스크립트 분석하여 문서 생성
oaisreport algorithm src/ps63_img_iqa/ps6310_nr_iqas.py
# → doc/d6310_nr_iqas.md (문서 번호 자동 추출)

# 문서 ID 명시적 지정
oaisreport algorithm src/ps62_img_filter/ps6211_cee_filter.py --doc-id d6211
# → doc/d6211_cee_filter.md

# 출력 경로 직접 지정
oaisreport algorithm src/ps63_img_iqa/ps6310_nr_iqas.py --output doc/d6310_NR-IQAs.md

# 라이브러리 정보 섹션 제외 (간략 버전)
oaisreport algorithm src/ps63_img_iqa/ps6310_nr_iqas.py --no-lib
```

**분석 항목:**
- 개요 (목적, 주요 특징, 처리 단계)
- 실행 방법 (기본 실행, 명령행 옵션, 예시)
- 설정 (CONFIG 딕셔너리)
- 기능/메트릭 상세
- 출력 파일 (디렉토리, 파일 목록)
- 코드 구조 (핵심 함수, 의존성, 처리 흐름)
- 참고사항

> **샘플 문서**: `doc/d6310_NR-IQAs.md` 참조

---

## 3. 템플릿

### 3.1 명명 규칙

> **패턴**: `v/template/oaisreport_*.md`

| 템플릿 | 용도 |
|--------|------|
| `oaisreport_algorithm.md` | **알고리즘 코드 분석 문서** (ps*.py → d*.md) |
| `oaisreport_error.md` | 에러 리포트 |
| `oaisreport_weekly.md` | 주간 리포트 (예정) |
| `oaisreport_monthly.md` | 월간 리포트 (예정) |

### 3.2 Jinja2 템플릿 문법

```markdown
# 주간 현황 ({{WEEK_NUMBER}})
- 신규: {{NEW_ISSUES_COUNT}}건 / 완료: {{COMPLETED_ISSUES_COUNT}}건
{{NEW_ISSUES_LIST}}
```

### 3.2 사용 가능한 변수

| 변수 | 설명 |
|------|------|
| `{{WEEK_NUMBER}}` | 주차 번호 |
| `{{NEW_ISSUES_COUNT}}` | 신규 이슈 수 |
| `{{COMPLETED_ISSUES_COUNT}}` | 완료 이슈 수 |
| `{{NEW_ISSUES_LIST}}` | 신규 이슈 목록 |

---

## 4. 스크립트

### 4.1 명명 규칙

> **패턴**: `v/script/oaisreport_*.py`

| 스크립트 | 용도 | 실행 예시 |
|----------|------|----------|
| `oaisreport_run.py` | 메인 실행 | `uv run python v/script/oaisreport_run.py status` |
| `oaisreport_md2pdf.py` | MD→PDF 변환 | `uv run python v/script/oaisreport_md2pdf.py <file>` |

> **Word 스크립트**: `v/guide/oaisword_guide.md` 참조

### 4.2 새 스크립트 추가 시

```
파일명: oaisreport_{기능}.py
위치: v/script/
예시: oaisreport_md2html.py
```

> 참조: `v/oaisdoc.md` 섹션 8.2 스크립트 분류

---

## 5. 의존성 설치

### 5.1 mermaid-cli (mermaid 다이어그램 변환)

```bash
npm install -g @mermaid-js/mermaid-cli
```

> **확인**: `mmdc --version` 으로 설치 확인

### 5.2 pandoc (LaTeX 수식 + 고급 변환)

- Windows: https://pandoc.org/installing.html
- macOS: `brew install pandoc`

---

## 6. 관련 문서

| 문서 | 용도 |
|------|------|
| `v/oaisreport.md` | 스킬 정의 |
| `v/oaisword.md` | Word 스킬 정의 |
| `v/guide/oaisword_guide.md` | Word 가이드 |
| `v/template/oaisreport_algorithm.md` | 알고리즘 코드 분석 템플릿 |
| `v/template/oaisreport_error.md` | 에러 리포트 템플릿 |
| `v/guide/common_guide.md` | 공통 가이드 |
| `doc/d6310_NR-IQAs.md` | 알고리즘 문서 샘플 (NR-IQA) |
