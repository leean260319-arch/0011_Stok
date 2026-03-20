"""
[oaispaper_run.py]
이 스크립트는 'oaispaper' 스킬의 핵심 실행 파일로, 논문 데이터의 정합성을 검사하고 관리합니다.

사용법:
    uv run python v/script/oaispaper_run.py run [--limit N] [--dry-run] [--skip-organize]
    uv run python v/script/oaispaper_run.py status
    uv run python v/script/oaispaper_run.py fix [--folder ID]
    uv run python v/script/oaispaper_run.py delete-broken [--dry-run]
"""

import argparse
import sys
import json
from pathlib import Path
from datetime import datetime
from oais_common import show_help_if_no_args

# 상수 정의
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PAPER_DIR = PROJECT_ROOT / "02_paper"
DOWN_DIR = PROJECT_ROOT / "01_down"

# 품질 기준
QUALITY_THRESHOLDS = {
    "summary": 500,      # 서머리 최소 bytes
    "english": 1000,     # 영문 전문 최소 bytes
    "korean": 1000,      # 한글 전문 최소 bytes
}

# 템플릿/미완료 마커
INCOMPLETE_MARKERS = [
    "(추출 필요)", "(추후 작성)", "[저자명]", "[제목]",
    "# 번역 필요", "[Translation Required]", "내용 자동 생성됨",
    "TODO", "(미작성)", "[미완료]", "작성 예정"
]

def check_file_quality(file_path, file_type):
    """
    파일의 내부 내용을 읽어 품질을 정밀 검사합니다.
    """
    # 1. 인코딩 검사
    try:
        content = file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return "인코딩 오류 (파일 깨짐)"
    except Exception as e:
        return f"읽기 실패 ({str(e)})"

    # 2. 최소 분량 검사
    threshold = QUALITY_THRESHOLDS.get(file_type, 500)
    if len(content.strip()) < threshold:
        return f"내용 부족 ({len(content)} bytes < {threshold})"

    # 3. 템플릿/미완료 마커 검사
    for marker in INCOMPLETE_MARKERS:
        if marker in content:
            return f"미완료 ('{marker}' 포함)"

    return None


def find_best_file(file_list, file_type):
    """
    여러 파일 중 가장 품질이 좋은 파일을 선택합니다.
    Returns: (best_file, duplicates_to_remove, quality_issue)
    """
    if not file_list:
        return None, [], None

    if len(file_list) == 1:
        issue = check_file_quality(file_list[0], file_type)
        return file_list[0], [], issue

    # 여러 파일이 있는 경우: 품질 체크 후 최고 품질 파일 선택
    quality_results = []
    for f in file_list:
        issue = check_file_quality(f, file_type)
        size = f.stat().st_size
        quality_results.append({
            "file": f,
            "issue": issue,
            "size": size,
            "is_ok": issue is None
        })

    # 품질 OK인 파일 우선, 그 다음 파일 크기 순
    quality_results.sort(key=lambda x: (not x["is_ok"], -x["size"]))

    best = quality_results[0]
    duplicates = [r["file"] for r in quality_results[1:]]

    return best["file"], duplicates, best["issue"]


