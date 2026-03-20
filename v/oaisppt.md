# oaisppt - PPT 생성 스킬

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v3.3 | 2026-01-17 | 출력 위치 규칙 추가 (입력 파일과 동일 경로) |
| v3.2 | 2026-01-03 | 문서 이력 관리 섹션 추가 |

---

> 공통 규칙: `v/guide/common_guide.md` 참조

## 1. 서브명령어

| 명령어 | 설명 |
|--------|------|
| `oaisppt status` | 서브명령어 리스트, 상태 요약 |
| `oaisppt version` | 스킬 버전 정보 (v3.3) |
| `oaisppt run [경로]` | PPTX 생성 |
| `oaisppt preview` | 미리보기 |

## 2. 워크플로우

```
Explore(수집) → oaisppt-agent(스크립트) → task-executor(생성) → task-checker(검증)
```

**병렬처리**: 슬라이드 10+개 시 `run_in_background=true`로 병렬 생성

**환각 방지**: 소스 내용만 사용, 원문 유지, 출처 표기

## 3. 설치

```bash
pip install python-pptx Pillow
```

## 4. 스타일

| 항목 | 값 |
|------|-----|
| 다크/라이트 배경 | `#0F0F0F` / `#F5F5F0` |
| 카드 배경 | `#1A1A1A` |
| 텍스트 | `#FFFFFF`, `#1A1A1A`, `#888888` |
| 폰트 | Pretendard (대체: 맑은 고딕) |
| 크기 | 16:9, 여백 0.67인치 |

## 5. 슬라이드 API

| 메서드 | 용도 | 배경 |
|--------|------|------|
| `add_cover_slide(title, subtitle, description, badge_text, footer_items)` | 표지 | 다크 |
| `add_about_slide(icon, name, subtitle, headline, description, stats[3])` | 소개 | 라이트 |
| `add_grid_slide(badge_text, subtitle, cards[4])` | 그리드 | 다크 |
| `add_features_slide(badge_text, subtitle, features[4], quote)` | 특징 | 라이트 |
| `add_tips_slide(badge_text, subtitle, tips[3])` | 팁 | 다크 |
| `add_closing_slide(title, subtitle, badge_text, footer_items)` | 마무리 | 다크 |

**파라미터 형식**:
- `cards`: `[{icon, title, desc, label}]`
- `features`: `[{title, desc}]`
- `tips`: `[{icon, title, desc}]`
- `footer_items/stats`: `[{label, value}]`

## 6. 소스 매핑

| 소스 | 처리 | 권장 슬라이드 |
|------|------|--------------|
| `.md` 제목 | 구조 파싱 | cover |
| `.md` 개요 | 계층 추출 | about |
| `.txt` 단락 | 문단 분리 | features |
| `.json` 데이터 | 구조화 | grid |
| 목록 3-4개 | 항목 추출 | grid/tips |
| 결론 | 마무리 | closing |

## 7. 파일 구조

```
v/script/oaisppt_pptx.py   # 생성 라이브러리
v/script/oaisppt_pack.py   # XML → PPTX
v/script/oaisppt_unpack.py # PPTX → XML
```

**유틸리티**:
```bash
python v/script/oaisppt_unpack.py input.pptx output_dir
python v/script/oaisppt_pack.py input_dir output.pptx
```

## 8. 출력 규칙

| 항목 | 규칙 |
|------|------|
| **출력 위치 (입력 파일 있음)** | 입력 파일과 동일한 디렉토리 |
| **출력 위치 (입력 파일 없음)** | `doc/` 폴더 |
| **파일명** | `{주제}_프레젠테이션.pptx` |

**예시**:
- 입력: `doc/d0001_prd.md` → 출력: `doc/d0001_prd_프레젠테이션.pptx`
- 입력: `data/report.txt` → 출력: `data/report_프레젠테이션.pptx`
- 입력 없음 (대화 기반) → 출력: `doc/{주제}_프레젠테이션.pptx`
