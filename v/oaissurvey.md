# oaissurvey - 논문 서베이 및 분석

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v06 | 2026-01-13 | list 명령어 paper_list.md 참조 기능 추가 |
| v05 | 2026-01-13 | OAIS_PAPER_DIR 환경변수 지원 (.env), 기본 폴더 외부 경로 지원 |
| v04 | 2026-01-06 | 스킬명 변경: oaispaper → oaissurvey, 서베이 → survey |
| v03 | 2026-01-06 | 출력 파일 d0011→d0100_survey.md 변경 (연구/논문 문서 번호 체계 적용) |
| v02 | 2026-01-06 | 범용화: PRD 연동, 비교 분석, 인용 생성, d0004 연동 추가 |
| v01 | 2026-01-06 | 최초 생성 |

---

> 공통: `v/guide/common_guide.md` | 컨텍스트: `v/oaiscontext.md`

## 1. 개요

논문 폴더를 분석하여 연구 주제 관련 서베이 문서를 생성/관리합니다.

- **입력**: 논문 폴더 내 논문 (PDF, 서머리, 전문)
- **출력**: `doc/d0100_survey.md` 서베이 문서
- **연동**: d0001_prd.md (연구 주제), d0004_todo.md (이슈)
- **컨텍스트**: `--sp N` 또는 `oaiscontext N`

### 1.0 논문 폴더 설정

**.env 파일에서 설정** (권장):

```bash
# .env
OAIS_PAPER_DIR=../0002_paper/02_paper   # 상대경로
# 또는
OAIS_PAPER_DIR=C:/Users/.../paper       # 절대경로
```

**기본값**: `paper/` (프로젝트 내)

**우선순위**:
1. `--paper-dir` 옵션
2. `.env`의 `OAIS_PAPER_DIR`
3. 기본값 `paper/`

### 1.1 연구 주제 자동 감지

PRD(`doc/d0001_prd.md`)에서 연구 주제 및 키워드를 자동 추출합니다.

```
# PRD에서 추출하는 정보
- 연구 주제 (제목/목표)
- 관련 키워드 (기술 스택, 방법론)
- 도메인 (컴퓨터 비전, NLP, 등)
```

### 1.2 수동 설정

PRD 없거나 오버라이드 시 `--topic`, `--keywords` 옵션 사용:

```bash
oaissurvey run --topic "크랙 세그멘테이션" --keywords "U-Net,Transformer,attention"
```

---

## 2. 서브명령어

| 명령어 | 설명 |
|--------|------|
| `oaissurvey status` | paper 폴더 현황, d0100 상태, 미분석 논문 |
| `oaissurvey version` | 스킬 버전 정보 (v06) |
| `oaissurvey list` | 논문 목록 (paper_list.md 참조, 없으면 폴더 스캔) |
| `oaissurvey run` | 서머리 기반 분석 → d0100_survey.md 생성 |
| `oaissurvey deeprun` | PDF 포함 정밀 분석 → d0100_survey.md 생성 |
| `oaissurvey compare` | 논문 간 비교 분석 (모델, 성능, 방법론) |
| `oaissurvey cite` | 인용 형식 생성 (APA, IEEE, BibTeX) |
| `oaissurvey add [폴더]` | 새 논문 추가 분석 → 기존 d0100에 병합 |

### 2.1 공통 옵션

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--paper-dir` | 논문 폴더 경로 오버라이드 | `--paper-dir ../0002_paper/02_paper` |
| `--topic` | 연구 주제 오버라이드 | `--topic "객체 탐지"` |
| `--keywords` | 키워드 오버라이드 (콤마 구분) | `--keywords "YOLO,ResNet"` |
| `--threshold` | 관련성 임계값 (기본 2) | `--threshold 3` |
| `--dry-run` | 실행 없이 계획만 출력 | |
| `--verbose` | 상세 로그 출력 | |

### 2.2 list 명령어

`oaissurvey list`는 논문 폴더 내 `paper_list.md` 파일을 우선 참조합니다.

**참조 우선순위**:
1. `{OAIS_PAPER_DIR}/paper_list.md` (존재 시)
2. 폴더 직접 스캔 (paper_list.md 없을 경우)

**paper_list.md 형식**:

```markdown
| No. | 폴더ID | 논문 제목 | 저자 | 연도 | 출처 | 등록일 | 완료 | 비고 |
|:---:|--------|----------|------|:----:|------|--------|:----:|------|
| 1 | 230312-1648 | Holistically_Nested_Edge | - | - | - | 2023-03-12 | O | - |
```

**list 출력 옵션**:

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--all` | 전체 목록 | `oaissurvey list --all` |
| `--pending` | 미완료만 | `oaissurvey list --pending` |
| `--recent N` | 최근 N개 | `oaissurvey list --recent 10` |
| `--search 키워드` | 제목 검색 | `oaissurvey list --search crack` |

