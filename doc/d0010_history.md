# d0010_history.md - Vibe 코딩 환경 변경 이력

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v11 | 2026-03-17 | StokAI 보안/안정성 코드 리뷰 16건 이슈 발견 및 전체 수정, PyInstaller hidden imports 40+ 모듈 추가, exe+인스톨러 재빌드 |
| v10 | 2026-03-03 | S10: 한국은행 PDF 2종 크롤링+OCR 파이프라인 스크립트 4종 작성 (download_bok_pdf, run_new_pdf_pipeline, run_ocr_new_pdfs, run_paddle_new_pdfs) |
| v09 | 2026-02-27 | td0100 완료: calc_cer 상한 제거, calc_cer_line_aligned/group_ocr_to_lines 추가, td3010 완료: PyMuPDF 차트/표 페이지 감지 구현 |
| v08 | 2026-02-25 | S09 완료: PaddleOCR Python 3.13 venv 실행(144 JSON), 4종 검증/리포트/차트 재생성 이력 기록 |
| v07 | 2026-02-24 | S08 완료: tax_policy_2025.pdf 전체 파이프라인(페이지선정+이미지세트+OCR 3종+검증), td4001 v03 PDF유형별비교 추가 이력 기록 |
| v06 | 2026-02-24 | S07 완료: Tesseract OCR 실행(72 JSON), 3종 검증/리포트/차트 재생성, td4001 최종 보고서 작성 이력 추가 |
| v05 | 2026-02-24 | S05+S06 완료: td3009 페이지선정, OCR 실행(easyocr+doctr), input_validation.json 생성 이력 추가 |
| v04 | 2026-02-23 | 초기 테스트 PDF 2종 수동 선정 및 다운로드 이력 추가 |
| v03 | 2026-01-28 | EasyOCR 프로젝트 초기 구축 이력 추가 |
| v02 | 2026-01-06 | oaisaddtodo → oaistodo 스킬명 변경 이력 추가 |
| v01 | 2026-01-06 | 초기 작성 |

---

## 개요

이 문서는 Vibe 코딩 환경 프로젝트의 주요 변경 사항을 기록합니다.

---

## 2026-03

### 2026-03-17

| 시간 | 변경 내용 | 관련 파일 |
|------|----------|----------|
| - | 코드 리뷰: 13개 핵심 파일 대상 보안/안정성 리뷰 (CRITICAL 5, HIGH 5, MEDIUM 4, LOW 2) | doc/d0011_code_review.md |
| - | [CRITICAL] AppState 스레드 안전성 - lock 보호 메서드 추가 (set_kill_switch, start_auto_trade 등) | src/web/app_state.py |
| - | [CRITICAL] API routes/WebSocket 직접 상태 변경을 스레드 안전 메서드로 교체 | src/web/api_routes.py, src/web/server.py |
| - | [CRITICAL] WebSocket 세션 매 메시지 재검증, 대시보드 인증 적용 | src/web/server.py |
| - | [CRITICAL] get_snapshot() copy.deepcopy 적용 | src/web/app_state.py |
| - | [HIGH] WebAuth threading.Lock 추가 (데드락 방지 내부/외부 메서드 분리) | src/web/auth.py |
| - | [HIGH] trade-logs limit 검증, 내부 상태 노출 제거, 명령 화이트리스트 | src/web/api_routes.py, src/web/server.py |
| - | [MEDIUM] MeanReversion 빈 데이터 매수 방지, 백테스트 OHLCV 전달 | src/engine/strategy_engine.py, src/engine/backtest_engine.py |
| - | [LOW] Strategy __init__ 속성 초기화, alert_view __import__ 해킹 제거 | src/engine/strategy_engine.py, src/ui/alert_view.py |
| - | PyInstaller hidden imports 40+ 모듈 추가 (전체 73개 src 모듈 + FastAPI 의존성) | build.py |
| - | exe 재빌드 (24.7MB) + Inno Setup 인스톨러 재빌드 (196.6MB) | dist/ |
| - | 테스트: 881 passed, 0 failed | tests/ |

---

### 2026-03-03

| 시간 | 변경 내용 | 관련 파일 |
|------|----------|----------|
| - | S10: 한국은행 PDF 2종 다운로드 (경제전망보고서 2025-02 4,897KB + 금융안정보고서 2024-12 6,687KB) | data/02_pdf_source/ |
| - | S10: 신규 PDF 2종 페이지 선정 (각 8페이지, n_text=6 + n_image=2) | data/output/selected_pages/ |
| - | S10: 이미지 세트 생성 (16페이지 × 11 = 176개) | data/04_normal/, data/05_noisy/, data/06_noisy_distorted/ |
| - | S10: OCR 3종 실행 (EasyOCR+DocTR+Tesseract, 신규 432 JSON) | data/output/ocr_results/{easy,doctr,tesseract}/ |
| - | S10: PaddleOCR 실행 (.venv_paddle, 신규 144 JSON) | data/output/ocr_results/paddle/ |
| - | S10: 4종 검증 리포트 재생성 (4 PDF 32페이지, 288파일 per lib, EasyOCR 0.7114 / Paddle 0.7191 / DocTR 0.8497 / Tesseract 0.8914) | data/output/reports/ |
| - | S10: td4002_bok_ocr_report.md 작성 (EasyOCR=PaddleOCR 동등 확인, p=0.3861) | doc/td4002_bok_ocr_report.md |

