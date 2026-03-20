# oaispaper - 통합 학술 연구 스킬

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v29 | 2026-01-23 | **run 통합 강화**: 01_down 처리를 Phase 0으로 자동 포함, --skip-organize 옵션 추가, status에 01_down 대기 PDF 표시 |
| v28 | 2026-01-21 | **translator 에이전트 연동**: trans korean에 translator 에이전트 활용 섹션 추가 |
| v27 | 2026-01-21 | **trans 명령어 신설**: PDF 텍스트 추출 및 번역 (oaispaper_trans.py), 스크립트 참조 섹션 확장 |
| v26 | 2026-01-21 | **anal --deep 개선**: 폴더별 05_서베이.md 생성, 참고문헌 분석 포함, 증분 업데이트 |
| v25 | 2026-01-21 | **명령어 영문화**: 네트워크→net |
| v24 | 2026-01-21 | **run 통합** (9→6개): 다운→run --download, 정리→run --organize, fix→run --fix/--sync |
| v23 | 2026-01-21 | **명령어 대폭 통합** (18→9개): search(7→1), anal(3→1), fix+sync(2→1) |
| v22 | 2026-01-21 | **ref 명령어 신설**: 인용+인용관리 → ref 통합 (19→18개), 타임스탬프 기반 매핑 |
| v21 | 2026-01-21 | **명령어 통합** (36→19개): 검색(4→1), 네트워크(3→1), 분석(2→1), fix(4→1), 인용관리(5→1), 한영중복→영문만(status/fix/sync) |
| v20 | 2026-01-19 | `정리` 명령어 강화: 리스트 추가 후 자동 다운로드 시도까지 일괄 처리 명시 |
| v19 | 2026-01-17 | Part D 인용관리 추가 (d0105 통합): 인용매핑/검증/정리/정규화 명령어 |
| v18 | 2026-01-17 | 템플릿 보강: 풀 제목 추출 규칙, 서머리 없는 항목 처리 방식 추가 |
| v17 | 2026-01-17 | paper_list.md 형식 템플릿 추가 (B안: 헤더에 제목 통합) |
| v16 | 2026-01-17 | `정리` 워크플로우 보강: 처리 완료 리스트 → data/00_old 보관, 실패 사유 분류 |
| v15 | 2026-01-17 | `동기화` 명령어 추가: 서머리 → paper_list.md 메타데이터 동기화 |
| v14 | 2026-01-15 | MCP→Plugin 기반 변경 + run 명령어 통합 |
| v13 | 2026-01-14 | `run` 명령어 추가: 전체 논문 자동 정리 (서머리+영문추출+한글번역) |
| v12 | 2026-01-13 | 검사/정리 역할 분리: 검사→todo 기록, 정리→todo 기반 수정+history 이동 |
| v11 | 2026-01-13 | `정리` 명령어 확장: 02_paper 파일명 검사/수정 기능 추가 |
| v10 | 2026-01-13 | `정리` 서브명령어 추가 (옵션 없음, 전체 정리, 다운 실패→paper_list.md) |
| v09 | 2026-01-13 | 서브명령어 한글 통일 (search→검색, download→다운 등) |
| v08 | 2026-01-13 | status 명령어에 서브명령어 리스트 추가, 1.4 명령어 섹션 추가 |
| v07 | 2026-01-13 | 대기 폴더 경로 변경 (data/01_down → 01_down) |
| v06 | 2026-01-13 | a0013_oaispaper.md와 통합 (검색/다운로드 + 분석/서베이) |
| v05 | 2026-01-06 | fix 서브명령어 추가 (논문 오류 검사, 수정, d0004 연동) |
| v04 | 2026-01-06 | 가이드 내용 분리 (v/guide/oaispaper_guide.md) 및 참조 추가 |
| v03 | 2026-01-06 | 출력 파일 d0011→d0100_서베이.md 변경 |
| v02 | 2026-01-06 | 범용화: PRD 연동, 비교 분석, 인용 생성, d0004 연동 추가 |
| v01 | 2026-01-06 | 최초 생성 |

---

> 공통: `v/guide/common_guide.md` | 컨텍스트: `v/oaiscontext.md` | **가이드: `v/guide/oaispaper_guide.md`**

## 1. 개요

논문의 검색/다운로드부터 분석/서베이까지 전체 학술 연구 워크플로우를 지원합니다.

### 1.1 기능 영역

| 영역 | 설명 | 주요 명령어 |
|------|------|-----------|
| **Part A: 검색/다운로드** | 외부 학술 DB에서 논문 검색 및 다운로드 | `search`, `run --download`, `net` |
| **Part B: 분석/서베이** | 로컬 논문 폴더 분석 및 서베이 문서 생성 | `run`, `anal`, `ref` |

### 1.2 데이터 흐름

```
외부 DB (arXiv, SS, GS, PWC)
    ↓ search, run --download
01_down/ (PDF)
    ↓ run --organize
02_paper/ (표준 폴더)
    ↓ anal
doc/d0100_서베이.md
```

### 1.3 연동 문서

- `d0001_prd.md`: 연구 주제/키워드 자동 추출
- `d0004_todo.md`: 이슈 등록 (분석 불가, 오류 등)
- `d0100_서베이.md`: 서베이 출력 문서

### 1.4 명령어

| 명령어 | 설명 |
|--------|------|
| `oaispaper run` | **통합 실행**: 01_down 정리 + 서머리/영문/한글 (--skip-organize: 01_down 건너뛰기, --download: 다운, --fix: 유지보수) |
| `oaispaper status` | 서브명령어 리스트, 01_down 대기 PDF, paper 폴더 현황, d0100 상태, 논문 목록 |
| `oaispaper version` | 스킬 버전 정보 (v29) |
| `oaispaper search` | **통합 검색**: 키워드/초록/코드/데이터셋/트렌드/최신/학회 |
| `oaispaper anal` | **통합 분석**: 서베이 생성 (--compare: 비교, --add: 추가, --deep: 정밀) |
| `oaispaper net` | 인용 네트워크 분석 (인용논문/참고문헌/관계분석) |
| `oaispaper trans` | **텍스트 추출/번역**: PDF→영문, 영문→한글 (oaispaper_trans.py) |
| `oaispaper ref` | **인용 통합 관리**: 보고서 인용 검증→정리→정규화 자동 워크플로우 |

실행: `uv run python v/script/oaispaper_run.py [subcommand] [args]`

### 1.5 run 명령어 (통합 실행)