---

## 3. paper 폴더 구조

> **참고**: 논문 폴더 경로는 `.env`의 `OAIS_PAPER_DIR`로 설정 (섹션 1.0 참조)

### 3.1 지원 구조

**구조 A: 날짜-시간 코드 (권장)**
```
paper/
├── {YYMMDD}-{HHMM}/           # 논문별 폴더
│   ├── {코드}_00_*_서머리.md   # 서머리 (최우선)
│   ├── {코드}_04_전문(한글).md  # 한글 전문
│   ├── {코드}_03_전문(영어).md  # 영문 전문
│   └── *.pdf                  # 원본 PDF
```

**구조 B: 논문명 기반**
```
paper/
├── {논문제목}/
│   ├── summary.md
│   ├── full_text.md
│   └── paper.pdf
```

**구조 C: 단순 PDF**
```
paper/
├── paper1.pdf
├── paper2.pdf
└── ...
```

### 3.2 파일 우선순위

| 순서 | 패턴 | 분석 대상 |
|------|------|:--------:|
| 1 | `*서머리*.md`, `summary*.md` | run, deeprun |
| 2 | `*전문(한글)*.md`, `*korean*.md` | run, deeprun |
| 3 | `*전문(영어)*.md`, `*english*.md` | deeprun |
| 4 | `*.pdf` | deeprun |

---

## 4. run 워크플로우

### 4.1 실행 흐름

```
1. PRD에서 연구 주제/키워드 추출 (또는 옵션 사용)
2. paper/ 폴더 스캔 → 논문 목록 생성
3. 각 논문 서머리 읽기 → 관련성 점수 계산
4. 임계값 이상 → 상세 분석 (한글 전문 포함)
5. d0100_survey.md 생성/업데이트
6. 분석 불가 논문 → d0004에 이슈 등록
```

### 4.2 관련성 판단

키워드 매칭 기반 점수 계산:

| 카테고리 | 예시 키워드 | 가중치 |
|----------|------------|:------:|
| 핵심 기술 | PRD에서 추출한 키워드 | 2.0 |
| 모델/아키텍처 | U-Net, ResNet, Transformer, YOLO | 1.5 |
| 방법론 | segmentation, detection, attention | 1.0 |
| 도메인 | image, vision, NLP, audio | 0.5 |

**기본 임계값**: 2.0 (2개 이상 매칭)

### 4.3 출력 형식

```markdown
# d0100_survey.md - 논문 서베이

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | YYYY-MM-DD | 초기 서베이 (N편 분석) |

---

## 1. 개요

- **연구 주제**: {PRD에서 추출}
- **분석 논문**: N편
- **분석 일시**: YYYY-MM-DD HH:MM
- **관련 키워드**: {키워드 목록}

---

## 2. 서베이

### 2.1 {논문 제목}

- **출처**: {폴더코드}
- **핵심 내용**: {1-2문장 요약}
- **관련 기술**: {키워드}
- **관련도**: {높음/중간/낮음} ({점수})
- **적용 가능성**: {본 연구와의 연관성}

---

## 3. 분석 요약

### 3.1 기술별 분류

| 기술 | 논문 수 | 대표 논문 |
|------|---------|----------|
| {기술1} | N | {논문명} |

### 3.2 핵심 인사이트

1. {인사이트}
2. {인사이트}

### 3.3 본 연구 적용점

| 논문 | 적용 가능 기술 | 구현 우선순위 |
|------|--------------|:------------:|
| {논문} | {기술} | P1/P2/P3 |

---

## 4. 참고 논문 목록

| # | 폴더코드 | 제목 | 관련도 | 분석 상태 |
|---|----------|------|:------:|:--------:|
| 1 | 251201-0036 | ... | 높음 | 완료 |
```

---

## 5. deeprun 워크플로우

### 5.1 추가 분석 항목

| 항목 | 설명 |
|------|------|
| 모델 아키텍처 | 상세 구조, 레이어, 파라미터 수 |
| 실험 설정 | 데이터셋, 하이퍼파라미터, 학습 전략 |
| 성능 수치 | 정량적 메트릭 (IoU, F1, mAP 등) |
| 핵심 수식 | Loss function, 핵심 알고리즘 |
| Figure/Table | 주요 시각자료 분석 |
| 한계점 | 논문에서 언급한 한계 |

