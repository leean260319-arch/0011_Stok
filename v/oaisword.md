# oaisword - Word 문서 생성/변환

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v02 | 2026-01-22 | `--plugin` 옵션 추가 (document-skills:docx 플러그인 통합) |
| v01 | 2026-01-22 | oaisreport에서 Word 기능 분리, 초기 버전 |

---

> 공통: `v/guide/common_guide.md` | 가이드: `v/guide/oaisword_guide.md`

Markdown을 Word(.docx) 문서로 변환하는 전문 스킬.

**2가지 처리 방식 지원:**
- **기본**: python-docx, pandoc, Node.js docx 라이브러리 직접 사용 (빠름, 간단)
- **플러그인** (`--plugin`): document-skills:docx 플러그인 (변경추적, 주석, Redlining 지원)

## 서브명령어

| 명령어 | 설명 |
|--------|------|
| `oaisword version` | 스킬 버전 정보 (v02) |
| `status` | 의존성 상태, 스크립트 목록 확인 |
| `convert` | Markdown → Word 기본 변환 (python-docx) |
| `convert --pandoc` | Markdown → Word (LaTeX 수식 + mermaid 지원) |
| `convert --plugin` | Markdown → Word (플러그인, 고급 기능 지원) |
| `quotation` | 견적서 마크다운 → 워드 (표/스타일 자동 서식) |
| `quotation --plugin` | 견적서 변환 (플러그인, 변경추적 지원) |
| `edit` | 기존 DOCX 편집 (플러그인 전용) |
| `template` | 커스텀 템플릿 기반 Word 생성 |

### --plugin 모드 추가 옵션

| 옵션 | 설명 |
|------|------|
| `--track-changes` | 변경 추적 활성화 (Tracked Changes) |
| `--comment "텍스트"` | 주석 추가 |
| `--redline` | Redlining 워크플로우 (문서 검토용) |
| `--author "이름"` | 작성자 이름 지정 (기본: Claude) |

---

## convert 서브명령어 (기본 변환)

Markdown 파일을 Word 문서로 변환합니다.

### convert 사용법

```bash
# 기본 변환 (python-docx)
oaisword convert doc/d0102_문서.md
# → doc/d0102_문서.docx

# LaTeX 수식 + mermaid 다이어그램 포함 (pandoc)
oaisword convert doc/d0102_논문.md --pandoc
# → doc/d0102_논문.docx (수식 OMML + mermaid PNG)
```

### convert 옵션

| 옵션 | 설명 |
|------|------|
| `<input_file>` | 입력 마크다운 파일 (필수) |
| `--pandoc` | pandoc 사용 (LaTeX 수식, mermaid 지원) |
| `--output <path>` | 출력 경로 지정 (기본: 입력파일과 동일 위치) |

### convert 지원 요소

| 마크다운 요소 | 변환 결과 |
|--------------|----------|
| `# H1` ~ `##### H5` | Word 제목 스타일 (Heading 0~4) |
| `- 목록` | 글머리 기호 목록 |
| `1. 번호` | 번호 매기기 목록 |
| `> 인용` | 들여쓰기 단락 |
| `**굵게**` | Bold |
| `*기울임*` | Italic |
| `` `코드` `` | Consolas 글꼴 (10pt) |
| `\|표\|` | Word 테이블 (테두리 자동) |
| `\`\`\`코드블록\`\`\`` | Consolas 글꼴 코드 블록 |

### convert --pandoc 추가 지원

| 요소 | 변환 방식 |
|------|----------|
| LaTeX 수식 (`$...$`, `$$...$$`) | OMML (Office Math) 변환 |
| mermaid 다이어그램 | PNG 이미지로 변환 후 삽입 |

---

## quotation 서브명령어 (견적서)

견적서 마크다운을 전문적인 워드 문서로 변환합니다. 표 서식, 금액 정렬, 소계/합계 강조 등 비즈니스 문서 스타일 자동 적용.

### quotation 사용법

```bash
# 기본 사용 (출력 경로 자동)
oaisword quotation doc/d0023_견적.md
# → doc/d0023_견적.docx

# 출력 경로 지정
oaisword quotation doc/d0023_견적.md --output tmp/reports/견적서.docx

# 커스텀 스타일 적용
oaisword quotation doc/견적서.md --config v/template/custom_config.json
```

### quotation 옵션