**명령어**: `oaispaper run [--옵션]`

기본 실행 시 미완료 논문을 자동 정리합니다. 옵션으로 다운로드/정리/유지보수/동기화 가능:

#### 처리 단계

```
Phase 0: 01_down 정리 (Organize)
    01_down/ PDF 파일 → 02_paper/ 이동
    → --skip-organize로 건너뛰기 가능
    ↓
Phase 1: 스캔 (Scan)
    02_paper/ 전체 폴더 검사
    → 미완료 논문 목록 생성
    ↓
Phase 2: 서머리 작성 (Summary)
    각 논문 폴더의 PDF 읽기
    → 00_서머리.md 내용 추출/작성
    ↓
Phase 3: 영문 추출 (English)
    PDF에서 전문 텍스트 추출
    → 03_전문(영어).md 생성
    ↓
Phase 4: 한글 번역 (Korean)
    03_전문(영어).md 읽기
    → 04_전문(한글).md 번역 작성
    ↓
Phase 5: 검증 (Validate)
    모든 파일 품질 검사
    → d0004_todo.md 업데이트
```

#### 품질 기준

| 파일 | 최소 조건 | 품질 검사 |
|------|----------|----------|
| 00_서머리.md | 500 bytes 이상 | 필수 섹션 존재, 템플릿 마커 없음 |
| 03_전문(영어).md | 1000 bytes 이상 | PDF 추출 완료, 깨진 문자 없음 |
| 04_전문(한글).md | 1000 bytes 이상 | 번역 완료, 템플릿 마커 없음 |

#### 실행 옵션

| 옵션 | 설명 | 예시 |
|------|------|------|
| (없음) | **기본**: 01_down 정리 + 서머리/영문추출/한글번역 | `oaispaper run` |
| `--skip-organize` | 01_down 정리 건너뛰고 02_paper만 처리 | `oaispaper run --skip-organize` |
| `--download` | PDF 다운로드 (arxiv/SS/GS/PWC) | `oaispaper run --download arxiv:2301.12345` |
| `--organize` | 01_down 전체 처리 (이동+다운+실패처리) | `oaispaper run --organize` |
| `--fix` | 02_paper 유지보수 (검사/수정) | `oaispaper run --fix` |
| `--sync` | 서머리→paper_list.md 메타데이터 동기화 | `oaispaper run --sync` |
| `--limit N` | 처리할 최대 논문 수 | `oaispaper run --limit 10` |
| `--phase P` | 특정 단계만 실행 | `oaispaper run --phase summary` |
| `--folder ID` | 특정 폴더만 처리 | `oaispaper run --folder 251106-0001` |
| `--dry-run` | 실행 없이 계획만 출력 | `oaispaper run --dry-run` |
| `--check-only` | 검사만 수행 (--fix와 함께) | `oaispaper run --fix --check-only` |

#### 서브에이전트 활용

대량 처리 시 서브에이전트를 병렬로 활용:

| 단계 | 에이전트 | 병렬 |
|------|---------|:----:|
| 스캔 | Explore | O |
| 서머리 | academic-researcher | O |
| 영문 추출 | data-analyst | O |
| 한글 번역 | task-executor | O |
| 검증 | task-checker | - |

#### 완료 조건

- 모든 논문에 4개 필수 파일 존재 (00, 01, 03, 04)
- 각 파일이 품질 기준 충족
- d0004_todo.md 오류 건수 0건

### 1.6 동기화 기능 (run --sync)

**명령어**: `oaispaper run --sync`

서머리 파일(00_서머리.md)에서 메타데이터를 추출하여 paper_list.md의 빈 필드를 채웁니다.

> **Note**: 기존 `동기화`, `fix --sync` 명령어는 `run --sync` 옵션으로 통합되었습니다.

#### 데이터 흐름

```
02_paper/{folder_id}/{folder_id}_00_*_서머리.md
    ↓ 추출 (저자, 연도, 출처)
02_paper/paper_list.md 업데이트
```

#### 추출 대상 필드

| 서머리 필드 | paper_list 필드 | 추출 패턴 |
|------------|----------------|----------|
| `저자:` | 저자 | `- 저자: {value}` 또는 `저자: {value}` |
| `출처:` | 출처/연도 | arXiv, IEEE, MDPI 등 + 연도 추출 |
| `논문 제목:` | 제목 | 검증용 (폴더 ID와 매칭) |

#### 실행 옵션

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--dry-run` | 변경 없이 미리보기 | `oaispaper run --sync --dry-run` |
| `--folder ID` | 특정 폴더만 처리 | `oaispaper run --sync --folder 230312-1648` |
| `--force` | 기존 값도 덮어쓰기 | `oaispaper run --sync --force` |

#### 워크플로우

1. **정리 후 동기화**: `oaispaper run --organize` 완료 후 `oaispaper run --sync` 실행
2. **run 후 동기화**: `oaispaper run` 완료 후 `oaispaper run --sync` 실행

### 1.7 trans 명령어 (텍스트 추출/번역)

**명령어**: `oaispaper trans [english|korean]`

PDF 텍스트 추출 및 번역 자동화 스크립트입니다.

#### 서브명령어

| 명령어 | 설명 |
|--------|------|
| `english` | PDF → 03_전문(영어).md 추출 |
| `korean` | 03_전문(영어).md → 04_전문(한글).md 번역 템플릿 생성 |

#### 실행 옵션

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--folder ID` | 특정 폴더만 처리 | `oaispaper trans english --folder 260121-0001` |
| `--force` | 기존 파일 덮어쓰기 | `oaispaper trans english --force` |

#### english 옵션 (영문 추출)

```bash
# 전체 논문 영문 추출
oaispaper trans english

# 특정 폴더만 추출
oaispaper trans english --folder 260121-0001

# 기존 파일 덮어쓰기
oaispaper trans english --force
```

**처리 과정**:
1. 각 논문 폴더의 PDF 스캔
2. PyPDF2로 텍스트 추출
3. `{CODE}_03_{Title3}_전문(영어).md` 생성
4. 품질 검사 (1000 bytes 이상)

#### korean 옵션 (한글 번역)

```bash
# 전체 논문 한글 번역 템플릿 생성
oaispaper trans korean

# 특정 폴더만 생성
oaispaper trans korean --folder 260121-0001

# 기존 파일 덮어쓰기
oaispaper trans korean --force
```