def check_paper_completeness(folder_path):
    """
    논문 폴더의 완성도를 상세히 검사합니다.
    Returns: dict with status for each file type
    """
    result = {
        "folder": folder_path.name,
        "pdf": {"exists": False, "path": None},
        "summary": {"exists": False, "path": None, "quality": None, "issue": None},
        "english": {"exists": False, "path": None, "quality": None, "issue": None},
        "korean": {"exists": False, "path": None, "quality": None, "issue": None},
        "duplicates": [],  # 삭제 대상 중복 파일 목록
        "needs_work": []
    }

    if not folder_path.is_dir():
        return result

    files = list(folder_path.iterdir())

    # PDF 체크
    pdf_files = [f for f in files if f.suffix.lower() == '.pdf']
    if pdf_files:
        result["pdf"]["exists"] = True
        result["pdf"]["path"] = str(pdf_files[0])
    else:
        result["needs_work"].append("pdf_missing")

    # 서머리 체크 (중복 감지 포함)
    summary_files = [f for f in files if "_00_" in f.name and "서머리" in f.name]
    if summary_files:
        best_file, duplicates, issue = find_best_file(summary_files, "summary")
        result["summary"]["exists"] = True
        result["summary"]["path"] = str(best_file)
        result["duplicates"].extend([str(d) for d in duplicates])
        if duplicates:
            result["needs_work"].append("summary_duplicates")
        if issue:
            result["summary"]["quality"] = "incomplete"
            result["summary"]["issue"] = issue
            result["needs_work"].append("summary_incomplete")
        else:
            result["summary"]["quality"] = "ok"
    else:
        result["needs_work"].append("summary_missing")

    # 영문 전문 체크 (중복 감지 포함)
    eng_files = [f for f in files if "_03_" in f.name and "전문(영어)" in f.name]
    if eng_files:
        best_file, duplicates, issue = find_best_file(eng_files, "english")
        result["english"]["exists"] = True
        result["english"]["path"] = str(best_file)
        result["duplicates"].extend([str(d) for d in duplicates])
        if duplicates:
            result["needs_work"].append("english_duplicates")
        if issue:
            result["english"]["quality"] = "incomplete"
            result["english"]["issue"] = issue
            result["needs_work"].append("english_incomplete")
        else:
            result["english"]["quality"] = "ok"
    else:
        result["needs_work"].append("english_missing")

    # 한글 전문 체크 (중복 감지 포함)
    kor_files = [f for f in files if "_04_" in f.name and "전문(한글)" in f.name]
    if kor_files:
        best_file, duplicates, issue = find_best_file(kor_files, "korean")
        result["korean"]["exists"] = True
        result["korean"]["path"] = str(best_file)
        result["duplicates"].extend([str(d) for d in duplicates])
        if duplicates:
            result["needs_work"].append("korean_duplicates")
        if issue:
            result["korean"]["quality"] = "incomplete"
            result["korean"]["issue"] = issue
            result["needs_work"].append("korean_incomplete")
        else:
            result["korean"]["quality"] = "ok"
    else:
        result["needs_work"].append("korean_missing")

    return result


def do_organize_01_down(dry_run=False):
    """
    01_down 폴더의 PDF를 02_paper로 이동합니다.
    Returns: (processed_count, pdf_list)
    """
    if not DOWN_DIR.exists():
        return 0, []

    pdf_files = list(DOWN_DIR.glob("*.pdf"))
    if not pdf_files:
        return 0, []

    print(f"## Phase 0: 01_down 정리\n", flush=True)
    print(f"01_down에서 {len(pdf_files)}개 PDF 발견\n", flush=True)

    if dry_run:
        print("**[Dry Run]** 실제 이동하지 않음\n", flush=True)
        for pdf in pdf_files:
            print(f"- `{pdf.name}`", flush=True)
        print("", flush=True)
        return len(pdf_files), pdf_files

    # organize_01_down 모듈 import 및 실행
    try:
        from v.script import organize_01_down
        organize_01_down.main()
        print(f"\n01_down 정리 완료: {len(pdf_files)}개 PDF 처리\n", flush=True)
        return len(pdf_files), pdf_files
    except Exception as e:
        print(f"01_down 정리 중 오류: {e}\n", flush=True)
        return 0, []