| 옵션 | 설명 |
|------|------|
| `<input_file>` | 입력 마크다운 파일 (필수) |
| `--output <path>` | 출력 경로 (기본: 입력파일과 동일 위치/이름.docx) |
| `--config <path>` | 커스텀 스타일 설정 JSON |

### quotation 자동 서식

| 기능 | 설명 |
|------|------|
| 표 헤더 | 배경색 자동 적용, 중앙 정렬, 굵게 |
| 금액 셀 | 우측 정렬 (`원`, 숫자로 끝나는 셀) |
| 소계 행 | 회색 배경, 굵게 |
| 합계 행 | 노란색 배경, 굵게 |
| 서명란 | 문서 하단 자동 추가 (작성/검토/승인) |
| 이미지 | 부록으로 이동, 표 형태로 배치 |

### quotation 스타일 설정 (JSON)

```json
{
  "document": {
    "defaultFont": "맑은 고딕",
    "defaultSize": 22,
    "margin": { "top": 1440, "right": 1200, "bottom": 1440, "left": 1200 }
  },
  "table": {
    "headerBackground": "E8F4FD",
    "subtotalBackground": "F0F0F0",
    "totalBackground": "FFF3CD"
  },
  "signature": {
    "columns": ["작성", "검토", "승인"]
  }
}
```

---

## template 서브명령어 (템플릿 기반)

커스텀 템플릿을 기반으로 Word 문서를 생성합니다.

### template 사용법

```bash
# 템플릿 + 데이터로 Word 생성
oaisword template --template v/template/report.docx --data data/report_data.json --output tmp/report.docx
```

### template 옵션

| 옵션 | 설명 |
|------|------|
| `--template <path>` | Word 템플릿 파일 (.docx) |
| `--data <path>` | 데이터 파일 (JSON/YAML) |
| `--output <path>` | 출력 경로 |

---

## edit 서브명령어 (플러그인 전용)

기존 Word 문서를 편집합니다. document-skills:docx 플러그인 기반으로 변경 추적, 주석 등 고급 기능을 지원합니다.

### edit 사용법

```bash
# 기존 문서 편집 (변경 추적 활성화)
oaisword edit doc/contract.docx --track-changes

# 문서에 주석 추가
oaisword edit doc/contract.docx --comment "검토 필요"

# Redlining 워크플로우 (문서 검토)
oaisword edit doc/contract.docx --redline

# 작성자 지정
oaisword edit doc/contract.docx --track-changes --author "홍길동"
```

### edit 옵션

| 옵션 | 설명 |
|------|------|
| `<input_file>` | 편집할 DOCX 파일 (필수) |
| `--track-changes` | 변경 추적 활성화 |
| `--comment "텍스트"` | 주석 추가 |
| `--redline` | Redlining 워크플로우 |
| `--author "이름"` | 작성자 이름 (기본: Claude) |
| `--output <path>` | 출력 경로 (기본: 원본 덮어쓰기) |

### edit 지원 기능 (플러그인)

| 기능 | 설명 |
|------|------|
| 변경 추적 | `<w:ins>`, `<w:del>` 태그로 삽입/삭제 추적 |
| 주석 | `comments.xml`에 주석 추가, 답글 지원 |
| Redlining | 마크다운 기반 변경 계획 → OOXML 적용 |
| 서식 보존 | 원본 문서 스타일, RSID 보존 |

---

## 서브에이전트

| 단계 | 에이전트 | 역할 |
|------|---------|------|
| 분석 | Explore | 입력 파일 구조 분석 |
| 변환 | task-executor | MD → DOCX 변환 실행 |
| 검증 | task-checker | 출력 파일 검증 |

## 워크플로우

### 기본 모드
```
입력 분석 → 변환 방식 결정 → 변환 실행 → 출력 검증
     ↓
python-docx (기본) / pandoc (수식/mermaid) / Node.js docx (견적서)
```

### 플러그인 모드 (`--plugin`)
```
입력 분석 → unpack → Document 라이브러리 처리 → pack → 출력 검증
     ↓
document-skills:docx 플러그인
     ↓
변경추적 / 주석 / Redlining / OOXML 직접 조작
```

### Redlining 워크플로우 (`--redline`)
```
1. pandoc으로 DOCX → Markdown 변환 (변경추적 포함)
2. 변경 사항 식별 및 그룹화 (배치 단위)
3. ooxml.md 참조하여 XML 패턴 확인
4. unpack → Python 스크립트로 변경 적용 → pack
5. 최종 검증 (pandoc으로 다시 Markdown 변환 후 확인)
```