**처리 과정**:
1. 각 논문 폴더의 03_전문(영어).md 스캔
2. 번역 템플릿 생성 (TODO 마커 포함)
3. `{CODE}_04_{Title3}_전문(한글).md` 생성

#### translator 에이전트 활용 (권장)

한글 번역 템플릿 생성 후, **translator 에이전트**를 사용하여 고품질 번역 수행:

```bash
# 1. 번역 템플릿 생성
oaispaper trans korean --folder 260121-0001

# 2. translator 에이전트로 번역 요청
# Claude Code에서:
# "translator 에이전트를 사용해서 02_paper/260121-0001/04_전문(한글).md 번역해줘"
```

**translator 에이전트 기능**:
- 학술 논문 전문 용어 일관성 유지
- 수식/코드 블록 원문 보존
- 번역투 없는 자연스러운 한국어
- 용어집 기반 일관된 번역

**에이전트 정의**: `v/agent/translator.md`

**⚠️ 참고**: translator 에이전트 미사용 시 수동 번역 필요 (v/guide/oaispaper_guide.md 섹션 1.3 참조)

### 1.8 paper_list.md 형식 템플릿

**파일 위치**: `02_paper/paper_list.md`

#### 문서 헤더 템플릿

```markdown
# d0014_논문리스트.md - 논문 목록

## 문서 이력
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| vXX | YYYY-MM-DD | 변경 내용 설명 |

---

## 총 논문수
**N개** (완료: X개, 미완료: Y개)

---

## 논문리스트
```

#### 논문 항목 템플릿 (B안)

```markdown
### {폴더ID} - {풀 제목}
- **키워드**: {키워드1}, {키워드2}, {키워드3}, ...
- **저자**: {저자명} | **연도**: {YYYY} | **출처**: {출처}
- **등록일**: {YYYY-MM-DD} | **완료**: {O/X}
```

#### 필드 설명

| 필드 | 설명 | 예시 |
|------|------|------|
| 폴더ID | `YYMMDD-HHMM` 형식 | `230312-1648` |
| 풀 제목 | 논문 전체 제목 (영문) | `Holistically-Nested Edge Detection` |
| 키워드 | 서머리에서 추출, 최대 5개 | `엣지검출, 딥러닝, CNN` |
| 저자 | 주저자 또는 전체 저자 | `Saining Xie, Zhuowen Tu` |
| 연도 | 출판 연도 | `2015` |
| 출처 | arXiv ID, 학회명, 저널명 등 | `arXiv:1504.06375` |
| 등록일 | 폴더 생성일 | `2023-03-12` |
| 완료 | 분석 완료 여부 | `O` 또는 `X` |

#### 예시

```markdown
### 230312-1648 - Holistically-Nested Edge Detection
- **키워드**: 엣지검출, 딥러닝, CNN, 다중스케일, 계층적특징학습
- **저자**: Saining Xie, Zhuowen Tu | **연도**: 2015 | **출처**: arXiv:1504.06375
- **등록일**: 2023-03-12 | **완료**: O

### 251202-0001 - Deep Learning for Crack Detection
- **저자**: - | **연도**: - | **출처**: -
- **등록일**: 2025-12-02 | **완료**: X
```

> **Note**: 키워드가 없는 항목은 `**키워드**` 라인 생략. 빈 필드는 `-`로 표시.

#### 풀 제목 추출 규칙

**추출 우선순위** (서머리 파일에서):
1. 테이블 형식: `| 제목 | Full Title Here |`
2. 볼드 제목: `- **제목**: Full Title Here`
3. 볼드 논문 제목: `- **논문 제목**: Full Title Here`
4. 리스트 형식: `- 논문 제목: Full Title Here`
5. H1 헤더: `# Full Title Here` (서머리/Summary 제외)

**서머리 없는 항목**: 폴더ID만 표시 (파일명 기반 축약 제목 사용 금지)

```markdown
### 240316-1916
- **저자**: - | **연도**: 2023 | **출처**: -
- **등록일**: 2024-03-16 | **완료**: O
```

**제목 품질 기준**:
- 최소 10자 이상
- 저자명, 기관명, 저작권 문구 제외
- 저널 ID, 파일명 코드 제외

#### 다운로드 불가 섹션 템플릿

```markdown
## 다운로드 불가

| No. | DOI/arXiv | 논문 제목 | 연도 | 출처 | 실패 사유 | 등록일 |
|:---:|-----------|----------|:----:|------|----------|--------|
| 1 | 10.1111/mice.12263 | Deep Learning Crack | 2017 | CACAIE | API 오류 | 2026-01-17 |
```

---

# Part A: 논문 검색/다운로드

## 2. 지원 데이터 소스

### 2.1 Plugin 및 Agent

| 소스 | 도구 | 주요 기능 |
|------|------|----------|
| **academic-researcher** | Task agent | 논문 검색, 인용 분석, 저자 검색, 학술 DB 조회 |
| **WebSearch** | Built-in | Google Scholar, arXiv 등 학술 검색 |
| **WebFetch** | Built-in | 논문 메타데이터 추출 |

> **Note**: MCP 서버 대신 Plugin과 Agent를 사용합니다. `academic-researcher` 에이전트가 ArXiv, PubMed, Google Scholar 등 학술 데이터베이스를 검색합니다.

### 2.2 API (Python 스크립트)

| API | 용도 |
|-----|------|
| **arXiv API** | 프리프린트 검색 (직접 API 호출) |
| **Unpaywall API** | 페이월 우회, 오픈 액세스 버전 찾기 |

---

## 3. 검색/다운로드 명령어

| 명령어 | 설명 |
|--------|------|
| `oaispaper search [query]` | **통합 검색**: 키워드/초록/코드/데이터셋/트렌드/최신/학회 |
| `oaispaper net [id]` | **통합 인용분석** (인용논문/참고문헌/관계) |

> **Note**: PDF 다운로드는 `oaispaper run --download [id]` 사용

