#!/usr/bin/env python3
"""
oais_common.py

OAIS 스킬 공통 모듈
- 공통 import 및 상수
- 로깅 설정
- 헬퍼 함수
"""

# ============================================================
# 공통 import (모든 oais 스크립트에서 사용)
# ============================================================
import re
import sys
import logging
from pathlib import Path
from datetime import datetime

# ============================================================
# Windows 콘솔 UTF-8 인코딩 설정
# ============================================================
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# ============================================================
# 공통 경로 상수
# ============================================================
SCRIPT_DIR = Path(__file__).parent
V_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = V_DIR.parent
DOC_DIR = PROJECT_ROOT / "doc"
TMP_DIR = PROJECT_ROOT / "tmp"
DATA_DIR = PROJECT_ROOT / "data"

# ============================================================
# 공통 파일 경로
# ============================================================
TODO_FILE = DOC_DIR / "d0004_todo.md"
HISTORY_FILE = DOC_DIR / "d0010_history.md"
PRD_FILE = DOC_DIR / "d0001_prd.md"

# ============================================================
# 상태 심볼 (SuperClaude 토큰 효율 모드)
# ============================================================
SYM_OK = "[OK]"           # 완료, 성공
SYM_FAIL = "[FAIL]"       # 실패, 에러
SYM_WARN = "[WARN]"       # 경고
SYM_INFO = "[INFO]"       # 정보
SYM_PROG = "[...]"        # 진행 중
SYM_WAIT = "[WAIT]"       # 대기
SYM_CRIT = "[CRIT]"       # 긴급/중요
SYM_TIP = "[TIP]"         # 팁/힌트
SYM_DRY = "[DRY-RUN]"     # 드라이런 모드

# 논리 심볼 (압축 출력용)
SYM_ARROW = "->"          # leads to
SYM_TRANS = "=>"          # transforms to
SYM_SEQ = ">>"            # sequence, then
SYM_AND = "&"             # and, combine
SYM_OR = "|"              # separator, or
SYM_DEF = ":"             # define, specify
SYM_EQ = "=="             # equivalent
SYM_NEQ = "!="            # not equal
SYM_APPROX = "~"          # approximately

# ============================================================
# 공통 플래그 (SuperClaude 플래그 시스템)
# ============================================================
# 분석 플래그
FLAG_THINK = "--think"           # 다중 파일 분석 (~4K 토큰)
FLAG_THINK_HARD = "--think-hard" # 아키텍처 분석 (~10K 토큰)
FLAG_ULTRATHINK = "--ultrathink" # 시스템 전체 분석 (~32K 토큰)

# 효율 플래그
FLAG_UC = "--uc"                 # 압축 출력 (30-50% 토큰 절감)
FLAG_PLAN = "--plan"             # 실행 전 계획 표시
FLAG_VALIDATE = "--validate"     # 사전 검증
FLAG_SAFE = "--safe-mode"        # 최대 검증 모드
FLAG_DRY_RUN = "--dry-run"       # 실제 실행 없이 미리보기

# MCP 플래그
FLAG_C7 = "--c7"                 # Context7 서버
FLAG_SEQ = "--seq"               # Sequential 서버
FLAG_MAGIC = "--magic"           # Magic 서버
FLAG_PLAY = "--play"             # Playwright 서버
FLAG_ALL_MCP = "--all-mcp"       # 모든 MCP 서버
FLAG_NO_MCP = "--no-mcp"         # MCP 비활성화

# 범위 플래그
FLAG_SCOPE_FILE = "--scope file"
FLAG_SCOPE_MODULE = "--scope module"
FLAG_SCOPE_PROJECT = "--scope project"
FLAG_SCOPE_SYSTEM = "--scope system"

# 반복 플래그
FLAG_LOOP = "--loop"             # 반복 개선 모드
FLAG_ITERATIONS = "--iterations" # 반복 횟수 지정

