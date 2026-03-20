# streamlit_guide - Streamlit 개발 가이드

> 공통 가이드라인: `v/guide/common_guide.md` 참조

## 1. 개요

Streamlit 프로젝트 개발 시 참조하는 프레임워크 가이드.
oaisdev 실행 시 Streamlit 프로젝트로 감지되면 자동 참조.

---

## 2. 레이아웃 패턴

### 2.1 CRUD 페이지

```
┌─────────────┬──────────────────────────────┐
│  사이드바    │         메인 영역             │
│  - 검색      │  [추가] [수정] [삭제]         │
│  - 필터      │  ┌─────────────────────────┐ │
│  - 기간선택  │  │ 데이터 테이블           │ │
│             │  └─────────────────────────┘ │
│             │  [상세 정보 / 수정 폼]        │
└─────────────┴──────────────────────────────┘
```

### 2.2 대시보드

```
┌─────────────┬──────────────────────────────┐
│  사이드바    │  [KPI 1] [KPI 2] [KPI 3]     │
│  - 기간선택  │  ┌───────────┬─────────────┐ │
│  - 필터      │  │ 차트 1    │ 차트 2      │ │
│             │  └───────────┴─────────────┘ │
│             │  ┌─────────────────────────┐ │
│             │  │ 상세 테이블             │ │
│             │  └─────────────────────────┘ │
└─────────────┴──────────────────────────────┘
```

---

## 3. 컴포넌트 매핑

| 기능 | 컴포넌트 | 비고 |
|------|---------|------|
| 텍스트 검색 | `st.text_input()` | placeholder 활용 |
| 상태 필터 | `st.selectbox()` | "전체" 옵션 포함 |
| 다중 선택 | `st.multiselect()` | 기본값 설정 |
| 날짜 범위 | `st.date_input()` | 튜플 반환 |
| 데이터 표시 | `st.dataframe()` | 읽기 전용 |
| 데이터 편집 | `st.data_editor()` | 수정 가능 |
| 상세 정보 | `st.expander()` | 접기/펼치기 |
| 탭 분리 | `st.tabs()` | 컨텍스트 분리 |
| 폼 입력 | `st.form()` | 일괄 제출 |
| 컬럼 레이아웃 | `st.columns()` | 가로 배치 |

---

## 4. 페이지 기본 구조

```python
import streamlit as st
from oais import ui, db

# 1. 페이지 설정
ui.setup_page_config(page_title="페이지명")
ui.show_page_header("제목", "설명")

# 2. 세션 상태 초기화
if "selected_item" not in st.session_state:
    st.session_state.selected_item = None

# 3. 사이드바
with st.sidebar:
    search_term = st.text_input("검색")
    filter_value = st.selectbox("상태", ["전체", "활성", "비활성"])

# 4. 메인 영역
data = db.get_data(search_term, filter_value)
st.dataframe(data)
```

---

## 5. 페이지 명명 규칙

### 5.1 파일명 체계

```
{대분류}_{페이지번호}_{페이지명}.py
```

| 구성요소 | 설명 | 예시 |
|---------|------|------|
| 대분류 | 서비스 그룹 번호 (0~9) | 0=홈, 1=정보, 9=관리 |
| 페이지번호 | 그룹 내 순번 (00~99) | 00=그룹헤더, 01~=하위페이지 |
| 페이지명 | 기능 설명 | 시니어넷, 게시판 |

### 5.2 대분류 코드

| 코드 | 대분류 | 설명 |
|------|--------|------|
| 0 | 홈 | 메인, 게시판, 사용자관리 |
| 1 | 정보 | 뉴스, 정책, 일자리 |
| 2 | 동영상 | 동영상 콘텐츠 |
| 3 | 의료 | 의료정보, 건강 |
| 4 | 복지 | 복지서비스, 지원 |
| 5 | 커머스 | 쇼핑, 상품 |
| 6 | 자산 | 자산운용, 펀드 |
| 7 | 앱프로토타입 | 모바일 앱 프로토타입 |
| 8 | 개발 | 개발도구 (Dev 전용) |
| 9 | 관리 | 관리자 (Admin 전용) |

### 5.3 특수 표기

| 표기 | 의미 | 예시 |
|------|------|------|
| `===` | 서비스 그룹 헤더 | `1_10_시니어뉴스_서비스===.py` |

### 5.4 PRD 문서 연동

> **상세 페이지 목록**: `doc/d20001_prd.md` 섹션 5 참조

| PRD 섹션 | 내용 |
|----------|------|
| 5.1 페이지 리스트 | 전체 페이지 목록 (ID, 대분류, 메뉴명, 권한) |
| 5.2 페이지 상세 | 페이지별 상세 기획 (주요기능, UI구성, 데이터소스) |

---

## 6. oais 모듈 활용

| 모듈 | 함수 | 용도 |
|------|------|------|
| oais.ui | setup_page_config | 페이지 설정 (title, icon) |
| oais.ui | show_page_header | 페이지 헤더 (제목, 설명) |
| oais.ui | display_user_info_header | 사용자 정보 표시 |
| oais.db | get_connection | DB 연결 |
| oais.db | execute_query | 쿼리 실행 |
| oais.date_utils | format_date | 날짜 포맷 |
| oais.validation | validate_input | 입력 검증 |

---

## 7. 세션 상태 패턴

### 7.1 기본 초기화

```python
# 단일 값
if "key" not in st.session_state:
    st.session_state.key = default_value

# 다중 값 (dict 활용)
defaults = {"page": 1, "filter": "전체", "selected": None}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v
```

### 7.2 콜백 패턴

```python
def on_select(item_id):
    st.session_state.selected = item_id

st.button("선택", on_click=on_select, args=(item_id,))
```

---

## 8. 캐싱 패턴

```python
@st.cache_data(ttl=300)  # 5분 캐시
def get_data(query_params):
    return db.execute_query(...)

@st.cache_resource  # 리소스 캐시 (DB 연결 등)
def get_db_connection():
    return db.get_connection()
```

---

## 9. DB 설계 표준용어

표준용어집: `v/template/db_standard_word.md`

| 패턴 | 용도 | 예시 |
|------|------|------|
| `*_id` | 식별자 | user_id, order_id |
| `*_cd` | 코드 | status_cd, type_cd |
| `*_nm` | 명칭 | user_nm, product_nm |
| `*_dt` | 날짜 | created_dt, updated_dt |
| `*_yn` | 여부 | use_yn, del_yn |
| `*_cnt` | 건수 | view_cnt, order_cnt |
| `*_amt` | 금액 | total_amt, tax_amt |

---

## 10. 체크리스트

### 10.1 구현 전

- [ ] PRD 분석 완료
- [ ] 필요 oais 모듈 확인
- [ ] DB 스키마 확인

### 10.2 구현 중

- [ ] 페이지 기본 구조 적용
- [ ] 세션 상태 초기화
- [ ] 사이드바/메인 영역 분리
- [ ] oais 모듈 활용

### 10.3 구현 후

- [ ] 코드 리뷰 (python-code-reviewer)
- [ ] 품질 분석 (oaisqa)
- [ ] 에러 체크 (code-error-checker)
- [ ] E2E 테스트 (필요 시)

---

## 11. 관련 문서

| 문서 | 용도 |
|------|------|
| v/guide/common_guide.md | 공통 가이드라인 |
| doc/d0005_lib.md | oais 모듈 문서 |
| doc/d0006_db.md | DB 구조 문서 |
| v/template/streamlit-page.md | 개발 템플릿 |