### 3.1 search 옵션 (통합 검색)

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--mode` | 검색 모드 | `--mode keyword\|abstract\|code\|dataset\|trend\|recent\|conf` |
| `--type` | 검색 유형 (keyword 모드) | `--type keyword\|title\|author` (기본: keyword) |
| `--년도` | 연도 범위 | `--년도 2020-2024` |
| `--인용` | 최소 인용 수 | `--인용 100이상` |
| `--정렬` | 정렬 기준 | `--정렬 인용순\|최신순\|관련순` |
| `--오픈액세스` | OA 논문만 | `--오픈액세스` |
| `--개수` | 결과 수 제한 | `--개수 10` |
| `--분야` | 연구 분야/카테고리 | `--분야 "cs.CV"` |
| `--학회` | 학회명 (conf 모드) | `--학회 NeurIPS --년도 2024` |

> **Note**: `--mode` 생략 시 기본값은 `keyword` (키워드 검색)

### 3.2 net 옵션 (통합 인용분석)

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--action` | 분석 유형 | `--action citing\|cited\|both` (기본: both) |
| `--depth` | 탐색 깊이 | `--depth 2` (기본: 1) |
| `--개수` | 결과 수 제한 | `--개수 20` |

> **Note**: `--action citing` = 인용논문, `--action cited` = 참고문헌, `--action both` = 전체 네트워크

### 3.3 검색 예시

```bash
# 키워드 검색 (기본)
oaispaper search "transformer attention mechanism"
oaispaper search "crack segmentation" --년도 2020-2024 --인용 50이상

# 제목 검색
oaispaper search "Attention Is All You Need" --type title

# 저자 검색
oaispaper search "Yoshua Bengio" --type author

# 초록 조회
oaispaper search arxiv:1706.03762 --mode abstract

# 코드 검색
oaispaper search "Attention Is All You Need" --mode code

# 데이터셋 검색
oaispaper search arxiv:1706.03762 --mode dataset

# 트렌드 분석
oaispaper search --mode trend --분야 cs.CV

# 최신 논문
oaispaper search --mode recent --분야 cs.LG --개수 20

# 학회 논문
oaispaper search --mode conf --학회 NeurIPS --년도 2024

# 논문 다운로드
oaispaper run --download arxiv:2301.12345
oaispaper run --download doi:10.1038/nature12373

# 인용 네트워크 분석 (통합)
oaispaper net arxiv:1706.03762                    # 전체 네트워크
oaispaper net arxiv:1706.03762 --action citing    # 인용논문만
oaispaper net arxiv:1706.03762 --action cited     # 참고문헌만
oaispaper net arxiv:1706.03762 --depth 2          # 2단계 깊이
```

---

## 4. 도구 매핑

### 4.1 명령어-도구 매핑

| 명령어 | 사용 도구 | 설명 |
|--------|----------|------|
| search | `academic-researcher` agent | 통합 검색 (--mode로 keyword/abstract/code/dataset/trend/recent/conf 선택) |
| run --download | arXiv API / Unpaywall | PDF 다운로드 |
| net | `academic-researcher` agent | 통합 인용분석 (인용논문/참고문헌/관계) |

### 4.2 Agent 사용 방법

```yaml
academic-researcher:
  용도: 논문 검색, 인용 분석, 학술 문헌 조사
  호출: Task tool with subagent_type='academic-researcher'
  기능:
    - ArXiv, PubMed, Google Scholar 검색
    - 논문 분석 및 요약
    - 인용 추적 및 문헌 분석
    - 학술 키워드 추출
```

---

## 5. 다운로드 워크플로우

### 5.1 arXiv 논문

```bash
oaispaper run --download arxiv:2301.12345
# → arXiv API로 PDF URL 조회
# → 01_down/{arxiv_id}.pdf 다운로드
```

### 5.2 일반 논문 (DOI)

```bash
oaispaper run --download doi:10.1038/nature12373
# 1. Unpaywall API로 오픈 액세스 버전 검색
# 2. is_oa: true → best_oa_location.url_for_pdf 사용
# 3. 01_down/{doi_safe}.pdf로 저장
```

### 5.3 페이월 우회 실패 시

1. arXiv/bioRxiv 프리프린트 검색
2. 저자 개인 페이지 확인
3. 기관 접근권 사용

---

# Part B: 논문 분석/서베이

## 6. 분석/서베이 명령어

| 명령어 | 설명 |
|--------|------|
| `oaispaper status` | 서브명령어 리스트, paper 폴더 현황, 논문 목록, d0100 상태 |
| `oaispaper anal` | **통합 분석**: 서베이 생성 (--compare: 비교, --add: 추가, --deep: 정밀) |
| `oaispaper ref` | 보고서 인용 검증→정리→정규화 자동 워크플로우 |

> **Note**: `정리`→`run --organize`, `fix`→`run --fix`로 통합되었습니다.

### 6.1 anal 옵션 (통합 분석)

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--compare` | 논문 간 비교 분석 (모델, 성능, 방법론) | `oaispaper anal --compare` |
| `--add [폴더]` | 새 논문 추가 분석 → 기존 d0100에 병합 | `oaispaper anal --add 251108-1400` |
| `--deep` | **폴더별 정밀 서베이** → 05_서베이.md 생성 | `oaispaper anal --deep` |
| `[폴더] --deep` | 특정 폴더만 정밀 서베이 | `oaispaper anal 251108-1400 --deep` |
| `--topic` | 연구 주제 오버라이드 | `--topic "객체 탐지"` |
| `--keywords` | 키워드 오버라이드 | `--keywords "YOLO,ResNet"` |
| `--threshold` | 관련성 임계값 (기본 2) | `--threshold 3` |
| `--dry-run` | 실행 없이 계획만 출력 | |
| `--verbose` | 상세 로그 출력 | |

### 6.2 run --fix 옵션 (유지보수)

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--sync` | 서머리 → paper_list.md 메타데이터 동기화 | `oaispaper run --sync` |
| `--check-only` | 검사만 수행 (수정 안함) | `oaispaper run --fix --check-only` |
| `--auto-fix` | 자동 수정 가능한 오류 수정 | `oaispaper run --fix --auto-fix` |
| `--delete-broken` | 깨진 파일 삭제 | `oaispaper run --fix --delete-broken` |
| `--clean-duplicates` | 중복 파일 정리 | `oaispaper run --fix --clean-duplicates` |
| `--folder` | 특정 폴더만 검사 | `oaispaper run --fix --folder 251108-1400` |

---

## 7. 실행 워크플로우

### 7.1 분석 흐름

```
1. PRD에서 연구 주제/키워드 추출 (또는 옵션 사용)
2. paper/ 폴더 스캔 → 논문 목록 생성
3. 각 논문 서머리 읽기 → 관련성 점수 계산
4. 임계값 이상 → 상세 분석 (한글 전문 포함)
5. d0100_서베이.md 생성/업데이트
6. 분석 불가 논문 → d0004에 이슈 등록
```

### 7.2 정밀분석 흐름 (anal --deep)