---

## 2026-02

### 2026-02-27

| 시간 | 변경 내용 | 관련 파일 |
|------|----------|----------|
| - | td0100: calc_cer() 상한(1.0) 제거, CER > 1.0 허용 | src/td3006_accuracy_evaluator.py |
| - | td0100: calc_cer_line_aligned() 추가 (줄 단위 Greedy 매칭 CER) | src/td3006_accuracy_evaluator.py |
| - | td0100-A: group_ocr_to_lines() 추가 (bbox 행 그루핑, y_gap_ratio=0.5) | src/td3006_accuracy_evaluator.py |
| - | TC-T100~T112 추가 (36개), 전체 100 PASS 3 SKIPPED | tests/test_accuracy_evaluator.py |
| - | td3006_accuracy_evaluator.md v03 업데이트 | doc/td3006_accuracy_evaluator.md |
| - | td3010_page_classifier.py 구현 (PyMuPDF thin_line 기반 차트/표 감지) | src/td3010_page_classifier.py |
| - | TC-P01~P07 7/7 PASS | tests/test_page_classifier.py |
| - | td3010_page_classifier.md 생성 | doc/td3010_page_classifier.md |

### 2026-02-25

| 시간 | 변경 내용 | 관련 파일 |
|------|----------|----------|
| - | PaddleOCR v3.4.0 Python 3.13 venv (.venv_paddle) 설치 및 AMD CPU 호환 패치 적용 | .venv_paddle/ |
| - | AMD CPU 호환 패치: static_infer.py optimization_level=0, memory_optim 비활성화 | .venv_paddle/...static_infer.py |
| - | PaddleOCR 실행: use_textline_orientation + enable_mkldnn=False + limit_side_len=960 | tmp/run_paddle_ocr.py |
| - | paddle OCR 결과 144 JSON 생성 (9버전 × 16이미지) | data/output/ocr_results/paddle/ |
| - | T26 완료: result_validation_paddle.json 생성 (avg_CER=0.7659) | data/output/reports/ |
| - | T30 갱신: comparative_validation.json 4종 라이브러리 포함 (6쌍 t-test) | data/output/reports/ |
| - | T32~T35 갱신: 비교 리포트/버전별CSV/차트 2종 4종 라이브러리로 재생성 | data/output/reports/ |
| - | d0002_plan.md v2.9, d0010_history.md v08 업데이트 | doc/d0002_plan.md |

### 2026-02-24

