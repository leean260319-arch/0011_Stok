# oaisword 가이드

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v02 | 2026-01-22 | `--plugin` 모드 사용법 추가 |
| v01 | 2026-01-22 | 초기 버전 (oaisreport에서 Word 기능 분리) |

---

> 스킬 정의: `v/oaisword.md` | 공통 가이드: `v/guide/common_guide.md`

## 1. 출력 경로 규칙

> **핵심 원칙**: Word 문서는 항상 원본 파일과 동일한 폴더에, 동일한 파일명으로, 확장자만 `.docx`로 변경하여 생성

### 1.1 경로 변환 예시

| 원본 파일 | Word 출력 |
|----------|----------|
| `doc/d0102_가상논문.md` | `doc/d0102_가상논문.docx` |
| `doc/d0023_견적.md` | `doc/d0023_견적.docx` |
| `tmp/draft.md` | `tmp/draft.docx` |

---

## 2. 사용 예시

### 2.1 기본 변환 (convert)

```bash
# python-docx 기반 기본 변환
oaisword convert doc/d0102_문서.md
# → doc/d0102_문서.docx

# 스크립트 직접 실행
uv run python v/script/oaisreport_md2docx.py doc/d0102_문서.md
```

### 2.2 pandoc 변환 (LaTeX 수식 + mermaid)

```bash
# LaTeX 수식 + mermaid 다이어그램 포함 문서
oaisword convert doc/d0102_논문.md --pandoc
# → doc/d0102_논문.docx (수식 OMML + mermaid PNG 변환)

# 스크립트 직접 실행
uv run python v/script/oaisreport_md2docx.py doc/d0102_논문.md --pandoc
```

> **Note**: mermaid 다이어그램은 자동으로 PNG 이미지로 변환되어 삽입됩니다.

### 2.3 견적서 변환 (quotation)

```bash
# 기본 사용 (출력 경로 자동)
oaisword quotation doc/d0023_1차개발_견적.md
# → doc/d0023_1차개발_견적.docx

# 출력 경로 지정
oaisword quotation doc/d0023_견적.md --output tmp/reports/견적서.docx

# 커스텀 스타일 적용
oaisword quotation doc/견적서.md --config v/template/custom_config.json

# Node.js 스크립트 직접 실행
node v/template/quotation_docx.js doc/d0023_견적.md
node v/template/quotation_docx.js doc/d0023_견적.md tmp/reports/견적서.docx
node v/template/quotation_docx.js doc/견적서.md tmp/견적서.docx v/template/custom_config.json
```

### 2.4 플러그인 모드 (`--plugin`)

플러그인 모드는 `document-skills:docx` 플러그인을 사용하여 변경 추적, 주석, Redlining 등 고급 기능을 지원합니다.

```bash
# 플러그인으로 변환 (고급 서식 지원)
oaisword convert doc/d0102_문서.md --plugin
# → doc/d0102_문서.docx

# 기존 문서 편집 (변경 추적 활성화)
oaisword edit doc/contract.docx --track-changes
# → 변경 사항이 추적되어 Word에서 검토 가능

# 기존 문서에 주석 추가
oaisword edit doc/report.docx --comment "3페이지 수정 필요"

# Redlining 워크플로우 (문서 검토용)
oaisword edit doc/contract.docx --redline --author "검토자"
# → 마크다운 기반 변경 계획 → OOXML 적용

# 작성자 지정
oaisword edit doc/contract.docx --track-changes --author "홍길동"
```

#### 플러그인 모드 옵션

| 옵션 | 설명 |
|------|------|
| `--plugin` | 플러그인 모드 활성화 |
| `--track-changes` | 변경 추적 활성화 (Tracked Changes) |
| `--comment "텍스트"` | 주석 추가 |
| `--redline` | Redlining 워크플로우 (문서 검토용) |
| `--author "이름"` | 작성자 이름 지정 (기본: Claude) |

#### 플러그인 모드 지원 기능

| 기능 | 설명 |
|------|------|
| 변경 추적 | `<w:ins>`, `<w:del>` 태그로 삽입/삭제 추적 |
| 주석 | `comments.xml`에 주석 추가, 답글 지원 |
| Redlining | 마크다운 기반 변경 계획 → OOXML 적용 |
| 서식 보존 | 원본 문서 스타일, RSID 보존 |

