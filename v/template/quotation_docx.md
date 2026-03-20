# quotation_docx - 견적서 워드 변환 템플릿

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | 2026-01-06 | 초기 버전 생성 |

---

## 개요

마크다운 형식의 견적서를 워드 문서(.docx)로 자동 변환하는 템플릿입니다.

## 파일 구성

| 파일 | 용도 |
|------|------|
| `quotation_docx.js` | 마크다운 파서 + 워드 생성기 |
| `quotation_docx.json` | 스타일 설정 (폰트, 색상, 여백 등) |
| `quotation_docx.md` | 사용 가이드 (본 문서) |

## 사용법

### 기본 사용

```bash
node v/template/quotation_docx.js <입력.md> [출력.docx] [config.json]
```

> **출력 경로 미지정 시**: 입력 파일과 같은 폴더에 같은 이름으로 `.docx` 파일 생성

### 예시

```bash
# 가장 간단한 사용 (출력 경로 자동 생성)
node v/template/quotation_docx.js doc/d0023_1차개발\ 견적.md
# → doc/d0023_1차개발 견적.docx 생성

# 출력 경로 지정
node v/template/quotation_docx.js doc/d0023_1차개발\ 견적.md tmp/reports/견적서.docx

# 커스텀 설정 사용
node v/template/quotation_docx.js doc/견적서.md tmp/견적서.docx v/template/custom_config.json
```

### oaisreport 연동

```bash
oaisreport word --source doc/d0023_1차개발\ 견적.md --out tmp/reports/견적서.docx
```

## 지원 마크다운 요소

| 요소 | 마크다운 문법 | 워드 변환 |
|------|-------------|----------|
| 제목 | `# ~ ######` | Heading 1~6 스타일 |
| 표 | `\| 열1 \| 열2 \|` | 테이블 (배경색 자동 적용) |
| 목록 | `- 항목` | 불릿 리스트 |
| 인용문 | `> 텍스트` | 들여쓰기 문단 |
| 이미지 | `![alt](경로)` | 이미지 삽입 |
| 문단 | 일반 텍스트 | 본문 스타일 |

## 표 자동 서식

| 조건 | 적용 스타일 |
|------|------------|
| 첫 번째 행 | 헤더 배경색 (파란색 계열) |
| "소계" 포함 셀 | 소계 배경색 (회색 계열) |
| "합계" 포함 셀 | 합계 배경색 (노란색 계열) |
| 금액 셀 (숫자+원) | 우측 정렬 |

## 스타일 설정 (quotation_docx.json)

### 문서 기본 설정

```json
{
  "document": {
    "defaultFont": "맑은 고딕",
    "defaultSize": 22,
    "margin": { "top": 1440, "right": 1200, "bottom": 1440, "left": 1200 }
  }
}
```

### 제목 스타일

```json
{
  "styles": {
    "title": { "size": 48, "bold": true, "color": "1F4E79" },
    "heading1": { "size": 32, "bold": true, "color": "1F4E79" },
    "heading2": { "size": 28, "bold": true, "color": "2E75B6" },
    "heading3": { "size": 24, "bold": true, "color": "404040" }
  }
}
```

### 표 스타일

```json
{
  "table": {
    "headerBackground": "E8F4FD",
    "subtotalBackground": "F0F0F0",
    "totalBackground": "FFF3CD",
    "borderColor": "CCCCCC"
  }
}
```

## 이미지 포함

마크다운에 이미지 문법을 사용하면 워드 문서에 이미지가 포함됩니다:

```markdown
![시안 1](./design/01_홈.png)
```

### 이미지 테이블 (부록용)

여러 이미지를 나란히 배치하려면:

```markdown
## 부록: 디자인 시안

| 시안 1 | 시안 2 | 시안 3 |
|--------|--------|--------|
| ![](01.png) | ![](02.png) | ![](03.png) |
```

## 의존성

```bash
npm install docx
```

## 관련 문서

- `v/oaisreport.md` - oaisreport 스킬 문서
- `doc/d0023_1차개발 견적.md` - 견적서 예시
