# {{DOC_ID}}_{{SCRIPT_NAME}}.md - {{SCRIPT_TITLE}} 문서

## 문서이력관리

| 버전 | 날짜 | 작성자 | 변경내용 |
|------|------|--------|----------|
| v01 | {{DATE}} | {{AUTHOR}} | 초기 작성 - {{SCRIPT_FILE}} 코드 분석 |

---

## 1. 개요

### 1.1 목적
{{PURPOSE_DESCRIPTION}}

### 1.2 주요 특징
- **{{FEATURE_1_NAME}}**: {{FEATURE_1_DESC}}
- **{{FEATURE_2_NAME}}**: {{FEATURE_2_DESC}}
- **{{FEATURE_3_NAME}}**: {{FEATURE_3_DESC}}

### 1.3 처리 단계
| 단계 | 내용 | 비고 |
|------|------|------|
| 1단계 | {{STEP_1}} | {{STEP_1_NOTE}} |
| 2단계 | {{STEP_2}} | {{STEP_2_NOTE}} |
| 3단계 | {{STEP_3}} | {{STEP_3_NOTE}} |

---

## 2. 실행 방법

### 2.1 기본 실행
```bash
uv run {{SCRIPT_PATH}}
```

### 2.2 명령행 옵션
| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `{{OPTION_1}}` | {{OPTION_1_DESC}} | {{OPTION_1_DEFAULT}} |
| `{{OPTION_2}}` | {{OPTION_2_DESC}} | {{OPTION_2_DEFAULT}} |

### 2.3 실행 예시
```bash
# 예시 1: {{EXAMPLE_1_DESC}}
uv run {{SCRIPT_PATH}} {{EXAMPLE_1_ARGS}}

# 예시 2: {{EXAMPLE_2_DESC}}
uv run {{SCRIPT_PATH}} {{EXAMPLE_2_ARGS}}
```

---

## 3. 설정 (CONFIG)

### 3.1 입출력 설정
```python
"io": {
    "input_dir": "{{INPUT_DIR}}",  # 입력 디렉토리
    {{IO_CONFIG_ITEMS}}
}
```

### 3.2 처리 설정
```python
"processing": {
    {{PROCESSING_CONFIG_ITEMS}}
}
```

### 3.3 출력 설정
```python
"output": {
    {{OUTPUT_CONFIG_ITEMS}}
}
```

---

## 4. 기능/메트릭 상세

### 4.1 {{CATEGORY_1_NAME}}

| 항목 | 설명 | 값 범위 | 의미 |
|------|------|---------|------|
| {{ITEM_1}} | {{ITEM_1_DESC}} | {{ITEM_1_RANGE}} | {{ITEM_1_MEANING}} |
| {{ITEM_2}} | {{ITEM_2_DESC}} | {{ITEM_2_RANGE}} | {{ITEM_2_MEANING}} |

### 4.2 {{CATEGORY_2_NAME}}

| 항목 | 설명 | 값 범위 | 의미 |
|------|------|---------|------|
| {{ITEM_3}} | {{ITEM_3_DESC}} | {{ITEM_3_RANGE}} | {{ITEM_3_MEANING}} |

---

## 5. 출력 파일

### 5.1 출력 디렉토리
```
{{OUTPUT_DIR}}
```

### 5.2 출력 파일 목록

| 파일명 | 내용 |
|--------|------|
| {{OUTPUT_FILE_1}} | {{OUTPUT_FILE_1_DESC}} |
| {{OUTPUT_FILE_2}} | {{OUTPUT_FILE_2_DESC}} |

### 5.3 출력 구조
{{OUTPUT_STRUCTURE_DESC}}

---

## 6. 코드 구조

### 6.1 핵심 함수 (oais 모듈)

