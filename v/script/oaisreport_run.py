#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""oaisreport_run.py - 자동 리포트 생성 (상세: doc/a0009_script.md)"""

import sys
import re
from datetime import datetime
from oais_common import (
    show_help_if_no_args, PROJECT_ROOT, DOC_DIR, TMP_DIR, TODO_FILE,
    log_ok, log_warn, log_info, log_tip
)

TEMPLATE_DIR = PROJECT_ROOT / "v" / "template"
REPORTS_DIR = TMP_DIR / "reports"


def print_usage():
    """사용법 출력"""
    print(f"Log started at {datetime.now()}")
    print("oaisreport - 자동 리포트 생성")
    print()
    print("사용법:")
    print("    oaisreport run              신규 리포트 생성 (기본)")
    print("    oaisreport update [name]    기존 리포트 업데이트")
    print("    oaisreport list             생성된 리포트 목록 확인")
    print()
    print("옵션:")
    print("    --source [파일]            데이터 소스 지정 (기본: d0004_todo.md)")
    print("    --template [템플릿]        템플릿 지정 (weekly, monthly, custom)")
    print("    --format [형식]            출력 형식 (md, pdf, pptx)")
    print("    --out [경로]               출력 경로 지정")
    print()
    print("예시:")
    print("    python v/script/oaisreport_run.py run --template weekly")
    print("    python v/script/oaisreport_run.py update weekly_report_2025_w01.md")
    print("    python v/script/oaisreport_run.py list")


def extract_todo_stats():
    """d0004_todo.md에서 통계 추출"""
    if not TODO_FILE.exists():
        return None

    content = TODO_FILE.read_text(encoding="utf-8")

    # 미완료 항목: - [ ]
    incomplete = len(re.findall(r"-\s*\[\s*\]", content))

    # 완료 항목: - [x]
    complete = len(re.findall(r"-\s*\[x\]", content, re.IGNORECASE))

    # 우선순위별 분류
    critical = len(re.findall(r"\[CRITICAL\]", content, re.IGNORECASE))
    error = len(re.findall(r"\[ERROR\]", content, re.IGNORECASE))
    warning = len(re.findall(r"\[WARNING\]", content, re.IGNORECASE))
    info = len(re.findall(r"\[INFO\]", content, re.IGNORECASE))

    return {
        "total": incomplete + complete,
        "incomplete": incomplete,
        "complete": complete,
        "critical": critical,
        "error": error,
        "warning": warning,
        "info": info
    }


def get_week_number():
    """현재 주차 반환"""
    today = datetime.now()
    return today.isocalendar()[1]


def generate_weekly_report(stats, options):
    """주간 리포트 생성"""
    today = datetime.now()
    week_num = get_week_number()
    year = today.year

    report = f"""# 주간 업무 현황 리포트 (Week {week_num}, {year})

생성일시: {today.strftime('%Y-%m-%d %H:%M:%S')}
데이터 소스: {options.get('source', 'd0004_todo.md')}

---

## 1. 요약

| 항목 | 수량 |
|------|------|
| 전체 이슈 | {stats['total']} 건 |
| 신규/미완료 | {stats['incomplete']} 건 |
| 완료됨 | {stats['complete']} 건 |

### 우선순위별 분포

| 우선순위 | 수량 |
|----------|------|
| CRITICAL | {stats['critical']} 건 |
| ERROR | {stats['error']} 건 |
| WARNING | {stats['warning']} 건 |
| INFO | {stats['info']} 건 |

---

## 2. 상세 내용

### 2.1 주요 진행 사항

- (자동 생성된 내용)
- 데이터 분석 기반 상세 내용은 data-analyst 서브에이전트 활용 필요

### 2.2 이슈 및 리스크

- CRITICAL: {stats['critical']}건 주의 필요
- ERROR: {stats['error']}건 검토 필요

---

## 3. 다음 주 계획

- 미완료 이슈 {stats['incomplete']}건 처리
- 우선순위별 순차 대응

---

## 4. 비고

- 이 리포트는 oaisreport에 의해 자동 생성되었습니다.
- 상세 분석은 서브에이전트를 통해 수행할 수 있습니다.

---
"""
    return report