### 5.2 deeprun 출력 추가 섹션

```markdown
### 2.N {논문 제목}

- **출처**: {폴더코드}
- **핵심 내용**: {상세 요약}
- **모델 아키텍처**:
  - Encoder: {설명}
  - Decoder: {설명}
  - 파라미터: {M}
- **실험 결과**:
  - Dataset: {데이터셋}
  - Metrics: IoU {값}, F1 {값}, mAP {값}
  - 비교 모델 대비: {+/-}%
- **핵심 기여**: {주요 기여점}
- **한계점**: {한계}
- **본 연구 적용**:
  - 적용 가능 기술: {기술}
  - 구현 난이도: {상/중/하}
  - 예상 효과: {설명}
```

---

## 6. compare 워크플로우

논문 간 비교 분석:

```bash
# 특정 논문들 비교
oaissurvey compare 251201-0036 251130-2321 251108-1402

# 전체 관련 논문 비교
oaissurvey compare --all

# 특정 측면으로 비교
oaissurvey compare --focus performance
oaissurvey compare --focus architecture
```

### 6.1 비교 출력

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

### 추천

- **성능 우선**: {논문}
- **경량화 우선**: {논문}
- **균형**: {논문}
```

---

## 7. cite 워크플로우

인용 형식 생성:

```bash
# 단일 논문
oaissurvey cite 251201-0036 --format bibtex

# 전체 분석된 논문
oaissurvey cite --all --format apa

# 형식: apa, ieee, bibtex, mla
```

### 7.1 출력 예시

```bibtex
@article{chen2024unet,
  title={Deep Learning for Crack Detection},
  author={Chen, Wei and Zhang, Li},
  journal={Pattern Recognition},
  year={2024},
  volume={89},
  pages={1-15}
}
```

---

## 8. d0004 연동

### 8.1 이슈 유형

| 유형 | 분류 | 설명 |
|------|------|------|
| 서머리 누락 | DOCS | 논문에 서머리 파일 없음 |
| PDF 분석 실패 | BUGFIX | PDF 읽기/파싱 오류 |
| 관련성 미판단 | MISC | 키워드 매칭 불가 |

### 8.2 이슈 등록 형식

| ID | 발생일 | 분류 | 내용 | 우선순위 | 상태 |
|----|--------|------|------|---------|------|
| P001 | 2026-01-06 | DOCS | paper/251201-0323 - 서머리 누락 | 낮음 | 대기 |

### 8.3 ID 규칙

- Prefix: `P` (Paper)
- 예: P001, P002...

---

## 9. 병렬 처리

### 9.1 아키텍처

```
메인 에이전트 (조율)
    ├── Agent 1: 서머리 분석 (run)
    ├── Agent 2: 전문 분석 (deeprun)
    ├── Agent 3: PDF 분석 (deeprun)
    └── Agent 4: 비교/인용 생성
```

### 9.2 서브에이전트 매핑

| 작업 | 에이전트 | 병렬 |
|------|---------|:----:|
| 서머리 분석 | Explore | O |
| 전문 분석 | academic-researcher | O |
| PDF 분석 | data-analyst | O |
| 문서 생성 | task-executor | - |

---

## 10. 완료 조건

| 조건 | 검증 방법 |
|------|----------|
| d0100 생성/업데이트 | 파일 존재 및 버전 증가 |
| 관련 논문 전체 분석 | 참고 목록에 누락 없음 |
| d0004 이슈 등록 | 분석 불가 논문 기록 |
| PRD 연동 확인 | 연구 주제 일치 |

---

## 11. 관련 문서

| 문서 | 용도 |
|------|------|
| doc/d0001_prd.md | 연구 주제 참조 |
| doc/d0100_survey.md | 생성 문서 |
| doc/d0004_todo.md | 이슈 등록 |
| v/guide/common_guide.md | 공통 가이드 |

---

## 12. 사용 예시

```bash
# 현황 확인
oaissurvey status

# 논문 목록
oaissurvey list

# 서베이 생성 (PRD 기반)
oaissurvey run

# 커스텀 주제로 서베이
oaissurvey run --topic "객체 탐지" --keywords "YOLO,SSD,RetinaNet"

# 정밀 분석
oaissurvey deeprun

# 새 논문 추가
oaissurvey add paper/251206-1234

# 논문 비교
oaissurvey compare --all --focus performance

# 인용 생성
oaissurvey cite --all --format bibtex > references.bib
```