| 함수 | 모듈 | 설명 |
|------|------|------|
| `{{CORE_FUNC_1}}` | {{CORE_FUNC_1_MODULE}} | {{CORE_FUNC_1_DESC}} |
| `{{CORE_FUNC_2}}` | {{CORE_FUNC_2_MODULE}} | {{CORE_FUNC_2_DESC}} |

### 6.2 로컬 함수

| 함수 | 설명 |
|------|------|
| `{{LOCAL_FUNC_1}}` | {{LOCAL_FUNC_1_DESC}} |
| `main()` | 메인 실행 함수 |

### 6.3 의존성 모듈

```python
{{IMPORT_STATEMENTS}}
```

### 6.4 처리 흐름

```
{{FLOW_DIAGRAM}}
```

### 6.5 핵심 함수 시그니처

```python
{{MAIN_FUNCTION_SIGNATURE}}
```

**파라미터:**
| 파라미터 | 타입 | 설명 |
|----------|------|------|
| `{{PARAM_1}}` | {{PARAM_1_TYPE}} | {{PARAM_1_DESC}} |
| `{{PARAM_2}}` | {{PARAM_2_TYPE}} | {{PARAM_2_DESC}} |

### 6.6 다른 코드에서 사용 예시

```python
{{USAGE_EXAMPLE}}
```

---

## 7. 결과 해석 가이드

### 7.1 {{INTERPRETATION_CATEGORY_1}}
- {{INTERPRETATION_1}}
- {{INTERPRETATION_2}}

### 7.2 {{INTERPRETATION_CATEGORY_2}}
- {{INTERPRETATION_3}}
- {{INTERPRETATION_4}}

---

## 8. 참고사항

### 8.1 {{NOTE_CATEGORY_1}}
- {{NOTE_1}}
- {{NOTE_2}}

### 8.2 {{NOTE_CATEGORY_2}}
- {{NOTE_3}}

### 8.3 지원 확장자/형식
```
{{SUPPORTED_FORMATS}}
```

---

## 9. 라이브러리 및 함수 정보

### 9.1 주요 라이브러리

| 라이브러리 | 버전 요구사항 | 용도 |
|------------|---------------|------|
| {{LIB_1}} | {{LIB_1_VER}} | {{LIB_1_PURPOSE}} |
| {{LIB_2}} | {{LIB_2_VER}} | {{LIB_2_PURPOSE}} |

### 9.2 주요 함수 참조

| 함수 | 용도 | 사용 위치 |
|------|------|-----------|
| {{FUNC_REF_1}} | {{FUNC_REF_1_PURPOSE}} | {{FUNC_REF_1_LOCATION}} |
| {{FUNC_REF_2}} | {{FUNC_REF_2_PURPOSE}} | {{FUNC_REF_2_LOCATION}} |

---

## 템플릿 사용 가이드

### 필수 치환 항목
- `{{DOC_ID}}`: 문서 번호 (예: d6310, d6211)
- `{{SCRIPT_NAME}}`: 스크립트 명 (예: nr_iqas, cee_filter)
- `{{SCRIPT_TITLE}}`: 스크립트 제목 (예: NR-IQA 통합 분석)
- `{{SCRIPT_FILE}}`: 스크립트 파일명 (예: ps6310_nr_iqas.py)
- `{{SCRIPT_PATH}}`: 스크립트 경로 (예: src/ps63_img_iqa/ps6310_nr_iqas.py)
- `{{DATE}}`: 작성 날짜 (예: 2026.01.17)
- `{{AUTHOR}}`: 작성자

### 선택 섹션
- **섹션 4**: 메트릭/기능이 많은 경우 사용 (없으면 생략)
- **섹션 7**: 결과 해석이 필요한 경우 사용 (없으면 생략)
- **섹션 9**: 라이브러리 정보가 중요한 경우 사용 (없으면 생략)

### 문서 번호 체계
- d6xxx: 이미지 처리/IQA 관련
- d5xxx: 머신러닝/딥러닝 관련
- d4xxx: 데이터 분석 관련