def generate_monthly_report(stats, options):
    """월간 리포트 생성"""
    today = datetime.now()
    month = today.month
    year = today.year

    report = f"""# 월간 업무 현황 리포트 ({year}년 {month}월)

생성일시: {today.strftime('%Y-%m-%d %H:%M:%S')}

---

## 1. 월간 요약

| 항목 | 수량 |
|------|------|
| 총 이슈 | {stats['total']} 건 |
| 완료 | {stats['complete']} 건 |
| 미완료 | {stats['incomplete']} 건 |
| 완료율 | {stats['complete'] * 100 // max(stats['total'], 1)}% |

---

## 2. 우선순위별 현황

| 우선순위 | 수량 | 비고 |
|----------|------|------|
| CRITICAL | {stats['critical']} | 즉시 대응 |
| ERROR | {stats['error']} | 빠른 대응 |
| WARNING | {stats['warning']} | 검토 필요 |
| INFO | {stats['info']} | 참고 |

---

## 3. 주요 활동

(월간 주요 활동 요약)

---

## 4. 다음 달 계획

(다음 달 계획)

---
"""
    return report


def cmd_run(options):
    """신규 리포트 생성 (run 서브명령어)"""
    dry_run = options.get("dry_run", False)
    print("# oaisreport run\n")
    if dry_run:
        print("[DRY-RUN] 실제 파일 생성 없이 미리보기만 실행\n")

    template_type = options.get("template", "weekly")
    output_format = options.get("format", "md")
    source = options.get("source", "d0004_todo.md")

    print(f"템플릿: {template_type}")
    print(f"데이터 소스: {source}")
    print(f"출력 형식: {output_format}")
    print()

    # 데이터 수집
    print("[1/4] 데이터 수집...")
    stats = extract_todo_stats()

    if not stats:
        print(f"  [WARN] {TODO_FILE}가 없습니다.")
        stats = {
            "total": 0, "incomplete": 0, "complete": 0,
            "critical": 0, "error": 0, "warning": 0, "info": 0
        }

    print(f"  총 {stats['total']}건 발견")

    # 리포트 생성
    print("[2/4] 리포트 생성...")
    if template_type == "monthly":
        report_content = generate_monthly_report(stats, options)
        filename_prefix = "monthly_report"
    else:
        report_content = generate_weekly_report(stats, options)
        filename_prefix = "weekly_report"

    # 파일 저장
    print("[3/4] 파일 저장...")

    today = datetime.now()
    if template_type == "monthly":
        filename = f"{filename_prefix}_{today.year}_{today.month:02d}.md"
    else:
        week_num = get_week_number()
        filename = f"{filename_prefix}_{today.year}_w{week_num:02d}.md"

    output_path = options.get("out")
    if output_path:
        report_file = Path(output_path)
    else:
        report_file = REPORTS_DIR / filename

    if dry_run:
        print(f"  [DRY-RUN] 저장 예정: {report_file}")
    else:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text(report_content, encoding="utf-8")
        print(f"  저장됨: {report_file}")

    # 완료
    print("[4/4] 완료")
    print()
    print("---")
    print(f"[OK] 리포트 생성됨: {report_file}")

    return 0