**명령어**: `oaispaper anal --deep` 또는 `oaispaper anal [폴더명] --deep`

각 논문 폴더에 **05_서베이.md**를 생성하는 개별 정밀 서베이 기능.

#### 입력 소스

```
02_paper/{folder_id}/
    ├── 01_*.pdf           ← PDF 원문
    ├── 03_전문(영어).md    ← 영문 전문
    ├── 04_전문(한글).md    ← 한글 번역
    └── 참고문헌 섹션        ← 인용 논문 분석
```

#### 출력

```
02_paper/{folder_id}/
    └── 05_서베이.md        ← 정밀 서베이 결과
```

#### 처리 로직

```
1. 폴더 스캔 (전체 or 지정 폴더)
2. 각 폴더별:
   ├── 05_서베이.md 존재?
   │   ├── YES → 기존 내용 분석, 추가 서베이 필요 여부 판단
   │   │         ├── 추가 필요 → 내용 보강
   │   │         └── 불필요 → SKIP
   │   └── NO → 신규 생성
   │
   ├── PDF + 전문(영어/한글) 정밀 분석
   ├── 참고문헌 추출 및 분석
   └── 05_서베이.md 저장
```

#### 05_서베이.md 구조

```markdown
# {논문 제목} - 정밀 서베이

## 1. 핵심 요약
## 2. 연구 배경 및 동기
## 3. 방법론 상세
## 4. 실험 및 결과
## 5. 참고문헌 분석
   - 주요 인용 논문
   - 관련 연구 맵
## 6. 한계점 및 향후 연구
## 7. 메모/코멘트
```

#### 사용 예시

```bash
# 전체 폴더 정밀 서베이
oaispaper anal --deep

# 특정 폴더만 정밀 서베이
oaispaper anal 251108-1400 --deep
```

### 7.3 정리 흐름 (run --organize)

**실행**: `oaispaper run --organize`

> **핵심**: 리스트 추가 후 별도 다운로드 명령 없이 `run --organize` 한 번으로 다운로드까지 자동 완료

정리 명령은 3가지 작업을 **순차적으로 자동** 수행합니다:
1. 01_down/ PDF 파일 → 02_paper/ 이동
2. **01_down/ 다운로드 리스트의 모든 논문 자동 다운로드 시도** → 성공/실패 처리
3. d0004_todo.md 기반 오류 수정 → d0010_history.md로 이동

#### Phase 1: PDF 파일 처리

```
01_down/ 스캔
    ↓
각 PDF 파일에 대해 반복:
    1. 메타데이터 추출 (제목, 저자, 연도, arXiv ID 등)
    2. 02_paper/에 표준 폴더 생성 (YYMMDD-HHMM)
    3. PDF 이동 및 표준 파일 생성
    4. 01_down/에서 해당 PDF 삭제
    ↓
다음 파일 처리
```

#### Phase 2: 다운로드 리스트 처리

```
01_down/*.md (다운로드 리스트) 스캔
    ↓
각 논문 항목에 대해 반복:
    1. 다운로드 시도 (arXiv 직접, DOI→Unpaywall API)
    2-a. 성공 → 02_paper/에 폴더 생성 및 정리
    2-b. 실패 → 02_paper/paper_list.md "다운로드 불가" 섹션에 추가
    ↓
다음 항목 처리
    ↓
처리 완료된 리스트 파일 → data/00_old/ 이동 (보관)
```

**다운로드 불가 기록 형식**:
```markdown
## 다운로드 불가
| No. | DOI/arXiv | 논문 제목 | 연도 | 출처 | 실패 사유 | 등록일 |
|:---:|-----------|----------|:----:|------|----------|--------|
| 1 | 10.1111/mice.12263 | Deep Learning Crack | 2017 | CACAIE | API 오류 | 2026-01-17 |
```

**실패 사유 분류**:
- `API 오류`: Unpaywall API 응답 실패 (422, 404 등)
- `MDPI 차단`: MDPI 사이트 봇 차단 (403)
- `페이월`: 오픈 액세스 버전 없음
- `링크 만료`: 다운로드 URL 무효

#### Phase 3: d0004 기반 오류 수정

```
d0004_todo.md "논문 오류" 섹션 읽기
    ↓
각 오류 항목에 대해 반복:
    1. 오류 유형 확인 (파일명, 인코딩, 내용 등)
    2. 자동 수정 가능 여부 판단
    3-a. 자동 수정 → 파일명 변경 등 실행
    3-b. 수동 수정 필요 → 건너뛰기 (메시지 출력)
    4. 수정 완료된 항목 → d0010_history.md로 이동
    ↓
다음 항목 처리
    ↓
수정 결과 리포트 출력
```

#### 파일명 수정 규칙

| 오류 유형 | 현재 파일명 | 수정 후 파일명 |
|----------|------------|---------------|
| Type A | `00_서머리.md` | `{CODE}_00_{Title3}_서머리.md` |
| Type A | `03_전문(영어).md` | `{CODE}_03_{Title3}_전문(영어).md` |
| Type A | `04_전문(한글).md` | `{CODE}_04_{Title3}_전문(한글).md` |
| Type B | `{CODE}_03_전문(영어).md` | `{CODE}_03_{Title3}_전문(영어).md` |
| Type B | `{CODE}_04_전문(한글).md` | `{CODE}_04_{Title3}_전문(한글).md` |

**Title3 추출 방법**: PDF 파일명에서 추출 (예: `251224-1001_01_Modern_Mathematics_Deep_Learning.pdf` → `Modern_Mathematics_Deep`)

#### 결과 파일

```
02_paper/
├── paper_list.md              # 다운로드 불가 논문 목록
└── 251224-1001/
    ├── 251224-1001_00_Modern_Mathematics_Deep_서머리.md
    ├── 251224-1001_01_Modern_Mathematics_Deep_Learning.pdf
    ├── 251224-1001_03_Modern_Mathematics_Deep_전문(영어).md
    └── 251224-1001_04_Modern_Mathematics_Deep_전문(한글).md
```

### 7.4 검사 흐름

**목적**: 02_paper 폴더의 모든 문제점을 검사하여 d0004_todo.md에 기록

**실행**: `oaispaper 검사`

```
02_paper/ 전체 폴더 스캔
    ↓
각 폴더에 대해 반복:
    1. 파일명 규칙 검사
    2. 파일 존재 여부 검사
    3. 인코딩 검사
    4. 내용 품질 검사
    ↓
신규 오류 발견 시 → d0004_todo.md "논문 오류" 섹션에 등록
    ↓
검사 결과 리포트 출력
```

