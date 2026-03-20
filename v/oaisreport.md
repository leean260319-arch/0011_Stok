# oaisreport - 리포트 자동 생성

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v12 | 2026-01-22 | Word 기능 분리 → `v/oaisword.md` (word, quotation 제거) |
| v11 | 2026-01-17 | algorithm 서브명령어 추가 (알고리즘 코드 분석 문서 생성) |
| v10 | 2026-01-07 | 0001_vibe + 0013_dualbranck 병합 (quotation + write/pdf/mermaid) |
| v09 | 2026-01-07 | mermaid 다이어그램 지원 추가 (--pandoc 옵션) |
| v08 | 2026-01-07 | write 서브명령어 추가 (논문 작성/다듬기) |
| v07 | 2026-01-07 | pdf, pdf --pandoc 서브명령어 추가 |
| v05 | 2026-01-06 | 템플릿 명명 규칙 추가 (oaisreport_*.md 패턴) |
| v01 | 2026-01-03 | 문서 이력 관리 섹션 추가 |

---

> 공통: `v/guide/common_guide.md` | 가이드: `v/guide/oaisreport_guide.md` | Word: `v/oaisword.md`

데이터 소스 기반 리포트 생성. 템플릿 렌더링, 다중 포맷(MD/PDF/PPTX) 지원.

> **Word 문서 생성**: `v/oaisword.md` 스킬 참조 (word, quotation 기능 분리됨)

## 서브명령어

| 명령어 | 설명 |
|--------|------|
| `oaisreport version` | 스킬 버전 정보 (v12) |
| `status` | 서브명령어 리스트, 스킬/문서 상태 |
| `run` | 신규 리포트 생성 |
| `write` | **논문 작성/다듬기** (연구자 모드) |
| `pdf` | Markdown → PDF 변환 |
| `pdf --pandoc` | Markdown → PDF (LaTeX 수식 + mermaid 지원) |
| `update` | 기존 리포트 업데이트 |
| `list` | 리포트 목록 조회 |
| `algorithm` | **알고리즘 코드 분석** 문서 자동 생성 (ps*.py → d*.md) |

---

## write 서브명령어 (논문 작성)

연구자 관점에서 논문을 작성하고 다듬는 스킬.

### write 사용법

```bash
# 새 섹션 작성
oaisreport write <file> --section "3.1 아키텍처 개요"

# 기존 내용 다듬기
oaisreport write <file> --refine

# 전체 논문 검토/개선
oaisreport write <file> --review
```

### write 옵션

| 옵션 | 설명 |
|------|------|
| `--section <name>` | 특정 섹션 작성/확장 |
| `--refine` | 기존 내용 다듬기 (문체, 명확성, 논리) |
| `--review` | 전체 검토 및 개선점 제안 |
| `--style <type>` | 문체 지정 (academic, technical, survey) |
| `--lang <code>` | 언어 지정 (ko, en) 기본: ko |

### write 서브에이전트

| 단계 | 에이전트 | 역할 |
|------|---------|------|
| 분석 | academic-researcher | 논문 구조, 선행연구 분석 |
| 작성 | task-executor + scribe | 연구자 관점 글쓰기 |
| 검토 | task-checker | 논리적 일관성, 학술적 정확성 검증 |

### write 워크플로우

```
문서 읽기 → 구조 분석 → 섹션별 작성/다듬기 → 검토 → 저장
     ↓
academic-researcher: 선행연구, 방법론 분석
     ↓
scribe (--persona-scribe): 학술적 문체로 작성
     ↓
task-checker: 논리/인용/일관성 검증
```

### write 작성 원칙

| 원칙 | 설명 |
|------|------|
| 객관성 | 주관적 표현 지양, 근거 기반 서술 |
| 명확성 | 모호한 표현 제거, 정확한 용어 사용 |
| 논리성 | 섹션 간 논리적 흐름 유지 |
| 인용 | 주장에 대한 적절한 참고문헌 연결 |

---

## algorithm 서브명령어 (알고리즘 코드 분석)

알고리즘/이미지 처리 스크립트(ps*.py)를 분석하여 문서(d*.md)를 자동 생성합니다.

### algorithm 사용법

```bash
# 기본 사용: 스크립트 지정
oaisreport algorithm <script_path>

# 문서 ID 지정
oaisreport algorithm <script_path> --doc-id d6310

# 출력 경로 지정
oaisreport algorithm <script_path> --output doc/d6310_nr_iqas.md
```

### algorithm 옵션

| 옵션 | 설명 |
|------|------|
| `<script_path>` | 분석할 스크립트 경로 (필수) |
| `--doc-id <id>` | 문서 번호 (예: d6310) |
| `--output <path>` | 출력 파일 경로 |
| `--include-lib` | 라이브러리/함수 정보 섹션 포함 (기본: 포함) |
| `--no-lib` | 라이브러리/함수 정보 섹션 제외 |