# ============================================================
# 로깅 설정
# ============================================================
class OaisLogger:
    """OAIS 스킬용 로거 클래스"""

    _loggers = {}

    @classmethod
    def get_logger(cls, name: str, level: int = logging.INFO) -> logging.Logger:
        """
        스킬별 로거 반환

        Args:
            name: 로거 이름 (보통 스킬 이름)
            level: 로깅 레벨 (기본: INFO)

        Returns:
            설정된 로거 인스턴스
        """
        if name in cls._loggers:
            return cls._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(level)

        # 핸들러가 없으면 추가
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(level)

            # 포맷 설정 (간결한 형식)
            formatter = logging.Formatter(
                '[%(levelname)s] %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        cls._loggers[name] = logger
        return logger

    @classmethod
    def set_level(cls, name: str, level: int) -> None:
        """로거 레벨 변경"""
        if name in cls._loggers:
            cls._loggers[name].setLevel(level)
            for handler in cls._loggers[name].handlers:
                handler.setLevel(level)


def get_logger(skill_name: str, verbose: bool = False) -> logging.Logger:
    """
    스킬용 로거 간편 생성

    Args:
        skill_name: 스킬 이름
        verbose: True면 DEBUG 레벨, False면 INFO 레벨

    Returns:
        설정된 로거
    """
    level = logging.DEBUG if verbose else logging.INFO
    return OaisLogger.get_logger(skill_name, level)


# ============================================================
# 출력 헬퍼 함수 (print 대체)
# ============================================================
def log_info(msg: str) -> None:
    """정보 메시지 출력"""
    print(f"[INFO] {msg}")

def log_ok(msg: str) -> None:
    """성공 메시지 출력"""
    print(f"[OK] {msg}")

def log_warn(msg: str) -> None:
    """경고 메시지 출력"""
    print(f"[WARN] {msg}")

def log_error(msg: str) -> None:
    """에러 메시지 출력"""
    print(f"[ERROR] {msg}")

def log_tip(msg: str) -> None:
    """팁 메시지 출력"""
    print(f"[TIP] {msg}")

def log_dry_run(msg: str) -> None:
    """dry-run 메시지 출력"""
    print(f"[DRY-RUN] {msg}")


# ============================================================
# 스킬 문서 파싱
# ============================================================
def parse_skill_file(skill_name: str) -> dict:
    """
    스킬 문서(v/oais*.md)를 파싱하여 정보 추출

    Args:
        skill_name: 스킬 이름 (예: "oaisstart", "oaissync")

    Returns:
        스킬 정보 딕셔너리
    """
    skill_file = V_DIR / f"{skill_name}.md"

    result = {
        "name": skill_name,
        "purpose": "",
        "all_commands": [],
        "file_exists": False
    }

    if not skill_file.exists():
        return result

    result["file_exists"] = True
    content = skill_file.read_text(encoding="utf-8")

    # 제목에서 용도 추출 (# oaisXXX - 용도)
    title_match = re.search(r"^# \w+ - (.+)$", content, re.MULTILINE)
    if title_match:
        result["purpose"] = title_match.group(1).strip()

    # 서브명령어 테이블에서 명령어 추출
    commands = []

    # 패턴 1: | `명령어` | 설명 | 형식
    cmd_pattern = r"\|\s*`([^`]+)`\s*\|"
    for match in re.finditer(cmd_pattern, content):
        cmd = match.group(1).strip()
        # 스킬명 제거하고 서브명령어만 추출
        if cmd.startswith(skill_name):
            subcmd = cmd.replace(skill_name, "").strip()
            if subcmd and subcmd not in commands:
                commands.append(subcmd)

    result["all_commands"] = commands
    return result


def print_skill_help(skill_name: str) -> None:
    """
    스킬 도움말 출력 (oaishelp와 동일한 형식)

    Args:
        skill_name: 스킬 이름 (예: "oaisstart", "oaissync")
    """
    skill = parse_skill_file(skill_name)

    if not skill["file_exists"]:
        log_error(f"스킬 문서를 찾을 수 없습니다: v/{skill_name}.md")
        return

    print(f"## {skill['name']}")
    print()
    print(f"**용도**: {skill['purpose']}")
    print()
    print("### 서브명령어")
    print()
    if skill["all_commands"]:
        for cmd in skill["all_commands"]:
            print(f"- `{skill['name']} {cmd}`")
    else:
        print("- (서브명령어 없음)")
    print()
    print(f"**상세 문서**: `v/{skill['name']}.md`")


def show_help_if_no_args(skill_name: str, args: list) -> bool:
    """
    인자가 없으면 도움말을 출력하고 True 반환

    Args:
        skill_name: 스킬 이름
        args: sys.argv[1:] 리스트

    Returns:
        도움말을 출력했으면 True, 아니면 False
    """
    if not args:
        print_skill_help(skill_name)
        return True
    return False


# ============================================================
# 유틸리티 함수
# ============================================================
def ensure_dir(path: Path) -> Path:
    """디렉토리가 없으면 생성"""
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_timestamp() -> str:
    """현재 타임스탬프 반환 (YYYY-MM-DD HH:MM:SS)"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_date() -> str:
    """현재 날짜 반환 (YYYY-MM-DD)"""
    return datetime.now().strftime("%Y-%m-%d")