def cmd_update(args, options):
    """기존 리포트 업데이트 (update 서브명령어)"""
    dry_run = options.get("dry_run", False)
    print("# oaisreport update\n")
    if dry_run:
        print("[DRY-RUN] 실제 파일 수정 없이 미리보기만 실행\n")

    if not args:
        print("[ERROR] 리포트 파일명을 지정하세요.")
        print("사용법: oaisreport update [name]")
        print()
        print("[TIP] oaisreport list 로 목록을 확인하세요.")
        return 1

    report_name = args[0]
    report_file = REPORTS_DIR / report_name

    if not report_file.exists():
        # 파일명만 입력한 경우
        if not report_name.endswith(".md"):
            report_file = REPORTS_DIR / f"{report_name}.md"

        if not report_file.exists():
            print(f"[ERROR] 리포트를 찾을 수 없습니다: {report_name}")
            return 1

    print(f"대상 리포트: {report_file}")
    print()

    # 최신 데이터로 업데이트
    print("[1/3] 최신 데이터 수집...")
    stats = extract_todo_stats()

    if not stats:
        print("  [WARN] 데이터 소스가 없습니다.")
        return 1

    print(f"  총 {stats['total']}건 발견")

    # 기존 내용 읽기
    print("[2/3] 리포트 업데이트...")
    content = report_file.read_text(encoding="utf-8")

    # 생성일시 업데이트
    today = datetime.now()
    content = re.sub(
        r"생성일시: .+",
        f"생성일시: {today.strftime('%Y-%m-%d %H:%M:%S')} (업데이트)",
        content
    )

    # 통계 업데이트
    content = re.sub(
        r"\| 전체 이슈 \| \d+ 건 \|",
        f"| 전체 이슈 | {stats['total']} 건 |",
        content
    )
    content = re.sub(
        r"\| 신규/미완료 \| \d+ 건 \|",
        f"| 신규/미완료 | {stats['incomplete']} 건 |",
        content
    )
    content = re.sub(
        r"\| 완료됨 \| \d+ 건 \|",
        f"| 완료됨 | {stats['complete']} 건 |",
        content
    )

    if dry_run:
        print(f"  [DRY-RUN] 수정 예정: {report_file}")
        print(f"  [DRY-RUN] 업데이트될 통계: 전체 {stats['total']}건, 미완료 {stats['incomplete']}건, 완료 {stats['complete']}건")
    else:
        report_file.write_text(content, encoding="utf-8")

    print("[3/3] 완료")
    print()
    print(f"[OK] 리포트 업데이트됨: {report_file}")

    return 0


def cmd_list():
    """생성된 리포트 목록 확인 (list 서브명령어)"""
    print("# oaisreport list\n")

    if not REPORTS_DIR.exists():
        print(f"[INFO] 리포트 디렉토리가 없습니다: {REPORTS_DIR}")
        print("[TIP] oaisreport run 으로 리포트를 생성하세요.")
        return 0

    reports = list(REPORTS_DIR.glob("*.md"))

    if not reports:
        print("[INFO] 생성된 리포트가 없습니다.")
        return 0

    # 수정 시간순 정렬
    reports.sort(key=lambda p: p.stat().st_mtime, reverse=True)

    print(f"리포트 디렉토리: {REPORTS_DIR}")
    print(f"총 리포트: {len(reports)}개")
    print()

    print("## 리포트 목록\n")
    print("| 파일명 | 크기 | 수정일 |")
    print("|--------|------|--------|")

    for report in reports:
        size = report.stat().st_size
        mtime = datetime.fromtimestamp(report.stat().st_mtime)
        mtime_str = mtime.strftime("%Y-%m-%d %H:%M")

        if size < 1024:
            size_str = f"{size} B"
        else:
            size_str = f"{size // 1024} KB"

        print(f"| {report.name} | {size_str} | {mtime_str} |")

    print()
    print("[TIP] oaisreport update [name] 으로 업데이트할 수 있습니다.")

    return 0


def parse_options(args):
    """옵션 파싱"""
    options = {
        "template": "weekly",
        "format": "md",
        "source": "d0004_todo.md",
        "dry_run": "--dry-run" in args
    }

    # --source
    if "--source" in args:
        idx = args.index("--source")
        if idx + 1 < len(args):
            options["source"] = args[idx + 1]

    # --template
    if "--template" in args:
        idx = args.index("--template")
        if idx + 1 < len(args):
            options["template"] = args[idx + 1]

    # --format
    if "--format" in args:
        idx = args.index("--format")
        if idx + 1 < len(args):
            options["format"] = args[idx + 1]

    # --out
    if "--out" in args:
        idx = args.index("--out")
        if idx + 1 < len(args):
            options["out"] = args[idx + 1]

    return options


def main():
    # 서브명령어 없이 실행 시 도움말 출력
    if show_help_if_no_args("oaisreport", sys.argv[1:]):
        return

    print(f"Log started at {datetime.now()}")

    args = sys.argv[1:]

    if not args:
        print_usage()
        return 0

    cmd = args[0].lower()
    cmd_args = [a for a in args[1:] if not a.startswith("--")]
    options = parse_options(args)

    if cmd == "run":
        return cmd_run(options)
    elif cmd == "update":
        return cmd_update(cmd_args, options)
    elif cmd == "list":
        return cmd_list()
    else:
        print(f"[ERROR] Unknown command: {cmd}")
        print_usage()
        return 1


if __name__ == "__main__":
    sys.exit(main())