#### 검사 항목

| # | 검사 항목 | 검사 내용 | 수정 방식 |
|---|----------|----------|----------|
| 1 | 파일명 규칙 | `{CODE}_00_{Title3}_서머리.md` 등 형식 준수 | 자동 |
| 2 | PDF 존재 | 원본 PDF 파일 존재 여부 | 수동 |
| 3 | 인코딩 검사 | UTF-8 인코딩, 깨진 문자 없음 | 수동 |
| 4 | 영어 전문 품질 | PDF에서 제대로 추출되었는지 | 수동 |
| 5 | 한글 번역 품질 | 번역 완료 여부 | 수동 |
| 6 | 서머리 품질 | 필수 섹션 존재, 내용 충실도 | 수동 |

#### d0004_todo.md 등록 형식

```markdown
## 논문 오류

### 파일명 오류 (자동 수정)
- [ ] 251224-1001: `00_서머리.md` → `251224-1001_00_Modern_Mathematics_Deep_서머리.md`
- [ ] 230312-1648: `230312-1648_03_전문(영어).md` → `230312-1648_03_Attention_Is_All_전문(영어).md`

### 내용 오류 (수동 수정)
- [ ] 240101-1333: 한글 번역 미완료
- [ ] 240216-1512: 서머리 섹션 누락 (방법론)
```

#### 검사 옵션

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--folder` | 특정 폴더만 검사 | `oaispaper 검사 --folder 251108-1400` |
| `--type` | 특정 오류 유형만 검사 | `oaispaper 검사 --type filename` |

---

## 8. 비교 워크플로우

```bash
# 특정 논문들 비교
oaispaper anal --compare 251201-0036 251130-2321 251108-1402

# 전체 관련 논문 비교
oaispaper anal --compare --all

# 특정 측면으로 비교
oaispaper anal --compare --focus performance
oaispaper anal --compare --focus architecture
```

### 비교 출력 예시

```markdown
## 논문 비교 분석

### 성능 비교
| 논문 | Dataset | IoU | F1 | mAP | 파라미터 |
|------|---------|-----|----|----|---------|
| A | CrackDataset | 0.85 | 0.90 | - | 25M |
| B | PASCAL | 0.82 | 0.88 | 0.75 | 45M |

### 아키텍처 비교
| 논문 | Backbone | 특징 | 장점 | 단점 |
|------|----------|------|------|------|
| A | ResNet34 | Skip connection | 경량 | 저해상도 |
| B | Swin-T | Attention | 글로벌 컨텍스트 | 연산량 |
```

---

## 9. 인용 워크플로우

보고서 인용 관리는 `ref` 명령어로 통합되었습니다.

```bash
# 보고서 인용 검증/정리/정규화 (자동)
oaispaper ref doc/d0910_보고서.md
```

상세 내용은 **Section 16. ref 명령어** 참조.

---

# Part C: 통합 워크플로우

## 10. 전체 워크플로우

### 10.1 논문 수집 → 분석 → 서베이

```
1. 키워드 기반 검색
    oaispaper search "crack segmentation deep learning" --년도 2020-2024

2. 유망 논문 다운로드
    oaispaper run --download arxiv:2301.12345

3. 논문 정리 (01_down → 02_paper)
    oaispaper run --organize

4. 텍스트 추출
    oaispaper trans english        # PDF → 영문 전문
    oaispaper trans korean         # 영문 전문 → 한글 번역 템플릿
    # (한글 번역 템플릿 생성 후 수동 번역 필요)

5. 서베이 생성
    oaispaper anal           # 서머리 기반
    oaispaper anal --deep    # 폴더별 05_서베이.md 생성

6. 품질 검사
    oaispaper run --fix --check-only

7. 비교 분석
    oaispaper anal --compare --all --focus performance
```

### 10.2 인용 기반 확장

```
1. 핵심 논문 인용 분석
   oaispaper net arxiv:1706.03762 --action citing

2. 인용 네트워크 시각화
   oaispaper net arxiv:1706.03762 --depth 2

3. 관련 논문 다운로드
   oaispaper run --download arxiv:xxxx.xxxxx

4. 서베이 업데이트
   oaispaper anal --add [새폴더]
```

---

## 11. 병렬 처리

### 11.1 아키텍처

```
메인 에이전트 (조율)
    ├── Agent 1: 검색 (search)
    ├── Agent 2: 서머리 분석 (anal)
    ├── Agent 3: 전문 분석 (anal --deep)
    ├── Agent 4: PDF 분석 (anal --deep)
    └── Agent 5: 비교/인용 생성 (anal --compare)
```

### 11.2 서브에이전트 매핑

| 작업 | 에이전트 | 병렬 |
|------|---------|:----:|
| 논문 검색 | academic-researcher | O |
| 서머리 분석 | Explore | O |
| 전문 분석 | academic-researcher | O |
| PDF 분석 | data-analyst | O |
| 문서 생성 | task-executor | - |

---

## 12. 완료 조건

| 조건 | 검증 방법 |
|------|----------|
| d0100 생성/업데이트 | 파일 존재 및 버전 증가 |
| 관련 논문 전체 분석 | 참고 목록에 누락 없음 |
| d0004 이슈 등록 | 분석 불가 논문 기록 |
| PRD 연동 확인 | 연구 주제 일치 |

---

## 13. 관련 문서

| 문서 | 용도 |
|------|------|
| **v/guide/oaispaper_guide.md** | **논문 관리 및 분석 가이드** (필독) |
| doc/d0001_prd.md | 연구 주제 참조 |
| doc/d0100_서베이.md | 생성 문서 |
| doc/d0004_todo.md | 이슈 등록 |
| v/guide/common_guide.md | 공통 가이드 |

---

## 14. 사용 예시

### Part A: 검색/다운로드

```bash
# 키워드 검색
oaispaper search "transformer attention" --년도 2020-2024 --개수 20

# 저자 검색 (통합)
oaispaper search "Kaiming He" --type author

# 다운로드
oaispaper run --download arxiv:2301.12345

# 인용 네트워크 분석 (통합)
oaispaper net arxiv:1706.03762
oaispaper net arxiv:1706.03762 --action citing --depth 2

# 트렌드
oaispaper search --mode trend --분야 cs.CV
oaispaper search --mode recent --분야 cs.LG
```

### Part B: 분석/서베이

```bash
# 현황 확인 (목록 포함)
oaispaper status