def do_run(args):
    """
    전체 논문 자동 정리 - 미완료 논문 목록을 생성하고 작업 계획을 출력합니다.
    """
    sys.stdout.reconfigure(encoding='utf-8')
    print("# oaispaper run - 전체 자동 정리\n", flush=True)
    print(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", flush=True)

    # Phase 0: 01_down 처리 (--skip-organize 옵션으로 건너뛰기 가능)
    if not getattr(args, 'skip_organize', False):
        organized_count, _ = do_organize_01_down(args.dry_run)
        if organized_count > 0:
            print(f"---\n", flush=True)

    if not PAPER_DIR.exists():
        print(f"Error: Paper directory not found at {PAPER_DIR}", flush=True)
        return

    # 모든 폴더 스캔
    target_folders = sorted([d for d in PAPER_DIR.iterdir() if d.is_dir()])
    total = len(target_folders)

    print(f"## Phase 1: 스캔\n", flush=True)
    print(f"총 {total}개 논문 폴더 검사 중...\n", flush=True)

    # 각 폴더 검사
    all_results = []
    needs_summary = []
    needs_english = []
    needs_korean = []
    has_duplicates = []  # 중복 파일이 있는 폴더
    all_duplicates = []  # 모든 중복 파일 경로
    perfect = []

    for folder in target_folders:
        result = check_paper_completeness(folder)
        all_results.append(result)

        # 중복 파일 수집
        if result["duplicates"]:
            has_duplicates.append(result["folder"])
            all_duplicates.extend(result["duplicates"])

        # Perfect 판정: 중복 파일도 없어야 함
        work_without_duplicates = [w for w in result["needs_work"] if "duplicates" not in w]
        if not work_without_duplicates and not result["duplicates"]:
            perfect.append(result["folder"])
        else:
            if "summary_missing" in result["needs_work"] or "summary_incomplete" in result["needs_work"]:
                needs_summary.append(result["folder"])
            if "english_missing" in result["needs_work"] or "english_incomplete" in result["needs_work"]:
                needs_english.append(result["folder"])
            if "korean_missing" in result["needs_work"] or "korean_incomplete" in result["needs_work"]:
                needs_korean.append(result["folder"])

    # 통계 출력
    print("### 스캔 결과\n", flush=True)
    print(f"| 항목 | 건수 | 비율 |", flush=True)
    print(f"|------|:----:|:----:|", flush=True)
    print(f"| 전체 논문 | {total} | 100% |", flush=True)
    print(f"| 완료 (Perfect) | {len(perfect)} | {len(perfect)*100//total}% |", flush=True)
    print(f"| 서머리 필요 | {len(needs_summary)} | {len(needs_summary)*100//total}% |", flush=True)
    print(f"| 영문 추출 필요 | {len(needs_english)} | {len(needs_english)*100//total}% |", flush=True)
    print(f"| 한글 번역 필요 | {len(needs_korean)} | {len(needs_korean)*100//total}% |", flush=True)
    print(f"| **중복 파일 폴더** | {len(has_duplicates)} | {len(has_duplicates)*100//total}% |", flush=True)
    print(f"| **중복 파일 수** | {len(all_duplicates)} | - |", flush=True)
    print("", flush=True)

    # 중복 파일 정리
    if all_duplicates:
        print("### 중복 파일 목록\n", flush=True)
        for dup in all_duplicates[:20]:  # 최대 20개만 표시
            print(f"- `{Path(dup).name}`", flush=True)
        if len(all_duplicates) > 20:
            print(f"- ... 외 {len(all_duplicates) - 20}개", flush=True)
        print("", flush=True)

        if not args.dry_run:
            print("### 중복 파일 자동 삭제\n", flush=True)
            deleted_count = 0
            for dup_path in all_duplicates:
                try:
                    Path(dup_path).unlink()
                    deleted_count += 1
                    print(f"- 삭제: `{Path(dup_path).name}`", flush=True)
                except Exception as e:
                    print(f"- 실패: `{Path(dup_path).name}` ({e})", flush=True)
            print(f"\n총 {deleted_count}개 중복 파일 삭제 완료\n", flush=True)
        else:
            print("**[Dry Run]** 중복 파일은 `--dry-run` 제외 시 자동 삭제됩니다.\n", flush=True)

    # limit 적용
    limit = args.limit if args.limit else len(needs_summary) + len(needs_english) + len(needs_korean)

    if args.dry_run:
        print("### [Dry Run] 실행 계획만 출력\n", flush=True)

    # 작업 목록 출력
    print("## Phase 2-4: 작업 목록\n", flush=True)

    task_count = 0
    tasks = []

    # 서머리 작업
    if needs_summary:
        print("### 서머리 작성 필요\n", flush=True)
        for folder_id in needs_summary[:limit]:
            if task_count >= limit:
                break
            result = next(r for r in all_results if r["folder"] == folder_id)
            pdf_path = result["pdf"]["path"] if result["pdf"]["exists"] else "N/A"
            issue = result["summary"].get("issue", "파일 없음")
            print(f"- [ ] `{folder_id}`: {issue}", flush=True)
            tasks.append({"folder": folder_id, "type": "summary", "pdf": pdf_path})
            task_count += 1
        print("", flush=True)

    # 영문 추출 작업
    if needs_english and task_count < limit:
        print("### 영문 추출 필요\n", flush=True)
        for folder_id in needs_english[:limit - task_count]:
            if task_count >= limit:
                break
            result = next(r for r in all_results if r["folder"] == folder_id)
            pdf_path = result["pdf"]["path"] if result["pdf"]["exists"] else "N/A"
            issue = result["english"].get("issue", "파일 없음")
            print(f"- [ ] `{folder_id}`: {issue}", flush=True)
            tasks.append({"folder": folder_id, "type": "english", "pdf": pdf_path})
            task_count += 1
        print("", flush=True)

    # 한글 번역 작업
    if needs_korean and task_count < limit:
        print("### 한글 번역 필요\n", flush=True)
        for folder_id in needs_korean[:limit - task_count]:
            if task_count >= limit:
                break
            result = next(r for r in all_results if r["folder"] == folder_id)
            eng_path = result["english"]["path"] if result["english"]["exists"] else "N/A"
            issue = result["korean"].get("issue", "파일 없음")
            print(f"- [ ] `{folder_id}`: {issue}", flush=True)
            tasks.append({"folder": folder_id, "type": "korean", "english": eng_path})
            task_count += 1
        print("", flush=True)

    # JSON 작업 목록 저장
    output_file = PROJECT_ROOT / "tmp" / "oaispaper_tasks.json"
    output_file.parent.mkdir(exist_ok=True)
    output_file.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f"## 요약\n", flush=True)
    print(f"- 처리 대상: {task_count}건", flush=True)
    print(f"- 작업 목록: `tmp/oaispaper_tasks.json`", flush=True)
    print("", flush=True)

    if not args.dry_run and task_count > 0:
        print("## 실행 안내\n", flush=True)
        print("위 작업 목록을 서브에이전트로 처리합니다.", flush=True)
        print("각 논문에 대해 PDF를 읽고 서머리/영문추출/한글번역을 수행합니다.", flush=True)
        print("", flush=True)
        print("**다음 단계**: Claude가 위 목록의 각 항목을 순차적으로 처리합니다.", flush=True)