---

## 3. 변환 방식 비교

| 방식 | 도구 | 장점 | 단점 |
|------|------|------|------|
| 기본 변환 | python-docx | 빠름, 의존성 적음 | 수식/mermaid 미지원 |
| pandoc 변환 | pandoc | LaTeX 수식, mermaid 지원 | pandoc 설치 필요 |
| 견적서 변환 | Node.js docx | 비즈니스 서식 자동화 | Node.js 필요 |
| 플러그인 변환 | document-skills | 변경추적, 주석, Redlining | 플러그인 설치 필요 |

### 3.1 변환 방식 선택 가이드

| 문서 유형 | 권장 방식 |
|----------|----------|
| 일반 문서 (텍스트, 표) | 기본 변환 |
| 학술 논문 (수식 포함) | pandoc 변환 |
| 기술 문서 (mermaid 포함) | pandoc 변환 |
| 견적서, 제안서 | quotation 변환 |
| 계약서 검토 (변경 추적) | 플러그인 변환 (`--plugin --track-changes`) |
| 문서 협업 (주석 필요) | 플러그인 변환 (`--plugin --comment`) |
| 문서 Redlining | 플러그인 변환 (`--plugin --redline`) |

---

## 4. 지원 마크다운 요소

### 4.1 기본 변환 (python-docx)

| 마크다운 | Word 변환 결과 |
|----------|---------------|
| `# H1` ~ `##### H5` | Heading 0~4 스타일 |
| `- 목록` | 글머리 기호 목록 |
| `1. 번호` | 번호 매기기 목록 |
| `> 인용` | 들여쓰기 단락 |
| `**굵게**` | Bold |
| `*기울임*` | Italic |
| `` `코드` `` | Consolas 10pt |
| `\|표\|` | Word 테이블 (테두리 자동) |
| ` ```코드블록``` ` | Consolas 9pt 블록 |

### 4.2 pandoc 변환 추가 지원

| 요소 | 변환 방식 |
|------|----------|
| `$수식$` | OMML (Office Math) |
| `$$수식$$` | OMML 블록 |
| ` ```mermaid ``` ` | PNG 이미지 변환 후 삽입 |

### 4.3 견적서 변환 자동 서식

| 기능 | 설명 |
|------|------|
| 표 헤더 | 배경색 `#E8F4FD`, 중앙 정렬, 굵게 |
| 금액 셀 | 우측 정렬 (`원`, 숫자로 끝나는 셀) |
| 소계 행 | 회색 배경 `#F0F0F0`, 굵게 |
| 합계 행 | 노란색 배경 `#FFF3CD`, 굵게 |
| 서명란 | 문서 하단 자동 추가 (작성/검토/승인) |
| 이미지 | 부록으로 이동, 표 형태로 배치 |

---

## 5. 견적서 스타일 설정

### 5.1 기본 설정 파일

`v/template/quotation_docx.json`:

```json
{
  "document": {
    "defaultFont": "맑은 고딕",
    "defaultSize": 22,
    "margin": { "top": 1440, "right": 1200, "bottom": 1440, "left": 1200 }
  },
  "styles": {
    "title": { "size": 48, "bold": true, "color": "1F4E79" },
    "heading1": { "size": 32, "bold": true, "color": "1F4E79" },
    "heading2": { "size": 28, "bold": true, "color": "2E75B6" },
    "paragraph": { "size": 20 }
  },
  "table": {
    "headerBackground": "E8F4FD",
    "subtotalBackground": "F0F0F0",
    "totalBackground": "FFF3CD",
    "borderColor": "CCCCCC"
  },
  "signature": {
    "columns": ["작성", "검토", "승인"]
  }
}
```

### 5.2 커스텀 설정 적용

```bash
# 커스텀 JSON 파일 생성 후 적용
node v/template/quotation_docx.js doc/견적서.md output.docx my_style.json
```

---

## 6. 의존성 설치

### 6.1 python-docx (필수)

```bash
uv add python-docx
```