# 01_down → 02_paper 정리
oaispaper run --organize  # 전체 정리 (PDF + 다운로드 리스트)

# 텍스트 추출/번역
oaispaper trans english        # PDF → 영문 전문 추출
oaispaper trans korean         # 영문 전문 → 한글 번역 템플릿 생성
oaispaper trans english --folder 260121-0001  # 특정 폴더만
oaispaper trans english --force  # 기존 파일 덮어쓰기

# 서베이 생성 (anal 통합)
oaispaper anal
oaispaper anal --deep  # 폴더별 05_서베이.md 생성

# 오류 검사/수정
oaispaper run --fix --check-only
oaispaper run --fix --auto-fix
oaispaper run --fix --delete-broken --clean-duplicates

# 비교 분석
oaispaper anal --compare --all --focus performance

# 인용 관리 (자동)
oaispaper ref doc/d0910_보고서.md
```

---

*통합: v06 (2026-01-13) - a0013_oaispaper.md 병합*
*한글 명령어: v09 (2026-01-13) - 서브명령어 한글 통일*
*정리 명령어: v10 (2026-01-13) - 01_down → 02_paper 이동/정리 추가*
*검사/정리 분리: v12 (2026-01-13) - 검사→todo 기록, 정리→todo 기반 수정+history 이동*
*ref 통합: v22 (2026-01-21) - 인용+인용관리 → ref 단일 명령어*

---

# Part D: 인용 관리 (보고서 작성용)

## 15. 인용 관리 개요

### 15.1 목적

보고서/논문 작성 시 인용의 체계적 관리 및 검증 프로세스를 지원합니다.

**핵심 원칙**: "검증 가능한 인용만 포함 | 원문 확인 가능성 | 인용 무결성 보장"

### 15.2 데이터 흐름

```
[Part A-C 워크플로우]
02_paper/ (논문 폴더)
    ↓ 분석, 서베이
d0100_서베이.md
    ↓
[Part D 인용 관리]
보고서 작성 (d0910)
    ↓ oaispaper ref (자동)
    │  ├─ 매핑 테이블 생성
    │  ├─ 인용 검증
    │  ├─ 검증 불가 제거 + 재번호
    │  └─ 형식 정규화
    ↓
최종 보고서 (d0910_v02.md)
```

### 15.3 연동 문서

| 문서 | 용도 |
|------|------|
| `02_paper/` | 논문 원문 저장소 (서머리에서 메타데이터 추출) |
| `d0910_보고서.md` | 메인 보고서 (인용 포함) |
| `d0910_보고서_v02.md` | ref 처리 후 결과물 |

---

## 16. ref 명령어 (통합 인용 관리)

**명령어**: `oaispaper ref [보고서파일]`

보고서의 인용을 **자동으로 검증→정리→정규화**하는 통합 명령어입니다.

### 16.1 사용법

```bash
oaispaper ref doc/d0910_보고서.md
```

### 16.2 자동 실행 워크플로우

```
Step 1: 매핑 테이블 생성
    02_paper/ 스캔 → 폴더명(타임스탬프)과 서머리에서 메타데이터 추출
    ↓
Step 2: 인용 검증
    보고서의 "[001]" 인용 → 매핑 테이블과 대조
    ↓
Step 3: 문제 발견 시 수정 여부 질문
    검증 불가 인용 목록 표시 → (Y/n) 확인
    ↓
Step 4: 자동 정리
    검증 불가 인용 제거 + 번호 재부여 + 형식 정규화
    ↓
Step 5: 결과 저장
    새 버전 파일 저장 (예: d0910_보고서_v02.md)
```

### 16.3 매핑 테이블 구조

02_paper/ 폴더 구조에서 자동 생성:

```
02_paper/
├── 240312-1611/                    ← 코드 (타임스탬프)
│   └── 240312-1611_00_서머리.md    ← 메타데이터 소스
└── 240401-0837/
    └── 240401-0837_00_서머리.md
```

**서머리에서 추출**:
```markdown
# 제목
## 기본 정보
- **저자**: Ham (Ji-Wan Ham)
- **발행년도**: 2022년 2월
```

**생성되는 매핑**:

| 번호 | 코드 | 저자 | 연도 | 제목 (앞 30자) |
|------|------|------|------|----------------|
| [001] | 240312-1611 | Ham | 2022 | 멀티스케일 멀티레벨... |
| [002] | 240401-0837 | Zhang | 2024 | Deep Motion Deblur... |

### 16.4 출력 예시

```
[ref] doc/d0910_보고서.md 인용 검증 시작...

[매핑] 02_paper/ 스캔: 45개 논문 발견
[검증] 보고서 인용 분석 중...

결과:
  ✅ 검증 완료: 42개
  ❌ 검증 불가: 3개
     - Kim (2023)[003]: 논문 파일 없음
     - Lee (2022)[015]: 서머리 없음
     - Park (2021)[022]: 제목 추출 불가
  ⚠️ 형식 오류: 2개 (중복 표기)

수정하시겠습니까? (Y/n): Y

[정리] 검증 불가 인용 3개 제거
[정리] 인용 번호 재부여: [001]~[042]
[정규화] 중복 표기 2개 수정
[저장] doc/d0910_보고서_v02.md

완료: 42개 인용, 무결성 100%
```

### 16.5 검증 기준

```
✅ 검증 가능:
- 02_paper/{코드}/ 폴더 존재
- {코드}_00_서머리.md 파일 존재
- 서머리에서 제목/저자/연도 추출 가능

❌ 검증 불가:
- 폴더 없음
- 서머리 없음
- 메타데이터 추출 불가
```

---

## 17. 인용 형식 규칙

### 17.1 올바른 인용 형식

```markdown
✅ 올바른 형식:
Zhang et al. (2022)[001]
Park et al. (2014)[006]
Zhang & Wang (2024)[003]
Kim (2023)[012]
```

### 17.2 피해야 할 형식

```markdown
❌ 잘못된 형식:
Zhang et al. (2022)[240312-1611][001]  # 코드 중복
Park 등 (2014)Park et al. (2014)[006]  # 한영 중복
Zhang et al. (2022)Zhang et al. (2022)[001]  # 전체 중복
[001] Zhang et al. (2022)  # 번호 위치 오류
```

### 17.3 형식 규칙

| 요소 | 규칙 | 예시 |
|------|------|------|
| 저자명 | 영문 표기, et al. 사용 | `Zhang et al.` |
| 연도 | 4자리 숫자 괄호 | `(2022)` |
| 번호 | 3자리 대괄호, 등장 순서 | `[001]` |
| 복수 저자 | `&` 연결 | `Zhang & Wang` |

---

## 18. ref 워크플로우

### 18.1 신규 보고서 작성 시

```bash
# 1. 논문 수집/분석
oaispaper search "transformer"
oaispaper run --download arxiv:2301.12345
oaispaper run --organize
oaispaper anal