def check_folder(folder_path):
    """
    개별 논문 폴더를 검사하고 발견된 오류 리스트를 반환합니다.
    """
    errors = []
    if not folder_path.is_dir():
        return []
    files = list(folder_path.iterdir())

    # 필수 파일 존재 및 품질 검사
    summary_files = [f for f in files if "_00_" in f.name and "서머리" in f.name]
    if not summary_files: errors.append("00_서머리 파일 누락")

    pdf_files = [f for f in files if f.suffix.lower() == '.pdf']
    if not pdf_files: errors.append("01_PDF 파일 누락")

    eng_files = [f for f in files if "_03_" in f.name and "전문(영어)" in f.name]
    if not eng_files: errors.append("03_전문(영어) 파일 누락")
    else:
        quality_msg = check_file_quality(eng_files[0], 'eng')
        if quality_msg: errors.append(f"03_전문(영어) 품질 미달: {quality_msg}")

    kor_files = [f for f in files if "_04_" in f.name and "전문(한글)" in f.name]
    if not kor_files: errors.append("04_전문(한글) 파일 누락")
    else:
        quality_msg = check_file_quality(kor_files[0], 'kor')
        if quality_msg: errors.append(f"04_전문(한글) 품질 미달: {quality_msg}")

    return errors

def do_status(args):
    """
    전체 논문 폴더의 상태 통계를 출력합니다.
    """
    sys.stdout.reconfigure(encoding='utf-8')
    print("Running oaispaper status...", flush=True)

    # 01_down 상태 확인
    down_pdfs = list(DOWN_DIR.glob("*.pdf")) if DOWN_DIR.exists() else []
    if down_pdfs:
        print(f"\n## 01_down 대기 중: {len(down_pdfs)}개 PDF", flush=True)
        for pdf in down_pdfs[:5]:
            print(f"  - {pdf.name}", flush=True)
        if len(down_pdfs) > 5:
            print(f"  - ... 외 {len(down_pdfs) - 5}개", flush=True)
        print("", flush=True)

    if not PAPER_DIR.exists():
        print(f"Error: Paper directory not found at {PAPER_DIR}", flush=True)
        return

    target_folders = [d for d in PAPER_DIR.iterdir() if d.is_dir()]
    total = len(target_folders)

    stats = {
        "pdf": 0,
        "summary": 0,
        "eng": 0,
        "kor": 0,
        "perfect": 0
    }

    print(f"Analyzing {total} papers...\n", flush=True)

    for folder in target_folders:
        files = list(folder.iterdir())
        has_pdf = any(f.suffix.lower() == '.pdf' for f in files)
        has_sum = any("_00_" in f.name for f in files)
        has_eng = any("_03_" in f.name for f in files)
        has_kor = any("_04_" in f.name for f in files)

        if has_pdf: stats["pdf"] += 1
        if has_sum: stats["summary"] += 1
        if has_eng: stats["eng"] += 1
        if has_kor: stats["kor"] += 1

        if has_pdf and has_sum and has_eng and has_kor:
            stats["perfect"] += 1

    # 리포트 생성
    lines = []
    lines.append("## OAIS Paper Status Report")
    lines.append(f"- Total Papers : {total}")
    lines.append("-" * 30)
    lines.append(f"- PDF Files    : {stats['pdf']:<4} ({stats['pdf']/total*100:5.1f}%)")
    lines.append(f"- Summaries    : {stats['summary']:<4} ({stats['summary']/total*100:5.1f}%)")
    lines.append(f"- English Full : {stats['eng']:<4} ({stats['eng']/total*100:5.1f}%)")
    lines.append(f"- Korean Trans : {stats['kor']:<4} ({stats['kor']/total*100:5.1f}%)")
    lines.append("-" * 30)
    lines.append(f"- Perfect Sets : {stats['perfect']:<4} ({stats['perfect']/total*100:5.1f}%)")

    # 서브명령어 안내 추가
    lines.append("")
    lines.append("## Available Commands")
    lines.append("  run              : 01_down 정리 + 서머리/영문추출/한글번역")
    lines.append("  run --skip-organize : 01_down 건너뛰고 02_paper만 처리")
    lines.append("  status           : 통계 표시")
    lines.append("  fix              : 무결성 체크")
    lines.append("  delete-broken    : 깨진 파일 삭제")
    lines.append("  clean-duplicates : 중복 파일 검사 및 정리")

    report = "\n".join(lines)
    print(report, flush=True)

    (PROJECT_ROOT / "status_report.txt").write_text(report, encoding='utf-8')
    print(f"\nReport saved to status_report.txt", flush=True)

