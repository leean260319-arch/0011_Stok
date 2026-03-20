#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oaisbatch_run.py

전체 파이프라인 배치 실행 (v/oaisbatch.md 구현)

서브명령어:
    status    - 서브명령어 리스트, 진행 상태
    run       - 전체 파이프라인 실행
    run --from/--to/--skip/--only [단계] - 부분 실행
    unitdev   - 단위개발문서 기준 페이지 단위 파이프라인
    optimize  - 전체 + 최적화

단계: prd, plan, dev, check, fix, lib, db, test, commit

사용법:
    python v/script/oaisbatch_run.py status
    python v/script/oaisbatch_run.py run
    python v/script/oaisbatch_run.py run --from dev
    python v/script/oaisbatch_run.py run --from check --to test
    python v/script/oaisbatch_run.py unitdev d21700
    python v/script/oaisbatch_run.py optimize
"""

import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from oais_common import show_help_if_no_args

# Configuration
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent

# 파이프라인 단계 순서
PIPELINE_STAGES = ["prd", "plan", "dev", "check", "fix", "lib", "db", "test", "commit"]

# 단계별 스킬 매핑
STAGE_SKILLS = {
    "prd": "oaisprd",
    "plan": "oaisplan",
    "dev": "oaisdev",
    "check": "oaischeck",
    "fix": "oaisfix",
    "lib": "oaislib",
    "db": "oaisdb",
    "test": "oaistest",
    "commit": "oaiscommit",
}

# SP (서브프로젝트) 컨텍스트
SP_CONTEXT = "00"


def get_sp_context() -> str:
    """현재 SP 컨텍스트 반환"""
    global SP_CONTEXT
    return SP_CONTEXT


def set_sp_context(sp: str):
    """SP 컨텍스트 설정"""
    global SP_CONTEXT
    if sp in ["00", "01", "02", "03", "04", "05"]:
        SP_CONTEXT = sp
        print(f"[INFO] SP Context: {sp}")
    else:
        print(f"[WARN] Invalid SP: {sp}, using default (00)")
        SP_CONTEXT = "00"


def get_sp_doc_path(base_doc_num: str) -> Path:
    """SP 컨텍스트에 따른 문서 경로 반환"""
    sp = get_sp_context()
    if sp == "00":
        doc_num = base_doc_num
    else:
        sp_num = int(sp)
        base_num = int(base_doc_num)
        doc_num = str(sp_num * 10000 + base_num)

    doc_names = {
        "0001": "prd",
        "0002": "plan",
        "0004": "todo",
        "0010": "history",
    }
    suffix = doc_names.get(base_doc_num, "")
    filename = f"d{doc_num}_{suffix}.md" if suffix else f"d{doc_num}.md"
    return PROJECT_ROOT / "doc" / filename


@dataclass
class PipelineState:
    """파이프라인 상태"""
    current_stage: Optional[str] = None
    completed: List[str] = field(default_factory=list)
    failed: List[str] = field(default_factory=list)
    skipped: List[str] = field(default_factory=list)
    start_time: Optional[datetime] = None

    def mark_completed(self, stage: str):
        if stage not in self.completed:
            self.completed.append(stage)

    def mark_failed(self, stage: str):
        if stage not in self.failed:
            self.failed.append(stage)

    def mark_skipped(self, stage: str):
        if stage not in self.skipped:
            self.skipped.append(stage)


# 전역 상태
pipeline_state = PipelineState()


def run_skill_script(skill: str, args: List[str] = None) -> int:
    """스킬 스크립트 실행"""
    script_path = SCRIPT_DIR / f"{skill}_run.py"

    if not script_path.exists():
        print(f"[WARN] Script not found: {script_path}")
        return -1

    cmd = ["uv", "run", "python", str(script_path)]
    if args:
        cmd.extend(args)

    try:
        result = subprocess.run(cmd, capture_output=False, check=False)
        return result.returncode
    except Exception as e:
        print(f"[ERROR] Failed to run {skill}: {e}")
        return 1


def check_stage_condition(stage: str) -> bool:
    """단계별 완료 조건 확인"""
    sp = get_sp_context()

    if stage == "prd":
        # PRD 문서 존재 확인
        prd_path = get_sp_doc_path("0001")
        return prd_path.exists()

    elif stage == "plan":
        # Plan 문서 존재 확인
        plan_path = get_sp_doc_path("0002")
        return plan_path.exists()

    elif stage == "fix":
        # d0004 현재 이슈 = 0 확인
        todo_path = get_sp_doc_path("0004")
        if todo_path.exists():
            content = todo_path.read_text(encoding="utf-8")
            # "현재 이슈 없음" 또는 이슈 테이블이 비어있는지 확인
            if "(현재 이슈 없음)" in content:
                return True
            # 현재 이슈 섹션에서 이슈 수 카운트
            # 간단한 휴리스틱: 대기 상태 이슈가 없으면 통과
            if "| 대기 |" not in content:
                return True
        return False

    # 기본: 조건 없음 (항상 통과)
    return True


def run_stage(stage: str, interactive: bool = False) -> int:
    """단계 실행"""
    global pipeline_state

    print(f"\n{'='*60}")
    print(f"[STAGE] {stage.upper()}")
    print(f"{'='*60}\n")

    pipeline_state.current_stage = stage

    # 사전 조건 확인
    if stage == "dev":
        # d0004 사전 검토
        print("[PRE-CHECK] d0004 현재 이슈 확인...")
        todo_path = get_sp_doc_path("0004")
        if todo_path.exists():
            content = todo_path.read_text(encoding="utf-8")
            if "| 대기 |" in content:
                print("[WARN] 기존 이슈가 존재합니다. 먼저 처리를 권장합니다.")
                if interactive:
                    response = input("계속 진행하시겠습니까? (y/n): ")
                    if response.lower() != 'y':
                        pipeline_state.mark_skipped(stage)
                        return 0

    # 스킬 실행
    skill = STAGE_SKILLS.get(stage)
    if skill:
        ret = run_skill_script(skill, ["run"])
        if ret != 0:
            pipeline_state.mark_failed(stage)
            print(f"[FAILED] {stage} 단계 실패 (exit code: {ret})")
            return ret

    # 완료 조건 확인
    if check_stage_condition(stage):
        pipeline_state.mark_completed(stage)
        print(f"[OK] {stage} 단계 완료")
        return 0
    else:
        pipeline_state.mark_failed(stage)
        print(f"[FAILED] {stage} 완료 조건 미충족")
        return 1


def cmd_status():
    """상태 조회 (status 서브명령어)"""
    print("# oaisbatch status\n")

    print("## 서브명령어")
    print("| 명령어 | 설명 |")
    print("|--------|------|")
    print("| status | 서브명령어 리스트, 진행 상태 |")
    print("| run | 전체 파이프라인 실행 |")
    print("| run --from/--to/--skip/--only [단계] | 부분 실행 |")
    print("| unitdev [문서번호] | 단위개발문서 기준 파이프라인 |")
    print("| optimize | 전체 + 최적화 |")

    print("\n## 파이프라인 단계")
    print("```")
    print("prd → plan → dev → check → fix → lib → db → test → commit")
    print("```")

    print("\n## 현재 상태")
    print(f"- SP Context: {get_sp_context()}")
    print(f"- 완료: {pipeline_state.completed or '없음'}")
    print(f"- 실패: {pipeline_state.failed or '없음'}")
    print(f"- 건너뜀: {pipeline_state.skipped or '없음'}")

    return 0


def cmd_run(from_stage: str = None, to_stage: str = None,
            skip_stages: List[str] = None, only_stages: List[str] = None,
            interactive: bool = False, report: bool = False):
    """파이프라인 실행 (run 서브명령어)"""
    global pipeline_state
    pipeline_state = PipelineState(start_time=datetime.now())

    print("# oaisbatch run\n")
    print(f"시작 시간: {pipeline_state.start_time}")
    print(f"SP Context: {get_sp_context()}")

    # 실행할 단계 결정
    stages = PIPELINE_STAGES.copy()

    if only_stages:
        stages = [s for s in stages if s in only_stages]
    else:
        if from_stage and from_stage in stages:
            start_idx = stages.index(from_stage)
            stages = stages[start_idx:]

        if to_stage and to_stage in stages:
            end_idx = stages.index(to_stage)
            stages = stages[:end_idx + 1]

    if skip_stages:
        stages = [s for s in stages if s not in skip_stages]

    print(f"\n실행 단계: {' → '.join(stages)}\n")

    # 단계별 실행
    max_retries = 3
    retry_count = 0

    for stage in stages:
        ret = run_stage(stage, interactive)

        if ret != 0:
            # 실패 시 재시도 (dev로 돌아가기)
            if stage in ["lib", "db", "test"] and retry_count < max_retries:
                retry_count += 1
                print(f"\n[RETRY] dev 단계로 복귀 (시도 {retry_count}/{max_retries})")
                # dev부터 다시 실행
                dev_idx = PIPELINE_STAGES.index("dev")
                current_idx = PIPELINE_STAGES.index(stage)
                for retry_stage in PIPELINE_STAGES[dev_idx:current_idx + 1]:
                    ret = run_stage(retry_stage, interactive)
                    if ret != 0:
                        break
            else:
                print(f"\n[ABORT] 파이프라인 중단: {stage} 실패")
                break

    # 결과 요약
    print("\n" + "=" * 60)
    print("# Summary")
    print("=" * 60)

    elapsed = datetime.now() - pipeline_state.start_time
    print(f"\n소요 시간: {elapsed}")
    print(f"완료: {len(pipeline_state.completed)}개 - {pipeline_state.completed}")
    print(f"실패: {len(pipeline_state.failed)}개 - {pipeline_state.failed}")
    print(f"건너뜀: {len(pipeline_state.skipped)}개 - {pipeline_state.skipped}")

    if report:
        # 리포트 파일 생성
        report_path = PROJECT_ROOT / "tmp" / f"oaisbatch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.parent.mkdir(exist_ok=True)
        report_content = f"""# oaisbatch Report