# 2. 보고서 작성 (수동)
# d0910_보고서.md에 인용 추가

# 3. 인용 검증/정리 (한 번에)
oaispaper ref doc/d0910_보고서.md
```

### 18.2 기존 보고서 검증 시

```bash
oaispaper ref doc/d0910_보고서.md
```

---

## 19. 스크립트 참조

oaispaper 스킬 관련 스크립트와 역할을 정리한 섹션입니다.

### 19.1 스크립트 리스트

| 스크립트 | 명령어 | 설명 |
|----------|--------|------|
| `oaispaper_run.py` | `oaispaper run`<br>`oaispaper status`<br>`oaispaper fix`<br>`oaispaper clean-duplicates`<br>`oaispaper ref-update` | 통합 실행, 상태 확인, 무결성 체크, 중복 파일 정리, 참고문헌 업데이트 |
| `oaispaper_trans.py` | `oaispaper trans english`<br>`oaispaper trans korean` | PDF 텍스트 추출, 한글 번역 템플릿 생성 |
| `organize_01_down.py` | (직접 실행) | 01_down/ PDF → 02_paper/ 이동, download_list.md 처리 |
| `oaispaper_cite_verify.py` | (직접 실행) | 보고서 인용 검증 |
| `oaispaper_cite_normalize.py` | (직접 실행) | 인용 형식 정규화 |
| `oaispaper_cite_mapping.py` | (직접 실행) | 02_paper/ → 매핑 테이블 생성 |
| `oaispaper_cite_cleanup.py` | (직접 실행) | 인용 중복 제거 |
| `oaispaper_ref_update.py` | (직접 실행) | 참고문헌 단일 파일 업데이트 |
| `oaispaper_ref_update_batch.py` | (직접 실행) | 참고문헌 일괄 업데이트 |
| `oaispaper_ref_update_log.py` | (직접 실행) | 참고문헌 업데이트 로그 |

### 19.2 스크립트 상세 설명

#### oaispaper_run.py

**기능**: 논문 관리 통합 실행 스크립트

**주요 명령어**:
- `run`: 전체 자동 정리 (서머리/영문추출/한글번역)
- `status`: 통계 표시
- `fix`: 무결성 체크
- `clean-duplicates`: 중복 파일 검사 및 정리
- `ref-update`: 참고문헌 업데이트

**실행 예시**:
```bash
uv run python v/script/oaispaper_run.py status
uv run python v/script/oaispaper_run.py run --limit 10
uv run python v/script/oaispaper_run.py clean-duplicates --dry-run
```

#### oaispaper_trans.py

**기능**: PDF 텍스트 추출 및 번역 스크립트

**주요 명령어**:
- `english`: PDF → 03_전문(영어).md 추출
- `korean`: 03_전문(영어).md → 04_전문(한글).md 번역 템플릿 생성

**실행 예시**:
```bash
uv run python v/script/oaispaper_trans.py english
uv run python v/script/oaispaper_trans.py english --folder 260121-0001 --force
uv run python v/script/oaispaper_trans.py korean
```

#### organize_01_down.py

**기능**: 01_down/ 폴더 PDF 처리 스크립트

**처리 과정**:
1. PDF 파일 메타데이터 추출 (제목, arXiv ID 등)
2. 02_paper/에 표준 폴더 생성
3. PDF 이동 및 기본 파일 생성
4. download_list.md 처리

**실행 예시**:
```bash
uv run python v/script/organize_01_down.py
```

#### oaispaper_cite_*.py (인용 관리 스크립트)

| 스크립트 | 기능 | 실행 |
|----------|------|------|
| `oaispaper_cite_verify.py` | 보고서 인용 검증 (02_paper/ 기반) | `uv run python v/script/oaispaper_cite_verify.py doc/d0910_보고서.md` |
| `oaispaper_cite_normalize.py` | 인용 형식 정규화 | `uv run python v/script/oaispaper_cite_normalize.py doc/d0910_보고서.md` |
| `oaispaper_cite_mapping.py` | 02_paper/ → 매핑 테이블 생성 | `uv run python v/script/oaispaper_cite_mapping.py` |
| `oaispaper_cite_cleanup.py` | 인용 중복 제거 | `uv run python v/script/oaispaper_cite_cleanup.py doc/d0910_보고서.md` |
| `oaispaper_ref_update.py` | 참고문헌 단일 파일 업데이트 | `uv run python v/script/oaispaper_ref_update.py` |
| `oaispaper_ref_update_batch.py` | 참고문헌 일괄 업데이트 | `uv run python v/script/oaispaper_ref_update_batch.py` |
| `oaispaper_ref_update_log.py` | 참고문헌 업데이트 로그 | `uv run python v/script/oaispaper_ref_update_log.py` |

### 19.3 스크립트 실행 방법

#### 방법 1: oaispaper 명령어 (권장)

```bash
# 통합 실행
oaispaper run
oaispaper status

# 텍스트 추출/번역
oaispaper trans english
oaispaper trans korean
```

#### 방법 2: 직접 실행

```bash
# 스크립트 직접 실행
uv run python v/script/oaispaper_run.py status
uv run python v/script/oaispaper_trans.py english
uv run python v/script/organize_01_down.py
```

---

## 20. 품질 보증 체크리스트

### 20.1 보고서 작성 중

```markdown
- [ ] 인용 형식 준수 (Author (Year)[NUMBER])
- [ ] 순차적 번호 부여
- [ ] 논문 파일 존재 여부 확인
- [ ] 중복 표기 방지
```

### 20.2 완료 후 검증

```bash
oaispaper ref doc/d0910_보고서.md
```

자동 검증 항목:
- 모든 인용의 논문 파일 존재 확인
- 검증 불가 인용 제거
- 인용 번호 재부여
- 형식 정규화
- 최종 일관성 검증

---

*출처: d0105_보고서 및 논문에서 인용방법론_v01.md (2025-01-03)*
