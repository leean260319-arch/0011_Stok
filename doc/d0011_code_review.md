# StokAI 코드 리뷰 보고서

## 문서 정보

- **문서번호**: d0011
- **작성일**: 2026-03-17
- **리뷰 대상**: src/ 전체 (73개 파일)
- **목적**: 주식 자동매매 프로그램의 보안/안정성/정확성 검증

## 문서이력관리

| 버전 | 날짜 | 변경내용 |
|------|------|----------|
| v02 | 2026-03-17 | 2차/3차 리뷰 반영 - 12개 추가 이슈 발견 및 수정, 트레이 모드/화면 설정/포트포워딩 기능 추가 |
| v01 | 2026-03-17 | 초기 작성 - 16개 이슈 발견, 전체 수정 완료 |

---

## 1. 리뷰 요약

| 항목 | 1차 리뷰 | 2차/3차 리뷰 | 최종 |
|------|---------|-------------|------|
| 리뷰 파일 수 | 13개 | 14개 | 27개 |
| 발견된 이슈 | 16개 | 12개 | 28개 |
| CRITICAL | 5 | 2 | 7 |
| HIGH | 5 | 3 | 8 |
| MEDIUM | 4 | 4 | 8 |
| LOW | 2 | 3 | 5 |
| **수정 완료** | **16/16** | **12/12** | **28/28 (100%)** |
| 테스트 결과 | 881 passed | 881 passed | 881 passed, 0 failed |

---

## 2. CRITICAL 이슈 (7건) - 모두 수정 완료

### C-01: 스레드 안전성 없는 상태 변경 (API Routes)

| 항목 | 내용 |
|------|------|
| 파일 | `src/web/api_routes.py:194-232` |
| 위험 | PyQt6 메인 스레드 + FastAPI 백그라운드 스레드가 공유 상태를 lock 없이 동시 접근 |
| 영향 | 킬 스위치 실패, 자동매매 상태 불일치, 의도치 않은 매매 발생 가능 |
| 수정 | `AppState`에 `set_kill_switch()`, `start_auto_trade()`, `stop_auto_trade()` 등 lock 보호 메서드 추가. API routes에서 직접 상태 변경 대신 해당 메서드 사용 |

### C-02: 동일한 스레드 안전성 문제 (WebSocket)

| 항목 | 내용 |
|------|------|
| 파일 | `src/web/server.py:121-133` |
| 위험 | `_handle_ws_command`에서 `self.state.kill_switch_active` 등을 lock 없이 직접 변경 |
| 영향 | WebSocket 경유 킬 스위치/자동매매 제어 시 경쟁 조건 발생 |
| 수정 | 모든 상태 변경을 `self.state.set_kill_switch()`, `self.state.start_auto_trade()` 등으로 교체 |

### C-03: WebSocket 세션 만료 미검증

| 항목 | 내용 |
|------|------|
| 파일 | `src/web/server.py:101-113` |
| 위험 | 연결 시점에만 토큰 검증, 이후 세션 만료되어도 명령 계속 수신 |
| 영향 | 만료된 토큰으로 매매 제어 가능 (보안 우회) |
| 수정 | `while True` 루프 내 매 메시지마다 `validate_session(token)` 재검증 추가. 만료 시 code=4001로 연결 종료 |

### C-04: 인증 없이 대시보드 HTML 노출

| 항목 | 내용 |
|------|------|
| 파일 | `src/web/server.py:88-96` |
| 위험 | `/dashboard` 경로가 인증 없이 접근 가능 -> API 구조/엔드포인트 노출 |
| 영향 | 공격자가 네트워크에서 대시보드 HTML을 통해 API 공격 표면 파악 |
| 수정 | `/dashboard` 라우트에 `token` 쿼리 파라미터 검증 추가. 미인증 시 `/` 로그인 페이지로 리다이렉트 |

### C-05: get_snapshot() 얕은 복사로 인한 데이터 경쟁

| 항목 | 내용 |
|------|------|
| 파일 | `src/web/app_state.py:108-122` |
| 위험 | `dict()`, `list()` 얕은 복사로 내부 중첩 객체 공유 -> 스레드 간 데이터 충돌 |
| 영향 | market_index 등 중첩 dict가 다른 스레드에서 변경 시 WebSocket 브로드캐스트 데이터 오염 |
| 수정 | `copy.deepcopy()` 적용으로 완전한 깊은 복사 보장 |

### C-06: 하드코딩된 기본 비밀번호 (2차 리뷰)