### algorithm 분석 항목

| 항목 | 설명 |
|------|------|
| 개요 | 목적, 주요 특징, 처리 단계 |
| 실행 방법 | 기본 실행, 명령행 옵션, 실행 예시 |
| 설정 | CONFIG 딕셔너리 분석 |
| 기능/메트릭 | 주요 기능 또는 메트릭 상세 (해당 시) |
| 출력 파일 | 출력 디렉토리, 파일 목록, 구조 |
| 코드 구조 | 핵심 함수, 로컬 함수, 의존성, 처리 흐름 |
| 해석 가이드 | 결과 해석 방법 (해당 시) |
| 참고사항 | 주의사항, 지원 형식 |
| 라이브러리 정보 | 사용 라이브러리 및 함수 상세 |

### algorithm 서브에이전트

| 단계 | 에이전트 | 역할 |
|------|---------|------|
| 분석 | Explore | 스크립트 구조, 의존성 분석 |
| 수집 | task-executor | CONFIG, 함수, 처리 흐름 추출 |
| 생성 | task-executor + scribe | 템플릿 기반 문서 생성 |
| 검증 | task-checker | 문서 완성도 검증 |

### algorithm 워크플로우

```
스크립트 읽기 → 구조 분석 → 템플릿 로드 → 항목 추출 → 문서 생성 → 검증
     ↓
Explore: 코드 구조, import 분석
     ↓
task-executor: CONFIG, 함수 시그니처, 처리 흐름 추출
     ↓
scribe: oaisreport_algorithm.md 템플릿 적용하여 문서 작성
     ↓
task-checker: 필수 섹션 완성도 검증
```

### algorithm 템플릿 적용 규칙

> **필수**: 알고리즘 코드 분석 문서 생성 시 반드시 `v/template/oaisreport_algorithm.md` 템플릿 구조를 따를 것

**9개 필수 섹션:**
1. 문서이력관리
2. 개요 (목적, 주요 특징, 처리 단계)
3. 실행 방법 (기본 실행, 명령행 옵션, 실행 예시)
4. 설정 (CONFIG)
5. 기능/메트릭 상세 (해당 시)
6. 출력 파일
7. 코드 구조 (핵심 함수, 로컬 함수, 의존성, 처리 흐름)
8. 참고사항
9. 라이브러리/함수 정보 (선택)

### algorithm 관련 파일

- `v/template/oaisreport_algorithm.md` - **알고리즘 문서 템플릿 (필수 참조)**
- 샘플 문서: `doc/d6310_NR-IQAs.md` (NR-IQA 통합 분석)

### algorithm 문서 번호 체계

| 번호 범위 | 영역 | 예시 |
|-----------|------|------|
| d5xxx | 머신러닝/딥러닝 | d5210_segformer |
| d6xxx | 이미지 처리/IQA | d6310_nr_iqas, d6211_cee_filter |
| d4xxx | 데이터 분석 | d4010_statistics |

---

## 서브에이전트 (run/update)

| 단계 | 에이전트 | 병렬 |
|------|---------|:----:|
| 수집 | Explore | O |
| 생성 | task-executor | O |
| 검증 | task-checker | - |

> 병렬: 독립 섹션 병렬 생성(run_in_background=true) → 최종 병합

## 워크플로우 (run/update)

```
수집 → 분석 → 템플릿 로드 → 생성 → 저장
```

**템플릿 예시:**
```markdown
# 주간 현황 ({{WEEK_NUMBER}})
- 신규: {{NEW_ISSUES_COUNT}}건 / 완료: {{COMPLETED_ISSUES_COUNT}}건
{{NEW_ISSUES_LIST}}
```

## 의존성

| 패키지 | 용도 | 필수 |
|--------|------|:----:|
| Jinja2 | 템플릿 렌더링 | O |
| markdown | MD 처리 | O |
| python-pptx | PPTX 출력 | - |
| weasyprint | PDF 출력 | - |
| pandoc | LaTeX 수식 변환 (PDF) | - |
| mermaid-cli | mermaid 다이어그램 → PNG 변환 | - |

> **mermaid-cli 설치**: `npm install -g @mermaid-js/mermaid-cli`
> **Word 의존성**: `v/oaisword.md` 참조

## 관련 경로

| 구분 | 경로 |
|------|------|
| 데이터 소스 | `doc/d{SP}*.md` |
| 출력 | 원본과 동일 폴더 (확장자만 변경) |
| 템플릿 | `v/template/oaisreport_*.md` (algorithm, error 등) |
| 스크립트 | `v/script/oaisreport_*.py` |
| 가이드 | `v/guide/oaisreport_guide.md` |
