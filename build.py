"""StokAI PyInstaller 빌드 + Inno Setup 인스톨러 스크립트

버전: v1.0
설명: uv run python build.py 로 실행
옵션:
  --exe-only    PyInstaller 빌드만 실행
  --installer   Inno Setup 인스톨러만 생성 (dist/StokAI 필요)
  (기본)        빌드 + 인스톨러 순차 실행
"""

import os
import subprocess
import sys

import PyInstaller.__main__

APP_NAME = "StokAI"
APP_VERSION = "0.1.0"
DIST_DIR = "dist"
WORK_DIR = "tmp/build"
INNO_COMPILER = (
    r"C:\Users\USER\AppData\Local\Programs\Inno Setup 6\ISCC.exe"
)
ISS_FILE = "installer.iss"


def build_exe() -> None:
    """PyInstaller로 exe 빌드를 실행한다."""
    print(f"[1/2] PyInstaller 빌드 시작: {APP_NAME}")

    # sqlcipher3 네이티브 DLL 수집
    import importlib
    sqlcipher_binaries = []
    spec = importlib.util.find_spec("sqlcipher3")
    if spec and spec.origin:
        pkg_dir = os.path.dirname(spec.origin)
        for f in os.listdir(pkg_dir):
            if f.endswith((".dll", ".pyd", ".so")):
                sqlcipher_binaries.append(f"--add-binary={os.path.join(pkg_dir, f)};sqlcipher3")

    opts = [
        "src/main.py",
        f"--name={APP_NAME}",
        "--onedir",
        "--windowed",
        "--noconfirm",
        "--clean",
        # --- PyQt6 ---
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=PyQt6.QtWebEngineWidgets",
        "--hidden-import=PyQt6.QtWebEngineCore",
        "--hidden-import=PyQt6.QtWebChannel",
        # --- DB/보안 ---
        "--hidden-import=sqlcipher3",
        "--hidden-import=sqlcipher3.dbapi2",
        "--hidden-import=keyring",
        "--hidden-import=keyring.backends",
        "--hidden-import=keyring.backends.Windows",
        "--hidden-import=cryptography",
        # --- 데이터/분석 ---
        "--hidden-import=pandas",
        "--hidden-import=pandas_ta",
        "--hidden-import=numpy",
        "--hidden-import=openai",
        "--hidden-import=requests",
        "--hidden-import=bs4",
        "--hidden-import=feedparser",
        "--hidden-import=backtrader",
        "--hidden-import=grpcio",
        "--hidden-import=google.protobuf",
        "--hidden-import=matplotlib",
        "--hidden-import=lightweight_charts",
        # --- FastAPI/uvicorn 전체 의존성 ---
        "--hidden-import=fastapi",
        "--hidden-import=fastapi.staticfiles",
        "--hidden-import=fastapi.templating",
        "--hidden-import=fastapi.responses",
        "--hidden-import=fastapi.requests",
        "--hidden-import=uvicorn",
        "--hidden-import=uvicorn.config",
        "--hidden-import=uvicorn.main",
        "--hidden-import=uvicorn.logging",
        "--hidden-import=uvicorn.loops",
        "--hidden-import=uvicorn.loops.auto",
        "--hidden-import=uvicorn.loops.asyncio",
        "--hidden-import=uvicorn.protocols",
        "--hidden-import=uvicorn.protocols.http",
        "--hidden-import=uvicorn.protocols.http.auto",
        "--hidden-import=uvicorn.protocols.http.h11_impl",
        "--hidden-import=uvicorn.protocols.websockets",
        "--hidden-import=uvicorn.protocols.websockets.auto",
        "--hidden-import=uvicorn.protocols.websockets.wsproto_impl",
        "--hidden-import=uvicorn.lifespan",
        "--hidden-import=uvicorn.lifespan.on",
        "--hidden-import=uvicorn.lifespan.off",
        "--hidden-import=starlette",
        "--hidden-import=starlette.routing",
        "--hidden-import=starlette.responses",
        "--hidden-import=starlette.middleware",
        "--hidden-import=starlette.staticfiles",
        "--hidden-import=starlette.templating",
        "--hidden-import=anyio",
        "--hidden-import=anyio._backends",
        "--hidden-import=anyio._backends._asyncio",
        "--hidden-import=h11",
        "--hidden-import=httptools",
        "--hidden-import=pydantic",
        "--hidden-import=jinja2",
        "--hidden-import=multipart",
        "--hidden-import=python_multipart",
        # --- 최적화 ---
        "--hidden-import=optuna",
        # --- src 최상위 ---
        "--hidden-import=src",
        "--hidden-import=src.app",
        "--hidden-import=src.config",
        "--hidden-import=src.main",
        "--hidden-import=src.service_container",
        # --- src.ai ---
        "--hidden-import=src.ai",
        "--hidden-import=src.ai.news_analyzer",
        "--hidden-import=src.ai.sentiment_scorer",
        "--hidden-import=src.ai.llm_service",
        "--hidden-import=src.ai.rag_engine",
        # --- src.bridge ---
        "--hidden-import=src.bridge",
        "--hidden-import=src.bridge.kiwoom_bridge",
        "--hidden-import=src.bridge.kiwoom_wrapper",
        "--hidden-import=src.bridge.kiwoom_server",
        "--hidden-import=src.bridge.kiwoom_pb2",
        "--hidden-import=src.bridge.kiwoom_pb2_grpc",
        # --- src.crawler ---
        "--hidden-import=src.crawler",
        "--hidden-import=src.crawler.naver_crawler",
        "--hidden-import=src.crawler.rss_crawler",
        "--hidden-import=src.crawler.news_manager",
        "--hidden-import=src.crawler.news_scheduler",
        # --- src.db ---
        "--hidden-import=src.db",
        "--hidden-import=src.db.database",
        "--hidden-import=src.db.models",
        "--hidden-import=src.db.migrations",
        # --- src.engine ---
        "--hidden-import=src.engine",
        "--hidden-import=src.engine.event_queue",
        "--hidden-import=src.engine.chart_analyzer",
        "--hidden-import=src.engine.signal_generator",
        "--hidden-import=src.engine.ai_scorer",
        "--hidden-import=src.engine.strategy_engine",
        "--hidden-import=src.engine.risk_manager",
        "--hidden-import=src.engine.backtest_engine",
        "--hidden-import=src.engine.orchestrator",
        "--hidden-import=src.engine.market_classifier",
        "--hidden-import=src.engine.optimizer",
        "--hidden-import=src.engine.trade_logger",
        "--hidden-import=src.engine.report_generator",
        # --- src.security ---
        "--hidden-import=src.security",
        "--hidden-import=src.security.credential_manager",
        "--hidden-import=src.security.encryption",
        "--hidden-import=src.security.app_lock",
        # --- src.utils ---
        "--hidden-import=src.utils",
        "--hidden-import=src.utils.constants",
        "--hidden-import=src.utils.logger",
        "--hidden-import=src.utils.exporter",
        "--hidden-import=src.utils.session_manager",
        "--hidden-import=src.utils.build_helper",
        "--hidden-import=src.utils.updater",
        # --- src.web ---
        "--hidden-import=src.web",
        "--hidden-import=src.web.server",
        "--hidden-import=src.web.auth",
        "--hidden-import=src.web.api_routes",
        "--hidden-import=src.web.ws_manager",
        "--hidden-import=src.web.app_state",
        # --- src.ui (뷰) ---
        "--hidden-import=src.ui",
        "--hidden-import=src.ui.dashboard",
        "--hidden-import=src.ui.chart_view",
        "--hidden-import=src.ui.news_view",
        "--hidden-import=src.ui.trade_view",
        "--hidden-import=src.ui.portfolio_view",
        "--hidden-import=src.ui.watchlist_view",
        "--hidden-import=src.ui.backtest_view",
        "--hidden-import=src.ui.alert_view",
        "--hidden-import=src.ui.settings_view",
        "--hidden-import=src.ui.ai_settings_view",
        "--hidden-import=src.ui.trade_settings_view",
        "--hidden-import=src.ui.web_settings_view",
        "--hidden-import=src.ui.setup_wizard",
        "--hidden-import=src.ui.display_settings_view",
        "--hidden-import=src.ui.alert_manager",
        # --- src.ui.panels ---
        "--hidden-import=src.ui.panels",
        "--hidden-import=src.ui.panels.left_panel",
        "--hidden-import=src.ui.panels.right_panel",
        # --- src.ui.widgets ---
        "--hidden-import=src.ui.widgets",
        "--hidden-import=src.ui.widgets.toggle_switch",
        "--hidden-import=src.ui.widgets.glass_card",
        "--hidden-import=src.ui.widgets.ai_signal_card",
        "--hidden-import=src.ui.widgets.ai_status_indicator",
        "--hidden-import=src.ui.widgets.kill_switch",
        "--hidden-import=src.ui.widgets.toast_notification",
        # --- src.ui.themes ---
        "--hidden-import=src.ui.themes",
        "--hidden-import=src.ui.themes.dark_theme",
        # --- 데이터 파일 ---
        "--add-data=src/db;src/db",
        "--add-data=src/web/templates;src/web/templates",
        "--add-data=src/web/static;src/web/static",
        "--add-data=assets;assets",
        # UAC 관리자 권한 요청
        "--uac-admin",
        # 출력 디렉토리
        f"--distpath={DIST_DIR}",
        f"--workpath={WORK_DIR}",
        "--specpath=.",
    ]

    # sqlcipher3 바이너리 추가
    opts.extend(sqlcipher_binaries)

    # 아이콘 파일이 있으면 추가
    if os.path.exists("assets/stokai.ico"):
        opts.append("--icon=assets/stokai.ico")

    PyInstaller.__main__.run(opts)

    exe_path = os.path.join(DIST_DIR, APP_NAME, f"{APP_NAME}.exe")
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"[1/2] 빌드 완료: {exe_path} ({size_mb:.1f} MB)")
    else:
        print(f"[1/2] 빌드 실패: {exe_path} 가 생성되지 않았습니다")
        sys.exit(1)