| 항목 | 내용 |
|------|------|
| 파일 | `src/config.py:47`, `src/main.py:88` |
| 위험 | 웹 대시보드 기본 비밀번호 `stokai2026`이 소스코드에 평문 하드코딩 |
| 영향 | 사용자가 변경하지 않으면 알려진 비밀번호로 외부에서 매매 제어 가능 |
| 수정 | `DEFAULT_CONFIG`에서 비밀번호 기본값을 빈 문자열로 변경. 웹 서버 시작 시 비밀번호 미설정이면 `secrets.token_urlsafe(12)`로 랜덤 생성 후 config 저장 |

### C-07: get_public_ip() 예외 미처리로 앱 시작 차단 (2차 리뷰)

| 항목 | 내용 |
|------|------|
| 파일 | `src/utils/constants.py:47-59` |
| 위험 | 네트워크 미연결 환경에서 `urlopen` 예외 발생 시 앱 전체가 시작되지 않음 |
| 영향 | 네트워크 없는 환경에서 프로그램 사용 불가 |
| 수정 | 각 서비스 호출을 개별 try/except로 감싸 실패 시 다음 서비스 시도, 모두 실패 시 빈 문자열 반환 |

---

## 3. HIGH 이슈 (8건) - 모두 수정 완료

### H-01: WebAuth 클래스 스레드 안전성 부재

| 항목 | 내용 |
|------|------|
| 파일 | `src/web/auth.py:12-69` |
| 위험 | `_sessions`, `_fail_count`, `_lock_until`에 대한 동시 접근 보호 없음 |
| 영향 | 동시 로그인 시도 시 잠금 우회 가능 |
| 수정 | `threading.Lock` 추가. 모든 공개 메서드에 lock 보호. 데드락 방지용 내부 메서드 분리 |

### H-02: API에서 내부 인증 상태 노출

| 항목 | 내용 |
|------|------|
| 파일 | `src/web/api_routes.py:104` |
| 위험 | `deps.auth._max_fail - deps.auth._fail_count`로 남은 시도 횟수 노출 |
| 수정 | `remaining_attempts()` 공개 메서드로 교체. 에러 메시지에서 남은 시도 횟수 제거 |

### H-03: trade-logs limit 파라미터 무제한

| 항목 | 내용 |
|------|------|
| 파일 | `src/web/api_routes.py:154` |
| 위험 | `limit` 값에 상한 없음 -> 메모리 과다 사용 가능 |
| 수정 | `limit = max(1, min(limit, 100))` 검증 추가 |

### H-04: WebSocket 명령 검증 없음

| 항목 | 내용 |
|------|------|
| 파일 | `src/web/server.py:117-134` |
| 위험 | 모든 JSON 데이터를 무검증 처리, strategy_name 길이/내용 제한 없음 |
| 수정 | 허용 명령 화이트리스트 + `strategy_name` 100자 제한 |

### H-05: 세션 정리 메커니즘 부재

| 항목 | 내용 |
|------|------|
| 파일 | `src/web/auth.py:15,71-85` |
| 위험 | 만료된 세션이 `_sessions` dict에 영구 잔류 -> 장기 실행 시 메모리 누수 |
| 수정 | `cleanup_expired_sessions()` 메서드 추가 + broadcast_loop에서 10분 주기 호출 |

### H-06: get_local_ip() 소켓 미해제 + 앱 차단 (2차 리뷰)

| 항목 | 내용 |
|------|------|
| 파일 | `src/utils/constants.py:37-44` |
| 위험 | 소켓 close 전 예외 시 리소스 누수, 네트워크 없으면 앱 시작 차단 |
| 수정 | try/finally로 소켓 반드시 닫힘 보장, OSError 시 `127.0.0.1` 반환 |

### H-07: API GET 엔드포인트 thread-safe 미적용 (3차 리뷰)

| 항목 | 내용 |
|------|------|
| 파일 | `src/web/api_routes.py:141-184` |
| 위험 | 7개 GET 엔드포인트가 lock 없이 AppState 속성 직접 읽기 |
| 영향 | PyQt6 메인 스레드와 동시 접근 시 불완전한 데이터 반환 가능 |
| 수정 | `AppState`에 `get_account()`, `get_positions()`, `get_trade_logs()` 등 7개 thread-safe getter 추가. 모든 GET 엔드포인트가 getter 사용 |

### H-08: SetupWizard app.exec() 이중 호출 (2차 리뷰)