def do_fix(args):
    sys.stdout.reconfigure(encoding='utf-8')
    print(f"Running oaispaper fix...", flush=True)

    if args.folder:
        target_folders = [PAPER_DIR / args.folder]
    else:
        target_folders = [d for d in PAPER_DIR.iterdir() if d.is_dir()]

    error_data = {}
    total_folders = len(target_folders)

    for folder in sorted(target_folders):
        errors = check_folder(folder)
        if errors:
            error_data[folder.name] = errors

    # 결과 리포트
    report_lines = []
    report_lines.append(f"Check Result: {len(error_data)} errors found in {total_folders} folders.")
    for name, errs in error_data.items():
        for err in errs:
            report_lines.append(f"{name}: {err}")

    report_text = "\n".join(report_lines)
    print(report_text, flush=True)
    (PROJECT_ROOT / "fix_report.txt").write_text(report_text, encoding='utf-8')

def do_delete_broken(args):
    sys.stdout.reconfigure(encoding='utf-8')
    print("Running delete-broken...", flush=True)
    target_folders = [d for d in PAPER_DIR.iterdir() if d.is_dir()]

    deleted_files = []
    for folder in target_folders:
        kor_files = [f for f in folder.iterdir() if "_04_" in f.name and "전문(한글)" in f.name]
        for kf in kor_files:
            is_broken = False
            try:
                content = kf.read_text(encoding='utf-8')
                if "\ufffd" in content and content.count("\ufffd") > 10:
                    is_broken = True
            except UnicodeDecodeError:
                is_broken = True

            if is_broken:
                if not args.dry_run:
                    kf.unlink()
                    deleted_files.append(kf.name)
                else:
                    deleted_files.append(f"{kf.name} (DryRun)")

    log_text = f"Deleted {len(deleted_files)} files.\n" + "\n".join(deleted_files)
    print(log_text, flush=True)
    (PROJECT_ROOT / "broken_files_log.txt").write_text(log_text, encoding='utf-8')