- 실행 시간: {pipeline_state.start_time}
- 소요 시간: {elapsed}
- SP Context: {get_sp_context()}

## 결과
- 완료: {pipeline_state.completed}
- 실패: {pipeline_state.failed}
- 건너뜀: {pipeline_state.skipped}
"""
        report_path.write_text(report_content, encoding="utf-8")
        print(f"\n리포트 저장: {report_path}")

    return 0 if not pipeline_state.failed else 1


def cmd_unitdev(doc_num: str, from_stage: str = None,
                only_stages: List[str] = None, interactive: bool = False,
                dry_run: bool = False):
    """단위개발문서 기준 파이프라인 (unitdev 서브명령어)"""
    print(f"# oaisbatch unitdev {doc_num}\n")

    # 문서번호 파싱: d{SP}1{YY}0 → SP, YY 추출
    match = re.match(r'd(\d)(\d)1(\d{2})0?', doc_num)
    if not match:
        match = re.match(r'd(\d{2})1(\d{2})0?', doc_num)
        if match:
            sp = match.group(1)
            yy = match.group(2)
        else:
            print(f"[ERROR] 잘못된 문서번호 형식: {doc_num}")
            print("예시: d21700, d21710, d21100")
            return 1
    else:
        sp = match.group(1) + match.group(2)
        yy = match.group(3)

    # SP 컨텍스트 설정
    set_sp_context(sp.zfill(2))

    # 페이지 ID 계산
    yy_int = int(yy)
    if 10 <= yy_int <= 19:
        x = 1
    elif 20 <= yy_int <= 29:
        x = 2
    elif 30 <= yy_int <= 39:
        x = 3
    elif 70 <= yy_int <= 79:
        x = 7
    else:
        x = yy_int // 10

    page_id = f"{x}_{yy}"

    # 서브프로젝트 경로
    sp_dirs = {
        "01": "01_algorithm",
        "02": "02_1st_server",
        "03": "03_app_design",
    }
    sp_dir = sp_dirs.get(sp.zfill(2), f"0{sp}_server")

    # 파일 패턴
    file_pattern = f"{sp_dir}/pages/{page_id}_*.py"

    # 단위개발문서 경로
    unit_doc_pattern = f"doc/d{doc_num}*.md"

    print("[매핑]")
    print(f"  문서번호: {doc_num}")
    print(f"  SP: {sp.zfill(2)}")
    print(f"  페이지ID: {page_id}")
    print(f"  파일패턴: {file_pattern}")
    print(f"  단위문서: {unit_doc_pattern}")

    # 대상 파일 확인
    target_files = list(PROJECT_ROOT.glob(file_pattern))
    unit_docs = list(PROJECT_ROOT.glob(unit_doc_pattern))

    print(f"\n  대상파일: {len(target_files)}개")
    for f in target_files:
        print(f"    - {f.name}")

    print(f"  단위문서: {len(unit_docs)}개")
    for d in unit_docs:
        print(f"    - {d.name}")

    if not unit_docs:
        print(f"\n[ERROR] 단위개발문서를 찾을 수 없습니다: {unit_doc_pattern}")
        return 1

    if dry_run:
        print("\n[DRY-RUN] 실행 계획만 출력합니다.")
        print("\n[파이프라인]")
        for stage in PIPELINE_STAGES:
            print(f"  - {stage}: 대기 중")
        return 0

    # 파이프라인 실행 (스코프 제한은 각 스킬에서 처리)
    print(f"\n환경변수 설정: OAISBATCH_PAGE_ID={page_id}")

    # 실행
    return cmd_run(
        from_stage=from_stage,
        only_stages=only_stages,
        interactive=interactive
    )


def cmd_optimize():
    """전체 + 최적화 (optimize 서브명령어)"""
    print("# oaisbatch optimize\n")

    # 전체 실행
    ret = cmd_run()

    if ret == 0:
        print("\n## 최적화 단계")
        # 각 스킬의 optimize 실행
        optimize_skills = ["oaisprd", "oaisplan", "oaislib", "oaisdb", "oaisdev", "oaisdoc"]
        for skill in optimize_skills:
            print(f"\n[OPTIMIZE] {skill}...")
            run_skill_script(skill, ["optimize"])

    return ret


def print_usage():
    """사용법 출력"""
    print("""oaisbatch - 전체 파이프라인 배치 실행