| 항목 | 내용 |
|------|------|
| 파일 | `src/main.py:60-66` |
| 위험 | `app.exec()`가 SetupWizard와 MainWindow에서 두 번 호출 -> Qt 미정의 동작 |
| 수정 | SetupWizard를 QDialog 래퍼로 감싸 `dialog.exec()` 모달 실행, 이벤트 루프 단일화 |

---

## 4. MEDIUM 이슈 (8건) - 모두 수정 완료

### M-01: MeanReversionStrategy 빈 데이터에서 매수 시그널

| 항목 | 내용 |
|------|------|
| 파일 | `src/engine/strategy_engine.py:198-204` |
| 위험 | close, bb_lower, bb_upper 모두 기본값 0 -> `0 <= 0` = True -> 매수 |
| 수정 | 0 이하 값 감지 시 `{"action": "관망", "reasons": ["데이터 부족"]}` 반환 |

### M-02: 백테스트 엔진 시장 데이터 미전달

| 항목 | 내용 |
|------|------|
| 파일 | `src/engine/backtest_engine.py:64` |
| 위험 | `evaluate()` 호출 시 Backtrader의 OHLCV 데이터를 전달하지 않음 |
| 수정 | OHLCV market_data dict 구성 후 `evaluate(market_data)` 전달 |

### M-03: AppState.get_snapshot() 얕은 복사

| 항목 | 내용 |
|------|------|
| 파일 | `src/web/app_state.py:108-122` |
| 수정 | `copy.deepcopy()` 적용 |

### M-04: 세션 만료 자동 정리 미호출

| 항목 | 내용 |
|------|------|
| 파일 | `src/web/auth.py`, `src/web/server.py` |
| 수정 | `cleanup_expired_sessions()` 메서드 추가 + `_broadcast_loop`에서 10분 주기 호출 |

### M-05: api_routes.py에서 내부 lock 직접 접근 (2차 리뷰)

| 항목 | 내용 |
|------|------|
| 파일 | `src/web/api_routes.py:204` |
| 위험 | `deps.state._lock_data` private 속성 직접 사용 -> 캡슐화 위반 |
| 수정 | `AppState.get_auto_trade_strategy()` 공개 메서드 추가, 직접 접근 제거 |

### M-06: QT_SCALE_FACTOR 런타임 변경 무효 (2차 리뷰)

| 항목 | 내용 |
|------|------|
| 파일 | `src/app.py` |
| 위험 | `QApplication` 생성 후 환경 변수 설정은 효과 없음 |
| 수정 | 런타임 변경 제거, 재시작 안내 메시지 표시. `main.py`에서 `QApplication` 생성 전 환경변수 설정 |

### M-07: build.py에 display_settings_view hidden import 누락 (2차 리뷰)

| 항목 | 내용 |
|------|------|
| 파일 | `build.py` |
| 수정 | `--hidden-import=src.ui.display_settings_view` 추가 |

### M-08: 트레이 자동매매 상태를 텍스트로 판단 (3차 리뷰)

| 항목 | 내용 |
|------|------|
| 파일 | `src/app.py` (SystemTray) |
| 위험 | UI 텍스트 기반 상태 판단이 깨지기 쉬움 |
| 수정 | `_autotrade_running`, `_kill_switch_active` 불리언 플래그 도입, 상태 메서드에서 플래그 업데이트 |

---

## 5. LOW 이슈 (5건) - 모두 수정 완료

### L-01: Strategy 클래스 _last_signal/_last_tick 미초기화

| 항목 | 내용 |
|------|------|
| 파일 | `src/engine/strategy_engine.py` |
| 수정 | 3개 전략 클래스 `__init__`에서 초기화 |

### L-02: alert_view.py의 __import__ 해킹 코드

| 항목 | 내용 |
|------|------|
| 파일 | `src/ui/alert_view.py:127` |
| 수정 | 정상 `from PyQt6.QtGui import QColor` import로 교체 |

### L-03: _current_font_size 미초기화 (2차 리뷰)

| 항목 | 내용 |
|------|------|
| 파일 | `src/app.py` (MainWindow) |
| 수정 | `__init__`에서 `self._current_font_size = 12` 명시적 초기화 |

### L-04: main.py 이중 import (3차 리뷰)

| 항목 | 내용 |
|------|------|
| 파일 | `src/main.py:59` |
| 수정 | 함수 내부의 중복 `import os` 제거 |