def build_installer() -> None:
    """Inno Setup으로 인스톨러를 생성한다."""
    print(f"[2/2] Inno Setup 인스톨러 생성 시작")

    if not os.path.exists(INNO_COMPILER):
        print(f"[2/2] Inno Setup 컴파일러를 찾을 수 없습니다: {INNO_COMPILER}")
        print("       Inno Setup 6을 설치하거나 경로를 확인하세요.")
        sys.exit(1)

    if not os.path.exists(ISS_FILE):
        print(f"[2/2] ISS 파일을 찾을 수 없습니다: {ISS_FILE}")
        sys.exit(1)

    dist_app_dir = os.path.join(DIST_DIR, APP_NAME)
    if not os.path.isdir(dist_app_dir):
        print(f"[2/2] 빌드 출력 디렉토리가 없습니다: {dist_app_dir}")
        print("       먼저 --exe-only 로 PyInstaller 빌드를 실행하세요.")
        sys.exit(1)

    result = subprocess.run(
        [INNO_COMPILER, ISS_FILE],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    if result.returncode != 0:
        print(f"[2/2] Inno Setup 컴파일 실패:")
        print(result.stdout)
        print(result.stderr)
        sys.exit(1)

    installer_path = os.path.join(DIST_DIR, f"{APP_NAME}_Setup_{APP_VERSION}.exe")
    if os.path.exists(installer_path):
        size_mb = os.path.getsize(installer_path) / (1024 * 1024)
        print(f"[2/2] 인스톨러 생성 완료: {installer_path} ({size_mb:.1f} MB)")
    else:
        print(f"[2/2] 인스톨러 파일이 생성되지 않았습니다: {installer_path}")
        print("       ISCC 출력:")
        print(result.stdout)


def main() -> None:
    """빌드 진입점."""
    args = sys.argv[1:]

    if "--exe-only" in args:
        build_exe()
    elif "--installer" in args:
        build_installer()
    else:
        build_exe()
        build_installer()

    print("완료.")


if __name__ == "__main__":
    main()
