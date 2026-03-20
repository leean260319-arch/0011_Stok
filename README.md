# OCR 모델 비교 테스트

4종 OCR 라이브러리의 성능을 비교하는 Streamlit 웹 애플리케이션

## 개요

본 프로젝트는 **PaddleOCR**, **EasyOCR**, **Tesseract OCR**, **DocTR** 4종의 OCR 라이브러리를 대상으로 이미지 조건별 인식 정확도 및 처리 속도를 비교 테스트하기 위한 것입니다.

## 주요 기능

- **단일 이미지 OCR 테스트**: 이미지를 업로드하여 4종 OCR 라이브러리 비교
- **배치 테스트**: 여러 이미지를 일괄 처리
- **결과 분석**: 인식 정확도, 처리 속도 비교 차트 및 데이터 내보내기

## 프로젝트 구조

```
a2z_ocr/
├── app.py                    # 메인 페이지
├── pages/
│   ├── 1_ocr_test.py        # OCR 테스트 페이지
│   ├── 2_batch_test.py       # 배치 테스트 페이지
│   └── 3_results.py         # 결과 분석 페이지
├── src/                      # OCR 모듈
│   ├── td3001_pdf_splitter.py
│   ├── td3002_image_augmentor.py
│   ├── td3003_preprocessor.py
│   ├── td3004_multi_ocr_runner.py
│   ├── td3005_input_validator.py
│   ├── td3006_accuracy_evaluator.py
│   ├── td3007_report_generator.py
│   ├── td3008_pipeline.py
│   ├── td3009_page_selector.py
│   └── td3010_page_classifier.py
├── doc/                      # 문서
│   ├── d0001_prd.md         # 제품 요구사항 정의서
│   ├── d0004_todo.md        # TODO 및 디버깅
│   └── d0010_history.md     # 변경 이력
├── tests/                    # 테스트 코드
└── v/                        # 스킬 문서
```

## 기술 스택

| 항목 | 기술 |
|------|------|
| 프레임워크 | Streamlit |
| 언어 | Python 3.13+ |
| 패키지 관리 | uv |
| OCR 라이브러리 | PaddleOCR, EasyOCR, Tesseract, DocTR |
| 이미지 처리 | OpenCV, Pillow, NumPy |

## 실행 방법

### 1. 의존성 설치

```bash
uv sync
```

### 2. Streamlit 서버 실행

```bash
# 기본 실행 (포트 8501)
uv run streamlit run app.py

# 또는 배치 파일 실행
run_ocr_app.bat
```

### 3. 브라우저에서 확인

- 로컬: http://localhost:8501
- 네트워크: http://192.168.1.254:8501

## 라이브러리 비교

| 라이브러리 | 개발사/团体 | 특징 | 한글 지원 |
|-----------|-----------|------|----------|
| PaddleOCR |百度 AI | 경량 모델, DB 텍스트 감지 | 지원 |
| EasyOCR | JaidedAI | CRAFT+CRNN, GPU 지원 | 지원 (kor) |
| Tesseract | Google | 전통적 OCR, LSTM 기반 | 지원 |
| DocTR | Mindee | TensorFlow/PyTorch 기반 | 제한적 |

## 이미지 조건

| 조건 | 설명 |
|------|------|
| Normal | 원본 PDF 페이지 이미지 |
| Noisy | 노이즈 추가 (Gaussian, Salt&Pepper) |
| Noisy+Distorted | 노이즈 + 기하학적 변형 (회전, 원근변환) |

## 평가 지표

- **CER** (Character Error Rate): 문자 단위 오류율
- **WER** (Word Error Rate): 단어 단위 오류율
- **처리 시간**: 페이지당 소요 시간
- **메모리 사용량**: 피크 메모리 사용량

## 문서

| 문서 | 설명 |
|------|------|
| doc/d0001_prd.md | 제품 요구사항 정의서 |
| doc/d0004_todo.md | TODO 및 디버깅 |
| doc/d0010_history.md | 변경 이력 |

---

Generated with Claude Code