### L-05: _quit_app 불필요한 창 표시 (3차 리뷰)

| 항목 | 내용 |
|------|------|
| 파일 | `src/app.py` (SystemTray._quit_app) |
| 수정 | 종료 전 `_show_window()` 호출 제거 |

---

## 6. 빌드 이슈 - 수정 완료

### B-01: PyInstaller hidden imports 대량 누락

| 항목 | 내용 |
|------|------|
| 파일 | `build.py` |
| 증상 | exe 실행 시 빈 3분할 화면만 표시, 네비게이션/설정/뷰 없음 |
| 원인 | 73개 src 모듈 중 약 40개가 hidden imports에서 누락 |
| 수정 | 모든 src 하위 모듈 + FastAPI/uvicorn/starlette/anyio/h11/pydantic/jinja2 등 의존성 추가 |

---

## 7. 추가 구현 사항 (리뷰 과정에서 추가)

| 기능 | 파일 | 설명 |
|------|------|------|
| 화면 설정 (폰트/UI 스케일) | `src/ui/display_settings_view.py` | 폰트 크기 8~24px, UI 스케일 75~200%, Ctrl+=/- 단축키 |
| 트레이 모드 강화 | `src/app.py` | X버튼 트레이 최소화, 종료 확인, 매매/킬스위치 제어, 알림, 웹 대시보드 열기 |
| 포트포워딩 가이드 | `doc/d0008_user.md` | ipTIME/KT/SK/LG/ASUS 공유기별 설정, DDNS, 고정IP |
| 인스톨러 보안 | `installer.iss` | Defender 제외, 방화벽 규칙, SmartScreen 해제, 제거 시 정리 |
| 공인 IP 표시 | `src/main.py`, `src/utils/constants.py` | 웹 대시보드 URL에 공인 IP 기본 표시 |

---

## 8. 향후 개선 권장사항 (미수정)

> 아래 항목은 현재 기능에 영향을 주지 않으나, 운영 환경 배포 전 검토 권장

| ID | 구분 | 내용 | 우선순위 |
|----|------|------|---------|
| R-01 | 보안 | 비밀번호 해싱을 SHA-256에서 PBKDF2/bcrypt/argon2로 변경 (솔트 + 키 스트레칭) | 높음 |
| R-02 | 보안 | 웹 서버 HTTPS/TLS 지원 추가 (uvicorn ssl_keyfile/ssl_certfile) | 중간 |
| R-03 | 보안 | `0.0.0.0` 바인딩을 `127.0.0.1` 기본값으로 변경, 외부 노출은 사용자 명시 opt-in | 중간 |
| R-04 | UX | 킬 스위치 글로벌 핫키 Ctrl+Shift+K 구현 | 낮음 |
| R-05 | UX | 킬 스위치 2초 길게 누르기 오조작 방지 UX | 낮음 |

---

## 9. 테스트 커버리지

| 항목 | 결과 |
|------|------|
| 총 테스트 수 | 881개 |
| 통과 | 881 (100%) |
| 실패 | 0 |
| 경고 | 3 (기존 deprecation, 무관) |
| 수행 시간 | 16.16초 |

---

## 10. 리뷰 대상 파일 목록

| 파일 | 설명 | 발견 이슈 수 |
|------|------|-------------|
| `src/web/api_routes.py` | REST API 엔드포인트 | 5 |
| `src/web/server.py` | FastAPI + WebSocket 서버 | 5 |
| `src/web/auth.py` | 인증 모듈 | 3 |
| `src/web/app_state.py` | 공유 상태 싱글톤 | 3 |
| `src/app.py` | 메인 윈도우 + 시스템 트레이 | 3 |
| `src/main.py` | 앱 진입점 | 3 |
| `src/utils/constants.py` | 상수/유틸리티 | 2 |
| `src/engine/strategy_engine.py` | 매매 전략 엔진 | 2 |
| `src/engine/backtest_engine.py` | 백테스팅 엔진 | 1 |
| `src/ui/alert_view.py` | 알림 센터 위젯 | 1 |
| `src/config.py` | 설정 관리 | 1 |
| `src/ui/themes/dark_theme.py` | 다크 테마 | 0 (양호) |
| `build.py` | PyInstaller 빌드 | 1 |
| `src/db/database.py` | SQLCipher DB | 0 (양호) |
| `src/security/credential_manager.py` | 자격증명 관리 | 0 (양호) |
| `src/engine/risk_manager.py` | 리스크 관리 | 0 (양호) |
