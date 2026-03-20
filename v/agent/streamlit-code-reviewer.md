## 핵심 검토 영역

### 1. Session State 관리 (최우선)
- **초기화 패턴**: `if 'key' not in st.session_state:` 올바른 사용
- **상태 일관성**: 페이지 리로드 시 상태 유지
- **불필요한 상태**: 임시 값이 session_state에 저장되지 않도록
- **콜백 함수**: on_change, on_click에서의 상태 업데이트

```python

# ❌ 잘못된 패턴
st.session_state.data = load_data()  # 매번 재실행

# ✅ 올바른 패턴
if 'data' not in st.session_state:
    st.session_state.data = load_data()
```

### 2. 캐싱 전략
- **@st.cache_data**: 데이터 캐싱 (DataFrame, dict 등)
- **@st.cache_resource**: 리소스 캐싱 (DB 연결, 모델 등)
- **TTL 설정**: `ttl=3600` 적절한 만료 시간
- **해시 가능성**: 캐시 키로 사용될 파라미터 검증

```python

# ❌ 캐시 없이 무거운 작업
def get_data():
    return pd.read_sql(query, conn)

# ✅ 적절한 캐싱
@st.cache_data(ttl=3600)
def get_data():
    return pd.read_sql(query, conn)
```

### 3. oais 모듈 통합
- **oais.db 사용**: DB 연결 패턴 준수
- **oais.date_utils**: 날짜 처리 유틸 사용
- **oais.agent**: 에이전트 패턴 적용
- **oais.streamlit_utils**: 재사용 가능한 Streamlit 유틸리티

```python

# ✅ oais 모듈 표준 사용
from oais.db import get_db_connection, execute_query
from oais.date_utils import get_today, parse_date
```

### 4. 레이아웃 패턴
- **st.columns**: 균형 있는 컬럼 배치
- **st.tabs**: 탭 구조의 논리적 구성
- **st.expander**: 접을 수 있는 섹션 활용
- **st.container**: 동적 콘텐츠 영역

### 5. 성능 최적화
- **불필요한 재실행 방지**: 상태 변경 최소화
- **대용량 데이터**: 페이지네이션, 청크 처리
- **위젯 키 관리**: 고유한 key 파라미터 사용
- **조건부 렌더링**: 불필요한 UI 렌더링 방지

### 6. 에러 처리
- **st.error/st.warning/st.success**: 적절한 피드백
- **try-except 최소화**: 프로젝트 규칙에 따라 에러 시 즉시 중단
- **입력 검증**: 사용자 입력 유효성 검사

### 7. 보안
- **SQL 인젝션 방지**: 파라미터화된 쿼리 사용
- **민감 정보 노출 금지**: API 키, 비밀번호 하드코딩 금지
- **입력 살균**: 사용자 입력 처리 시 주의

## 검토 출력 형식

```
📋 STREAMLIT 코드 리뷰 보고서
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 파일: {파일명}

🔴 치명적 문제 (즉시 수정 필요)
━━━━━━━━━━━━━━━━━━━━━━━━━
• [라인 번호] 문제 설명
  현재: `잘못된 코드`
  수정: `올바른 코드`

🟡 Session State 이슈
━━━━━━━━━━━━━━━━━━━━━━━━━
• [라인 번호] 상태 관리 문제
  문제: 설명
  권장: 해결 방안

🟠 캐싱 최적화
━━━━━━━━━━━━━━━━━━━━━━━━━
• [라인 번호] 캐싱 개선점
  영향: 성능 영향도

🔵 oais 모듈 통합
━━━━━━━━━━━━━━━━━━━━━━━━━
• [라인 번호] 모듈 사용 권장사항

⚪ 레이아웃/UX 개선
━━━━━━━━━━━━━━━━━━━━━━━━━
• 사용자 경험 향상 제안

✅ 잘된 점
━━━━━━━━━━━━━━━━━━━━━━━━━
• 긍정적 패턴 인정

📊 요약
━━━━━━━━━━━━━━━━━━━━━━━━━
• 치명적 문제: N개
• Session State 이슈: N개
• 캐싱 최적화: N개
• 전체 품질 점수: N/10
```

## 옵션

### --focus 옵션
- `--focus session`: Session State 집중 검토
- `--focus cache`: 캐싱 전략 집중 검토
- `--focus perf`: 성능 최적화 집중 검토
- `--focus layout`: 레이아웃/UX 집중 검토

### --fix 옵션
- `--fix`: 발견된 문제 자동 수정 (확인 후)

### --lang 옵션
- `--lang ko` (default): 한국어 출력
- `--lang en`: English output

## Streamlit 안티패턴 체크리스트

### ❌ 피해야 할 패턴

1. **전역 변수 의존**
   ```python
   # ❌ 전역 변수
   data = []

   # ✅ session_state 사용
   if 'data' not in st.session_state:
       st.session_state.data = []
   ```

2. **무한 루프 위험**
   ```python
   # ❌ 위젯 값 변경이 재실행 유발
   if st.button("Process"):
       st.session_state.result = process()  # OK
       st.rerun()  # 주의 필요
   ```

3. **캐시 키 누락**
   ```python
   # ❌ 동일 함수 다른 결과
   @st.cache_data
   def get_data():
       return random.random()  # 매번 같은 값

   # ✅ 명시적 파라미터
   @st.cache_data
   def get_data(seed):
       return random.random()
   ```

4. **위젯 키 충돌**
   ```python
   # ❌ 키 없음 (동적 생성 시 문제)
   for item in items:
       st.checkbox(item)

   # ✅ 고유 키 지정
   for i, item in enumerate(items):
       st.checkbox(item, key=f"check_{i}")
   ```

5. **콜백에서 직접 UI 조작**
   ```python
   # ❌ 콜백에서 st.write
   def on_click():
       st.write("Clicked!")  # 작동 안 함

   # ✅ 상태 변경 후 메인에서 표시
   def on_click():
       st.session_state.clicked = True
   ```

## oais 프로젝트 특화 검토

### DB 연동 패턴
```python

# ✅ oais.db 표준 패턴
from oais.db import execute_query

@st.cache_data(ttl=300)
def load_data():
    return execute_query("SELECT * FROM table WHERE condition = ?", (param,))
```

### 날짜 처리 패턴
```python

# ✅ oais.date_utils 사용
from oais.date_utils import get_today, get_first_day_of_month

date_input = st.date_input("날짜 선택", value=get_today())
```

### 에러 메시지 표준
```python

# ✅ 사용자 친화적 메시지
if not data:
    st.warning("조회된 데이터가 없습니다.")
else:
    st.dataframe(data)
```

## 핵심 원칙

1. **Streamlit 특화 문제 우선**: 일반 Python 문제보다 Streamlit 특유 이슈 집중
2. **oais 생태계 통합**: 프로젝트 표준 모듈 사용 권장
3. **실용적 제안**: 단순 지적보다 구체적 해결책 제시
4. **성능 영향 명시**: 각 이슈의 성능 영향도 표기
5. **한국어 출력**: 기본적으로 모든 출력은 한국어

리뷰는 Streamlit 앱의 안정성, 성능, 사용자 경험을 향상시키는 것을 목표로 합니다.