def do_clean_duplicates(args):
    """
    중복 파일만 검사하고 정리합니다.
    """
    sys.stdout.reconfigure(encoding='utf-8')
    print("# oaispaper clean-duplicates - 중복 파일 정리\n", flush=True)
    print(f"실행 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", flush=True)

    if not PAPER_DIR.exists():
        print(f"Error: Paper directory not found at {PAPER_DIR}", flush=True)
        return

    target_folders = sorted([d for d in PAPER_DIR.iterdir() if d.is_dir()])
    total = len(target_folders)

    print(f"총 {total}개 논문 폴더 검사 중...\n", flush=True)

    all_duplicates = []
    folders_with_dups = []

    for folder in target_folders:
        result = check_paper_completeness(folder)
        if result["duplicates"]:
            folders_with_dups.append(result["folder"])
            for dup in result["duplicates"]:
                all_duplicates.append({
                    "folder": result["folder"],
                    "file": dup,
                    "name": Path(dup).name
                })

    # 결과 출력
    print("## 검사 결과\n", flush=True)
    print(f"- 전체 폴더: {total}개", flush=True)
    print(f"- 중복 파일이 있는 폴더: {len(folders_with_dups)}개", flush=True)
    print(f"- 총 중복 파일 수: {len(all_duplicates)}개\n", flush=True)

    if not all_duplicates:
        print("중복 파일이 없습니다.\n", flush=True)
        return

    print("## 중복 파일 목록\n", flush=True)
    print("| 폴더 | 삭제 대상 파일 |", flush=True)
    print("|------|---------------|", flush=True)
    for dup in all_duplicates:
        print(f"| `{dup['folder']}` | `{dup['name']}` |", flush=True)
    print("", flush=True)

    if args.dry_run:
        print("**[Dry Run]** 실제 삭제하려면 `--dry-run` 옵션을 제거하세요.\n", flush=True)
    else:
        print("## 삭제 실행\n", flush=True)
        deleted = 0
        failed = 0
        for dup in all_duplicates:
            try:
                Path(dup["file"]).unlink()
                print(f"- 삭제 완료: `{dup['name']}`", flush=True)
                deleted += 1
            except Exception as e:
                print(f"- 삭제 실패: `{dup['name']}` ({e})", flush=True)
                failed += 1

        print(f"\n### 결과: {deleted}개 삭제, {failed}개 실패\n", flush=True)

    # 로그 저장
    log_file = PROJECT_ROOT / "tmp" / "duplicates_log.txt"
    log_file.parent.mkdir(exist_ok=True)
    log_content = f"중복 파일 정리 로그 - {datetime.now()}\n"
    log_content += f"총 {len(all_duplicates)}개 중복 파일\n\n"
    for dup in all_duplicates:
        log_content += f"{dup['folder']}: {dup['name']}\n"
    log_file.write_text(log_content, encoding='utf-8')
    print(f"로그 저장: `tmp/duplicates_log.txt`", flush=True)