| 시간 | 변경 내용 | 관련 파일 |
|------|----------|----------|
| - | S05 완료: td3009_page_selector.py 구현 (population_2025_2045.pdf 8페이지 선정/추출) | src/td3009_page_selector.py |
| - | TC-T37 테스트 작성 및 PASS (10/10), 전체 87 PASS 3 SKIPPED | tests/test_td3009_page_selector.py |
| - | src/ 전체 td-넘버링 적용 (td3001~td3009) | src/*.py |
| - | doc/ td-넘버링 문서 9종 생성 (td3001~td3009.md) | doc/td3001~td3009_*.md |
| - | td1001_selected_pages.md, td2001_extraction_results.md 생성 | doc/td1001*.md, doc/td2001*.md |
| - | 8페이지 추출 완료 (data/output/selected_pages/ 16파일) | data/output/selected_pages/ |
| - | T23 완료: input_validation.json 생성 (8/8 valid) | data/output/reports/input_validation.json |
| - | easyocr, python-doctr 설치 완료 (Python 3.14) | .venv |
| - | OCR 실행: easyocr(844항목)+doctr(1441항목) 8페이지 결과 저장 | data/output/ocr_results/ |
| - | td2002_ocr_results.md 생성 (OCR 실행 결과 문서) | doc/td2002_ocr_results.md |
| - | d0002_plan.md v2.5, d0003_test.md v05 업데이트 | doc/d0002_plan.md, doc/d0003_test.md |
| - | 이미지 세트 생성 완료: 정상(8) + 노이즈(40) + 왜곡(40) = 88개 | data/04_normal/, data/05_noisy/, data/06_noisy_distorted/ |
| - | OCR v1/v2/v3 전체 실행: easy+doctr × 9버전 × 8페이지 = 144 JSON | data/output/ocr_results/{easy,doctr}/{subdir}/ |
| - | T26 완료: result_validation_{easy,doctr}.json 생성 | data/output/reports/ |
| - | T30 완료: comparative_validation.json (단조성 pass, p=0.054, d=0.82) | data/output/reports/comparative_validation.json |
| - | T32~T35 완료: 비교 리포트 CSV/JSON, 버전별 CSV, 차트 2종 생성 | data/output/reports/ |
| - | td2003_image_sets.md, td2004_validation_reports.md 생성 | doc/td2003*.md, doc/td2004*.md |
| - | d0002_plan.md v2.6 업데이트 | doc/d0002_plan.md |
| - | Tesseract v5.4 설치 (winget) + kor.traineddata 다운로드 | C:\Program Files\Tesseract-OCR\ |
| - | Tesseract OCR 실행: kor+eng × 9버전 × 8페이지 = 72 JSON | data/output/ocr_results/tesseract/ |
| - | T26 완료: result_validation_tesseract.json 생성 (avg_CER=0.9359) | data/output/reports/ |
| - | T30 갱신: comparative_validation.json 3종 라이브러리 포함 (3쌍 t-test) | data/output/reports/comparative_validation.json |
| - | T32~T35 갱신: comparison_report/버전별CSV/차트 2종 3종 라이브러리로 재생성 | data/output/reports/ |
| - | td4001_ocr_performance_report.md 생성 (3종 최종 비교 보고서) | doc/td4001_ocr_performance_report.md |
| - | d0002_plan.md v2.7 업데이트 (T19~T21/T23/T26/T30/T36 완료 반영) | doc/d0002_plan.md |
| - | tax_policy_2025.pdf 8페이지 선정/추출 (td3009_page_selector) | data/output/selected_pages/ |
| - | tax 이미지 세트 생성: normal(8)+noisy(40)+distorted(40) = 88개 | data/04_normal~06_noisy_distorted/ |
| - | tax OCR 3종 실행: easy+doctr+tesseract × 9버전 × 8페이지 = 216 JSON | data/output/ocr_results/ |
| - | 2 PDF 합산 검증 재실행: result_validation 144개, comparative_validation 갱신 | data/output/reports/ |
| - | td4001 v03 업데이트: 5.4 PDF유형별비교 신설 (차트혼합 vs 텍스트위주) | doc/td4001_ocr_performance_report.md |
| - | d0002_plan.md v2.8, d0010_history.md v07 업데이트 | doc/d0002_plan.md |

### 2026-02-23

| 시간 | 변경 내용 | 관련 파일 |
|------|----------|----------|
| - | PRD v1.8 업데이트 (8.2.4 초기 테스트 PDF 선정 결과 추가) | doc/d0001_prd.md |
| - | Plan v2.2 업데이트 (F01-00 추가, T00a/T00b 완료 반영, S00 스프린트 추가) | doc/d0002_plan.md |
| - | 초기 테스트 PDF-A 다운로드 완료 (tax_policy_2025.pdf, 10.4MB, NABO 조세정책 보고서) | data/02_pdf_source/tax_policy_2025.pdf |
| - | 초기 테스트 PDF-B 다운로드 완료 (population_2025_2045.pdf, 9.2MB, NABO 인구전망 보고서) | data/02_pdf_source/population_2025_2045.pdf |

---

## 2026-01

### 2026-01-28

| 시간 | 변경 내용 | 관련 파일 |
|------|----------|----------|
| - | EasyOCR 제품 라벨 인식 PRD 작성 (v1.1) | doc/d0001_prd.md |
| - | 구현 계획 작성 | doc/d0002_plan.md |
| - | OCR 테스트 코드 개발 | src/test_ocr.py |
| - | 샘플 라벨 이미지 10장 생성 | data/01_sample/*.png |
| - | OCR 실행 및 결과 저장 (10건) | data/output/*.json |
| - | 가상환경 복구, easyocr/opencv 설치 | pyproject.toml, .venv |

### 2026-01-06

| 시간 | 변경 내용 | 관련 파일 |
|------|----------|----------|
| 18:30 | oaisaddtodo → oaistodo 스킬명 변경 | v/oaistodo.md, v/script/oaistodo_run.py |
| 18:20 | 핵심 문서 생성 (d0001, d0004, d0010) | doc/*.md |
| 18:15 | oaiscommand 스킬 문서 생성 | v/oaiscommand.md |
| 18:10 | 명령어 표기법 통일 (스킬명 접두사) | v/script/oaiscommand_run.py |
| 17:50 | oaissync view 서브명령어 추가 | v/oaissync.md, v/script/oaissync_run.py |
| 17:30 | oaissync 스킬 생성 | v/oaissync.md, v/script/oaissync_run.py |
| 17:00 | 0002_paper 프로젝트에 vibe 환경 동기화 | - |

---

## 아카이브된 이슈

> d0004_todo.md에서 해결 후 이동된 이슈

| 원본 ID | 분류 | 내용 | 해결일 | 해결방법 |
|---------|------|------|--------|---------|
| - | - | (아카이브된 이슈 없음) | - | - |

---

## 참고 문서

- PRD: `doc/d0001_prd.md`
- 할일/디버깅: `doc/d0004_todo.md`
- 명령어 목록: `doc/d0007_command.md`