---

## 의존성

### 기본 모드

| 패키지 | 용도 | 필수 | 설치 |
|--------|------|:----:|------|
| python-docx | 기본 MD→DOCX 변환 | O | `uv add python-docx` |
| pandoc | LaTeX 수식/mermaid 지원 | - | [pandoc.org](https://pandoc.org/installing.html) |
| mermaid-cli | mermaid → PNG | - | `npm install -g @mermaid-js/mermaid-cli` |
| docx (npm) | quotation용 워드 생성 | - | `npm install docx` |

### 플러그인 모드 (`--plugin`)

| 패키지 | 용도 | 필수 | 설치 |
|--------|------|:----:|------|
| defusedxml | 보안 XML 파싱 | O | `pip install defusedxml` |
| pandoc | 텍스트 추출/변환 | O | [pandoc.org](https://pandoc.org/installing.html) |
| docx (npm) | 새 문서 생성 (docx-js) | - | `npm install docx` |
| LibreOffice | PDF 변환 | - | `apt install libreoffice` |
| Poppler | PDF→이미지 변환 | - | `apt install poppler-utils` |

> **플러그인 위치**: `.claude/skills/docx/`

### 의존성 확인

```bash
# 기본 모드
uv run python -c "import docx; print('python-docx OK')"
pandoc --version
mmdc --version
node -e "require('docx'); console.log('docx OK')"

# 플러그인 모드
python -c "import defusedxml; print('defusedxml OK')"
ls .claude/skills/docx/SKILL.md && echo 'plugin OK'
```

---

## 관련 파일

### 기본 모드

| 구분 | 경로 |
|------|------|
| 스킬 정의 | `v/oaisword.md` |
| 변환 스크립트 | `v/script/oaisreport_md2docx.py` |
| 견적서 변환기 | `v/template/quotation_docx.js` |
| 견적서 스타일 | `v/template/quotation_docx.json` |
| 가이드 | `v/guide/oaisword_guide.md` |

### 플러그인 모드

| 구분 | 경로 |
|------|------|
| 플러그인 정의 | `.claude/skills/docx/SKILL.md` |
| OOXML 레퍼런스 | `.claude/skills/docx/ooxml.md` |
| docx-js 가이드 | `.claude/skills/docx/docx-js.md` |
| Document 라이브러리 | `.claude/skills/docx/scripts/document.py` |
| pack/unpack 스크립트 | `.claude/skills/docx/ooxml/scripts/` |
| XML 스키마 | `.claude/skills/docx/ooxml/schemas/` |

---

## 출력 경로 규칙

> **핵심 원칙**: 출력 파일은 입력 파일과 동일한 폴더에, 동일한 파일명으로, 확장자만 `.docx`로 변경

| 입력 | 출력 |
|------|------|
| `doc/d0102_문서.md` | `doc/d0102_문서.docx` |
| `tmp/draft.md` | `tmp/draft.docx` |

---

## 사용 예시

### 기본 변환

```bash
# 단순 변환
oaisword convert doc/d0102_가상논문.md

# 수식 포함 논문 변환
oaisword convert doc/d0102_가상논문.md --pandoc
```

### 견적서 변환

```bash
# 견적서 워드 생성
oaisword quotation doc/d0023_1차개발_견적.md
```

### 플러그인 모드 (`--plugin`)

```bash
# 플러그인으로 변환 (고급 서식 지원)
oaisword convert doc/d0102_문서.md --plugin

# 기존 문서 편집 (변경 추적)
oaisword edit doc/contract.docx --track-changes

# Redlining 워크플로우
oaisword edit doc/contract.docx --redline --author "검토자"

# 주석 추가
oaisword edit doc/report.docx --comment "3페이지 수정 필요"
```

### 스크립트 직접 실행

```bash
# 기본 모드 - python-docx
uv run python v/script/oaisreport_md2docx.py doc/d0102_문서.md

# 기본 모드 - pandoc
uv run python v/script/oaisreport_md2docx.py doc/d0102_문서.md --pandoc

# 기본 모드 - Node.js 견적서
node v/template/quotation_docx.js doc/d0023_견적.md

# 플러그인 모드 - unpack/pack
python .claude/skills/docx/ooxml/scripts/unpack.py doc.docx unpacked/
python .claude/skills/docx/ooxml/scripts/pack.py unpacked/ output.docx
```