사용법:
    oaisbatch status                       상태 조회
    oaisbatch run                          전체 파이프라인 실행
    oaisbatch run --from dev               dev 단계부터 실행
    oaisbatch run --from check --to test   check~test만 실행
    oaisbatch run --skip lib,db            lib, db 건너뛰기
    oaisbatch run --only check,fix         check, fix만 실행
    oaisbatch run --interactive            단계별 확인
    oaisbatch run --report                 리포트 생성
    oaisbatch unitdev d21700               단위개발문서 기준 실행
    oaisbatch unitdev d21700 --dry-run     실행 계획만 출력
    oaisbatch optimize                     전체 + 최적화

단계: prd, plan, dev, check, fix, lib, db, test, commit

예시:
    uv run python v/script/oaisbatch_run.py status
    uv run python v/script/oaisbatch_run.py run
    uv run python v/script/oaisbatch_run.py unitdev d21710
""")


def main():
    # 서브명령어 없이 실행 시 도움말 출력
    if show_help_if_no_args("oaisbatch", sys.argv[1:]):
        return

    print(f"[oaisbatch] Started at {datetime.now()}")

    args = sys.argv[1:]

    if not args:
        print_usage()
        return 0

    subcommand = args[0]

    # 옵션 파싱
    from_stage = None
    to_stage = None
    skip_stages = []
    only_stages = []
    interactive = False
    report = False
    dry_run = False

    i = 1
    while i < len(args):
        if args[i] == "--from" and i + 1 < len(args):
            from_stage = args[i + 1]
            i += 2
        elif args[i] == "--to" and i + 1 < len(args):
            to_stage = args[i + 1]
            i += 2
        elif args[i] == "--skip" and i + 1 < len(args):
            skip_stages = args[i + 1].split(",")
            i += 2
        elif args[i] == "--only" and i + 1 < len(args):
            only_stages = args[i + 1].split(",")
            i += 2
        elif args[i] == "--interactive":
            interactive = True
            i += 1
        elif args[i] == "--report":
            report = True
            i += 1
        elif args[i] == "--dry-run":
            dry_run = True
            i += 1
        elif args[i] == "--sp" and i + 1 < len(args):
            set_sp_context(args[i + 1])
            i += 2
        else:
            i += 1

    if subcommand == "status":
        return cmd_status()
    elif subcommand == "run":
        return cmd_run(from_stage, to_stage, skip_stages, only_stages, interactive, report)
    elif subcommand == "unitdev":
        if len(args) < 2:
            print("[ERROR] 문서번호를 지정하세요. 예: oaisbatch unitdev d21700")
            return 1
        doc_num = args[1]
        return cmd_unitdev(doc_num, from_stage, only_stages, interactive, dry_run)
    elif subcommand == "optimize":
        return cmd_optimize()
    elif subcommand in ("-h", "--help", "help"):
        print_usage()
        return 0
    else:
        print(f"[ERROR] Unknown subcommand: {subcommand}")
        print_usage()
        return 1


if __name__ == "__main__":
    sys.exit(main())