def do_ref_update(args):
    """
    서머리 파일에 참고문헌을 추가합니다.
    """
    import re
    sys.stdout.reconfigure(encoding='utf-8')
    print("Running oaispaper ref-update...", flush=True)

    if args.folder:
        target_folders = [d for d in PAPER_DIR.iterdir() if d.is_dir() and d.name == args.folder]
    else:
        target_folders = [d for d in PAPER_DIR.iterdir() if d.is_dir()]

    print(f"Processing {len(target_folders)} folders...", flush=True)

    updated = 0
    skipped = 0
    failed = 0

    for folder in target_folders:
        summary_files = list(folder.glob("*_00_*서머리.md"))
        eng_files = list(folder.glob("*_03_*전문(영어).md"))

        if not summary_files:
            failed += 1
            print(f"- [FAILED] {folder.name}: No summary", flush=True)
            continue

        summary_file = summary_files[0]

        if not eng_files:
            failed += 1
            print(f"- [FAILED] {folder.name}: No English full text", flush=True)
            continue

        eng_file = eng_files[0]

        # Check if already exists
        try:
            summary_content = summary_file.read_text(encoding='utf-8')
        except:
            failed += 1
            print(f"- [FAILED] {folder.name}: Read error", flush=True)
            continue

        if re.search(r'^##\s*(References?|참고\s*문헌|참고문헌)', summary_content, re.MULTILINE | re.IGNORECASE):
            # Check content length
            match = re.search(r'^##\s*(References?|참고\s*문헌|참고문헌)', summary_content, re.MULTILINE | re.IGNORECASE)
            start = match.end()
            end_match = re.search(r'^##\s+', summary_content[start:], re.MULTILINE)
            content = summary_content[start:start+end_match.start()] if end_match else summary_content[start:]
            if len(content.strip()) > 50:
                skipped += 1
                # print(f"- [SKIPPED] {folder.name}: Already exists", flush=True)
                continue

        # Extract refs
        try:
            eng_content = eng_file.read_text(encoding='utf-8', errors='ignore')
        except:
            failed += 1
            continue

        match = re.search(r'^##\s*(References?|Bibliography|참고\s*문헌|참고문헌)', eng_content, re.MULTILINE | re.IGNORECASE)
        refs = None
        if match:
            start_pos = match.end()
            refs = eng_content[start_pos:].strip()
        else:
            match_uc = re.search(r'\nREFERENCES\s*\n', eng_content)
            if match_uc:
                refs = eng_content[match_uc.end():].strip()

        if not refs or len(refs) < 50:
            failed += 1
            print(f"- [FAILED] {folder.name}: Extraction failed", flush=True)
            continue

        # Update summary
        keyword_match = re.search(r'^##\s*키워드', summary_content, re.MULTILINE)
        new_section = f"\n\n## 참고문헌\n{refs}\n"

        if keyword_match:
            insert_pos = keyword_match.start()
            new_content = summary_content[:insert_pos] + new_section + "\n" + summary_content[insert_pos:]
        else:
            new_content = summary_content + new_section

        if not args.dry_run:
            summary_file.write_text(new_content, encoding='utf-8')
            updated += 1
            print(f"- [UPDATED] {folder.name}", flush=True)
        else:
            updated += 1
            print(f"- [UPDATED] {folder.name} (Dry Run)", flush=True)

    print("-" * 30, flush=True)
    print(f"Total: {len(target_folders)}", flush=True)
    print(f"Updated: {updated}", flush=True)
    print(f"Skipped: {skipped}", flush=True)
    print(f"Failed: {failed}", flush=True)

def main():
    # 서브명령어 없이 실행 시 도움말 출력
    if show_help_if_no_args("oaispaper", sys.argv[1:]):
        return

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)

    # run 명령어 (전체 자동 정리)
    run_p = subparsers.add_parser('run', help="전체 자동 정리: 01_down 정리 + 서머리/영문추출/한글번역")
    run_p.add_argument('--limit', type=int, help="처리할 최대 논문 수")
    run_p.add_argument('--dry-run', action='store_true', help="실행 없이 계획만 출력")
    run_p.add_argument('--folder', type=str, help="특정 폴더만 처리")
    run_p.add_argument('--phase', type=str, choices=['summary', 'english', 'korean'], help="특정 단계만 실행")
    run_p.add_argument('--skip-organize', action='store_true', help="01_down 정리 단계 건너뛰기")

    subparsers.add_parser('status', help="Show statistics")

    fix_p = subparsers.add_parser('fix', help="Check integrity")
    fix_p.add_argument('--check-only', action='store_true')
    fix_p.add_argument('--folder', type=str)
    fix_p.add_argument('--auto-fix', action='store_true')

    del_p = subparsers.add_parser('delete-broken', help="Delete broken files")
    del_p.add_argument('--dry-run', action='store_true')

    # clean-duplicates 명령어 (중복 파일 정리)
    dup_p = subparsers.add_parser('clean-duplicates', help="중복 파일 검사 및 정리")
    dup_p.add_argument('--dry-run', action='store_true', help="실행 없이 목록만 출력")

    # ref-update 명령어 check
    ref_p = subparsers.add_parser('ref-update', help="서머리 파일에 참고문헌 추가")
    ref_p.add_argument('--folder', type=str)
    ref_p.add_argument('--dry-run', action='store_true')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.command == 'run':
        do_run(args)
    elif args.command == 'status':
        do_status(args)
    elif args.command == 'fix':
        do_fix(args)
    elif args.command == 'delete-broken':
        do_delete_broken(args)
    elif args.command == 'clean-duplicates':
        do_clean_duplicates(args)
    elif args.command == 'ref-update':
        do_ref_update(args)
    else:
        print("Not implemented")

if __name__ == "__main__":
    main()