### 6.2 pandoc (선택 - 수식/mermaid용)

- **Windows**: https://pandoc.org/installing.html
- **macOS**: `brew install pandoc`
- **확인**: `pandoc --version`

### 6.3 mermaid-cli (선택 - mermaid 다이어그램용)

```bash
npm install -g @mermaid-js/mermaid-cli
```

- **확인**: `mmdc --version`

### 6.4 docx (선택 - 견적서용)

```bash
npm install docx
```

### 6.5 플러그인 모드 의존성 (선택)

플러그인 모드(`--plugin`)를 사용하려면 추가 의존성이 필요합니다.

```bash
# defusedxml (보안 XML 파싱)
pip install defusedxml

# pandoc (텍스트 추출/변환)
# 위 6.2 참조

# 플러그인 확인
ls .claude/skills/docx/SKILL.md && echo 'plugin OK'
```

> **플러그인 위치**: `.claude/skills/docx/`

#### 플러그인 관련 파일

| 파일 | 용도 |
|------|------|
| `.claude/skills/docx/SKILL.md` | 플러그인 정의 |
| `.claude/skills/docx/ooxml.md` | OOXML 레퍼런스 |
| `.claude/skills/docx/docx-js.md` | docx-js 가이드 |
| `.claude/skills/docx/scripts/document.py` | Document 라이브러리 |
| `.claude/skills/docx/ooxml/scripts/` | pack/unpack 스크립트 |

### 6.6 의존성 확인 스크립트

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

## 7. 트러블슈팅

### 7.1 한글 깨짐

- **원인**: 폰트 미설치 또는 인코딩 문제
- **해결**: `맑은 고딕` 폰트 설치 확인, UTF-8 인코딩 사용

### 7.2 mermaid 변환 실패

- **원인**: mermaid-cli 미설치
- **해결**: `npm install -g @mermaid-js/mermaid-cli`

### 7.3 pandoc 수식 변환 실패

- **원인**: pandoc 미설치 또는 구버전
- **해결**: pandoc 최신 버전 설치

### 7.4 견적서 표 서식 미적용

- **원인**: 마크다운 표 형식 오류
- **해결**: `|셀|셀|` 형식 확인, 구분선 `|---|---|` 포함 확인

### 7.5 플러그인 모드 오류

#### 플러그인 미설치
- **원인**: `.claude/skills/docx/` 폴더 없음
- **해결**: document-skills:docx 플러그인 설치 필요

#### defusedxml 미설치
- **원인**: `--plugin` 옵션 사용 시 defusedxml 라이브러리 필요
- **해결**: `pip install defusedxml`

#### 변경 추적 미동작
- **원인**: `--track-changes` 옵션 누락 또는 기존 문서 아님
- **해결**: `oaisword edit doc.docx --track-changes` 형식으로 사용

#### Redlining 워크플로우 실패
- **원인**: pandoc 미설치 또는 OOXML 구조 오류
- **해결**: pandoc 설치 확인, `.claude/skills/docx/ooxml.md` 참조

---

## 8. 관련 파일

### 8.1 기본 모드

| 구분 | 경로 |
|------|------|
| 스킬 정의 | `v/oaisword.md` |
| 가이드 | `v/guide/oaisword_guide.md` |
| 변환 스크립트 | `v/script/oaisreport_md2docx.py` |
| 견적서 변환기 | `v/template/quotation_docx.js` |
| 견적서 스타일 | `v/template/quotation_docx.json` |
| 견적서 가이드 | `v/template/quotation_docx.md` |
| 공통 가이드 | `v/guide/common_guide.md` |

### 8.2 플러그인 모드

| 구분 | 경로 |
|------|------|
| 플러그인 정의 | `.claude/skills/docx/SKILL.md` |
| OOXML 레퍼런스 | `.claude/skills/docx/ooxml.md` |
| docx-js 가이드 | `.claude/skills/docx/docx-js.md` |
| Document 라이브러리 | `.claude/skills/docx/scripts/document.py` |
| pack/unpack 스크립트 | `.claude/skills/docx/ooxml/scripts/` |
| XML 스키마 | `.claude/skills/docx/ooxml/schemas/` |
