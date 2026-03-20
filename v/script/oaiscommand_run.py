#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""oaiscommand_run.py - oais 명령어 집계 및 문서화 (상세: doc/a0009_script.md)"""

import sys
import re
import json
from datetime import datetime
from oais_common import (
    show_help_if_no_args, PROJECT_ROOT, DOC_DIR, V_DIR,
    log_ok, log_warn, log_info, log_tip, log_dry_run
)

V_COMMAND_DIR = V_DIR / "command"
CLAUDE_DIR = PROJECT_ROOT / ".claude"
COMMANDS_DIR = CLAUDE_DIR / "commands"
SC_DIR = COMMANDS_DIR / "sc"  # SuperClaude 외부 소스
MCP_CONFIG = PROJECT_ROOT / ".mcp.json"
OUTPUT_FILE = DOC_DIR / "d0007_command.md"

# ============================================================
# Built-in Claude Code Commands (하드코딩)
# ============================================================
BUILTIN_COMMANDS = [
    {"command": "/help", "description": "도움말 표시", "source": "built-in"},
    {"command": "/clear", "description": "대화 기록 초기화", "source": "built-in"},
    {"command": "/compact", "description": "대화 컴팩트 모드", "source": "built-in"},
    {"command": "/config", "description": "설정 관리", "source": "built-in"},
    {"command": "/cost", "description": "토큰 사용량/비용 확인", "source": "built-in"},
    {"command": "/doctor", "description": "환경 진단", "source": "built-in"},
    {"command": "/init", "description": "프로젝트 초기화", "source": "built-in"},
    {"command": "/login", "description": "로그인", "source": "built-in"},
    {"command": "/logout", "description": "로그아웃", "source": "built-in"},
    {"command": "/mcp", "description": "MCP 서버 관리", "source": "built-in"},
    {"command": "/memory", "description": "메모리/컨텍스트 관리", "source": "built-in"},
    {"command": "/model", "description": "모델 선택", "source": "built-in"},
    {"command": "/permissions", "description": "권한 설정", "source": "built-in"},
    {"command": "/pr-comments", "description": "PR 코멘트 확인", "source": "built-in"},
    {"command": "/review", "description": "코드 리뷰", "source": "built-in"},
    {"command": "/status", "description": "상태 확인", "source": "built-in"},
    {"command": "/terminal-setup", "description": "터미널 설정", "source": "built-in"},
    {"command": "/vim", "description": "Vim 모드 토글", "source": "built-in"},
]

# ============================================================
# Plugin Skills (시스템에서 확인된 플러그인)
# ============================================================
PLUGIN_SKILLS = [
    # code-review plugin
    {"command": "code-review:code-review", "description": "Code review a pull request", "source": "plugin:code-review"},
    # commit-commands plugin
    {"command": "commit-commands:clean_gone", "description": "Cleans up git branches marked as [gone]", "source": "plugin:commit-commands"},
    {"command": "commit-commands:commit-push-pr", "description": "Commit, push, and open a PR", "source": "plugin:commit-commands"},
    {"command": "commit-commands:commit", "description": "Create a git commit", "source": "plugin:commit-commands"},
    # feature-dev plugin
    {"command": "feature-dev:feature-dev", "description": "Guided feature development with codebase understanding", "source": "plugin:feature-dev"},
    # document-skills plugin
    {"command": "document-skills:algorithmic-art", "description": "Creating algorithmic art using p5.js", "source": "plugin:document-skills"},
    {"command": "document-skills:brand-guidelines", "description": "Applies brand colors and typography", "source": "plugin:document-skills"},
    {"command": "document-skills:canvas-design", "description": "Create visual art in .png and .pdf", "source": "plugin:document-skills"},
    {"command": "document-skills:doc-coauthoring", "description": "Guide for co-authoring documentation", "source": "plugin:document-skills"},
    {"command": "document-skills:docx", "description": "Document creation, editing, and analysis (.docx)", "source": "plugin:document-skills"},
    {"command": "document-skills:frontend-design", "description": "Create production-grade frontend interfaces", "source": "plugin:document-skills"},
    {"command": "document-skills:internal-comms", "description": "Write internal communications", "source": "plugin:document-skills"},
    {"command": "document-skills:mcp-builder", "description": "Guide for creating MCP servers", "source": "plugin:document-skills"},
    {"command": "document-skills:pdf", "description": "PDF manipulation toolkit", "source": "plugin:document-skills"},
    {"command": "document-skills:pptx", "description": "Presentation creation and editing (.pptx)", "source": "plugin:document-skills"},
    {"command": "document-skills:skill-creator", "description": "Guide for creating effective skills", "source": "plugin:document-skills"},
    {"command": "document-skills:slack-gif-creator", "description": "Create animated GIFs for Slack", "source": "plugin:document-skills"},
    {"command": "document-skills:theme-factory", "description": "Toolkit for styling artifacts with a theme", "source": "plugin:document-skills"},
    {"command": "document-skills:web-artifacts-builder", "description": "Tools for creating web artifacts", "source": "plugin:document-skills"},
    {"command": "document-skills:webapp-testing", "description": "Toolkit for testing web apps with Playwright", "source": "plugin:document-skills"},
    {"command": "document-skills:xlsx", "description": "Spreadsheet creation and analysis (.xlsx)", "source": "plugin:document-skills"},
    # frontend-design plugin
    {"command": "frontend-design:frontend-design", "description": "Create distinctive frontend interfaces", "source": "plugin:frontend-design"},
    # superpowers plugin
    {"command": "superpowers:brainstorming", "description": "Use before any creative work", "source": "plugin:superpowers"},
    {"command": "superpowers:dispatching-parallel-agents", "description": "Use for 2+ independent tasks", "source": "plugin:superpowers"},
    {"command": "superpowers:executing-plans", "description": "Execute written implementation plan", "source": "plugin:superpowers"},
    {"command": "superpowers:finishing-a-development-branch", "description": "Guide completion of development work", "source": "plugin:superpowers"},
]


def extract_commands_from_md(file_path):
    """Markdown 파일에서 명령어 테이블 추출"""
    content = file_path.read_text(encoding="utf-8")
    commands = []

    lines = content.splitlines()
    in_command_section = False
    base_command = file_path.stem

    for line in lines:
        if re.search(r"^##\s+(\d+\.\s*)?(명령어\s*$|서브명령어\s*$|명령어 목록)", line):
            in_command_section = True
            continue
        if re.search(r"^##\s+", line) and in_command_section:
            in_command_section = False
            continue

        if in_command_section and line.strip().startswith("|") and "`" in line:
            parts = [p.strip() for p in line.strip().split("|")]
            if len(parts) >= 3:
                cmd_str = parts[1].replace("`", "").strip()
                desc_str = parts[2].strip()

                if "---" in cmd_str:
                    continue
                if "명령어" in cmd_str or "서브명령어" in cmd_str:
                    continue

                # 스킬명 접두사 정규화: "run" → "oaistest run"
                if not cmd_str.startswith(base_command):
                    cmd_str = f"{base_command} {cmd_str}"

                commands.append({
                    "command": cmd_str,
                    "description": desc_str,
                    "source": file_path.name
                })

    return commands


def extract_project_skills():
    """프로젝트 스킬 스캔 (.claude/commands/)"""
    skills = []

    if not COMMANDS_DIR.exists():
        return skills

    # 직접 .md 파일들
    for md_file in COMMANDS_DIR.glob("*.md"):
        name = md_file.stem
        # 첫 줄에서 설명 추출 시도
        try:
            content = md_file.read_text(encoding="utf-8")
            first_line = content.strip().split("\n")[0]
            desc = first_line.lstrip("#").strip()[:60]
            if not desc or desc.startswith("---"):
                desc = f"{name} 스킬"
        except:
            desc = f"{name} 스킬"

        skills.append({
            "command": name,
            "description": desc,
            "source": f".claude/commands/{md_file.name}"
        })

    # 서브디렉토리 (sc/, daemosan/ 등)
    for subdir in COMMANDS_DIR.iterdir():
        if subdir.is_dir():
            prefix = subdir.name
            for md_file in subdir.glob("*.md"):
                name = md_file.stem
                try:
                    content = md_file.read_text(encoding="utf-8")
                    first_line = content.strip().split("\n")[0]
                    desc = first_line.lstrip("#").strip()[:60]
                    if not desc or desc.startswith("---"):
                        desc = f"{prefix}:{name} 스킬"
                except:
                    desc = f"{prefix}:{name} 스킬"

                skills.append({
                    "command": f"{prefix}:{name}",
                    "description": desc,
                    "source": f".claude/commands/{prefix}/{md_file.name}"
                })

    return skills


def extract_mcp_servers():
    """MCP 서버 파싱 (.mcp.json)"""
    servers = []

    if not MCP_CONFIG.exists():
        return servers

    try:
        content = MCP_CONFIG.read_text(encoding="utf-8")
        config = json.loads(content)

        mcp_servers = config.get("mcpServers", {})
        for name, info in mcp_servers.items():
            cmd = info.get("command", "")
            args = info.get("args", [])
            package = args[-1] if args else cmd

            servers.append({
                "command": f"mcp:{name}",
                "description": f"MCP Server: {package}",
                "source": ".mcp.json"
            })
    except Exception as e:
        print(f"  Warning: Failed to parse .mcp.json: {e}")

    return servers


def generate_command_doc(oais_commands, builtin_commands, project_skills, plugin_skills, mcp_servers):
    """d0007_command.md 내용 생성"""
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 통계
    total_oais = len(oais_commands)
    total_builtin = len(builtin_commands)
    total_project = len(project_skills)
    total_plugin = len(plugin_skills)
    total_mcp = len(mcp_servers)
    total_all = total_oais + total_builtin + total_project + total_plugin + total_mcp

    # OAIS 그룹화
    oais_grouped = {}
    for cmd in oais_commands:
        skill = cmd['source'].replace(".md", "")
        if skill not in oais_grouped:
            oais_grouped[skill] = []
        oais_grouped[skill].append(cmd)

    # OAIS 요약 테이블
    oais_summary_rows = []
    for skill in sorted(oais_grouped.keys()):
        cmds = [c['command'] for c in oais_grouped[skill]]
        base_cmd = min(cmds, key=len) if cmds else skill
        desc = "기능 모음"
        for c in oais_grouped[skill]:
            if c['command'] == skill or c['command'] == f"{skill} run":
                desc = c['description']
                break
        oais_summary_rows.append(f"| {skill} | `{base_cmd}` | {desc} |")
    oais_summary_table = "\n".join(oais_summary_rows)

    # OAIS 상세 섹션
    oais_details = []
    for skill in sorted(oais_grouped.keys()):
        rows = []
        for cmd in oais_grouped[skill]:
            rows.append(f"| `{cmd['command']}` | {cmd['description']} |")
        table = f"""
#### {skill}

| 명령어 | 설명 |
|--------|------|
{chr(10).join(rows)}
"""
        oais_details.append(table)

    # Built-in 테이블
    builtin_rows = [f"| `{c['command']}` | {c['description']} |" for c in builtin_commands]
    builtin_table = "\n".join(builtin_rows)

    # Project Skills 테이블
    project_rows = [f"| `{c['command']}` | {c['description']} | {c['source']} |" for c in project_skills]
    project_table = "\n".join(project_rows)

    # Plugin Skills 그룹화
    plugin_grouped = {}
    for cmd in plugin_skills:
        plugin = cmd['source'].replace("plugin:", "")
        if plugin not in plugin_grouped:
            plugin_grouped[plugin] = []
        plugin_grouped[plugin].append(cmd)

    plugin_details = []
    for plugin in sorted(plugin_grouped.keys()):
        rows = [f"| `{c['command']}` | {c['description']} |" for c in plugin_grouped[plugin]]
        table = f"""
#### {plugin}

| 스킬 | 설명 |
|------|------|
{chr(10).join(rows)}
"""
        plugin_details.append(table)

    # MCP 테이블
    mcp_rows = [f"| `{c['command']}` | {c['description']} |" for c in mcp_servers]
    mcp_table = "\n".join(mcp_rows)

    content = f"""# d0007_command.md - 명령어/스킬 통합 집계

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v2.0 | {today} | Claude Code 통합 집계 추가 (oaiscommand run) |
| v1.0 | 2024-12-31 | 자동 생성됨 |

---

## 1. 개요

이 문서는 프로젝트에서 사용 가능한 모든 명령어, 스킬, 플러그인을 집계합니다.

**자동 갱신**: `oaiscommand run` 실행 시 자동 갱신
**마지막 갱신**: {now}

### 1.1 통계 요약

| 카테고리 | 개수 |
|----------|------|
| OAIS 스킬 명령어 | {total_oais} |
| Claude Built-in 명령어 | {total_builtin} |
| Project Skills | {total_project} |
| Plugin Skills | {total_plugin} |
| MCP Servers | {total_mcp} |
| **총계** | **{total_all}** |

### 1.2 명령어 표기법

모든 OAIS 스킬 명령어는 **스킬명 접두사**를 포함합니다.

| 형식 | 예시 | 설명 |
|------|------|------|
| `스킬명 서브명령` | `oaistest run` | 기본 형식 |
| `스킬명 서브명령 [인자]` | `oaissync view [project]` | 인자 포함 |
| `스킬명 서브명령 --옵션` | `oaistest run --unit` | 옵션 포함 |

> 상세: `v/oaiscommand.md` 참조

---

## 2. Claude Code Built-in 명령어

기본 제공되는 슬래시 명령어입니다.

| 명령어 | 설명 |
|--------|------|
{builtin_table}

---

## 3. OAIS 스킬 명령어

`v/oais*.md`에서 정의된 프로젝트 전용 스킬입니다.

### 3.1 요약

| 스킬 | 기본 명령어 | 주요 용도 |
|------|------------|----------|
{oais_summary_table}

### 3.2 상세
{"".join(oais_details)}

---

## 4. Project Skills

`.claude/commands/`에 정의된 프로젝트 스킬입니다.

| 스킬 | 설명 | 위치 |
|------|------|------|
{project_table}

---

## 5. Plugin Skills

Claude Code 플러그인에서 제공하는 스킬입니다.
{"".join(plugin_details)}

---

## 6. MCP Servers

`.mcp.json`에 설정된 MCP 서버입니다.

| 서버 | 설명 |
|------|------|
{mcp_table}

---

## 7. 관련 문서

- `v/oaiscommand.md` - 명령어 집계 스킬 정의
- `.claude/COMMANDS.md` - SuperClaude 명령어 프레임워크
- `.mcp.json` - MCP 서버 설정
"""
    return content


def cmd_update():
    """모든 소스 스캔 및 문서 갱신"""
    print("## Scanning v/oais*.md files...")
    md_files = list(V_DIR.glob("oais*.md"))
    oais_commands = []

    for md_file in md_files:
        if "guide" in md_file.name:
            continue
        print(f"  Parsing {md_file.name}...")
        cmds = extract_commands_from_md(md_file)
        oais_commands.extend(cmds)

    print(f"  -> {len(oais_commands)} OAIS commands found.")

    print("\n## Loading Built-in commands...")
    builtin_commands = BUILTIN_COMMANDS
    print(f"  -> {len(builtin_commands)} Built-in commands.")

    print("\n## Scanning .claude/commands/...")
    project_skills = extract_project_skills()
    print(f"  -> {len(project_skills)} Project skills found.")

    print("\n## Loading Plugin skills...")
    plugin_skills = PLUGIN_SKILLS
    print(f"  -> {len(plugin_skills)} Plugin skills.")

    print("\n## Parsing .mcp.json...")
    mcp_servers = extract_mcp_servers()
    print(f"  -> {len(mcp_servers)} MCP servers found.")

    total = len(oais_commands) + len(builtin_commands) + len(project_skills) + len(plugin_skills) + len(mcp_servers)
    print(f"\n## Total: {total} commands/skills/servers")

    # 문서 생성
    new_content = generate_command_doc(
        oais_commands, builtin_commands, project_skills, plugin_skills, mcp_servers
    )

    # 파일 쓰기
    OUTPUT_FILE.write_text(new_content, encoding="utf-8")
    print(f"\n[OK] Updated {OUTPUT_FILE}")
    return 0


def extract_v_commands():
    """v/command/ 디렉토리에서 명령어 추출"""
    commands = []

    if not V_COMMAND_DIR.exists():
        return commands

    for md_file in sorted(V_COMMAND_DIR.glob("*.md")):
        if md_file.name == "README.md":
            continue

        name = md_file.stem
        content = md_file.read_text(encoding="utf-8")

        # 첫 줄에서 설명 추출
        lines = content.strip().split("\n")
        desc = lines[0].lstrip("#").strip()[:80] if lines else f"{name} 명령어"

        # 파일 크기
        size = md_file.stat().st_size

        commands.append({
            "name": name,
            "description": desc,
            "file": md_file.name,
            "size": size
        })

    return commands


def extract_external_commands():
    """외부 소스(.claude/commands/sc/)에서 명령어 추출"""
    commands = []

    if not SC_DIR.exists():
        return commands

    for md_file in sorted(SC_DIR.glob("*.md")):
        name = md_file.stem
        content = md_file.read_text(encoding="utf-8")

        # 첫 줄에서 설명 추출
        lines = content.strip().split("\n")
        desc = lines[0].lstrip("#").strip()[:80] if lines else f"{name} 명령어"

        # 파일 크기
        size = md_file.stat().st_size

        commands.append({
            "name": name,
            "description": desc,
            "file": md_file.name,
            "size": size
        })

    return commands


def cmd_list():
    """v/command/ 통합 명령어 목록 조회 (list 서브명령어)"""
    print("# oaiscommand list\n")

    v_commands = extract_v_commands()
    sc_commands = extract_external_commands()

    print("## v/command/ 명령어\n")
    if v_commands:
        print("| 명령어 | 설명 |")
        print("|--------|------|")
        for cmd in v_commands:
            print(f"| /{cmd['name']} | {cmd['description'][:50]} |")
    else:
        print("(없음)")

    print()
    print(f"## .claude/commands/sc/ 명령어\n")
    if sc_commands:
        print("| 명령어 | 설명 |")
        print("|--------|------|")
        for cmd in sc_commands:
            print(f"| sc:{cmd['name']} | {cmd['description'][:50]} |")
    else:
        print("(없음)")

    print()
    print("---")
    print(f"v/command: {len(v_commands)}개 | sc: {len(sc_commands)}개")
    return 0


def cmd_compare():
    """외부 소스와 v/command 비교 (compare 서브명령어)"""
    print("# oaiscommand compare\n")

    v_commands = {c['name']: c for c in extract_v_commands()}
    sc_commands = {c['name']: c for c in extract_external_commands()}

    v_names = set(v_commands.keys())
    sc_names = set(sc_commands.keys())

    # 공통 명령어
    common = v_names & sc_names
    # v에만 있는 것
    v_only = v_names - sc_names
    # sc에만 있는 것
    sc_only = sc_names - v_names

    print("## 비교 결과\n")

    print(f"### 공통 명령어 ({len(common)}개)")
    if common:
        print("| 명령어 | v/command | sc/ | 크기 차이 |")
        print("|--------|-----------|-----|----------|")
        for name in sorted(common):
            v_size = v_commands[name]['size']
            sc_size = sc_commands[name]['size']
            diff = v_size - sc_size
            diff_str = f"+{diff}" if diff > 0 else str(diff)
            status = "동일" if diff == 0 else ("v 더 큼" if diff > 0 else "sc 더 큼")
            print(f"| {name} | {v_size}B | {sc_size}B | {diff_str}B ({status}) |")
    else:
        print("(없음)")

    print()
    print(f"### v/command에만 있음 ({len(v_only)}개)")
    for name in sorted(v_only):
        print(f"  - /{name}")

    print()
    print(f"### sc/에만 있음 ({len(sc_only)}개)")
    for name in sorted(sc_only):
        print(f"  - sc:{name}")

    print()
    print("---")
    print(f"공통: {len(common)} | v전용: {len(v_only)} | sc전용: {len(sc_only)}")

    if sc_only:
        print(f"\n[TIP] 새 명령어를 채택하려면: oaiscommand adopt <명령어>")

    return 0


def cmd_sync():
    """외부 소스 변경사항 동기화 (sync 서브명령어)"""
    dry_run = "--dry-run" in sys.argv
    print("# oaiscommand sync\n")
    if dry_run:
        print("[DRY-RUN] 실제 동기화 없이 미리보기만 실행\n")

    v_commands = {c['name']: c for c in extract_v_commands()}
    sc_commands = {c['name']: c for c in extract_external_commands()}

    v_names = set(v_commands.keys())
    sc_names = set(sc_commands.keys())

    # sc에만 있는 명령어 (새로 추가할 것)
    to_add = sc_names - v_names

    # 공통 명령어 중 sc가 더 최신인 것
    common = v_names & sc_names
    to_update = []

    for name in common:
        v_size = v_commands[name]['size']
        sc_size = sc_commands[name]['size']
        # 크기가 다르면 업데이트 대상
        if v_size != sc_size:
            to_update.append(name)

    print("## 동기화 계획\n")

    print(f"### 추가 예정 ({len(to_add)}개)")
    for name in sorted(to_add):
        print(f"  + /{name}")

    print()
    print(f"### 업데이트 예정 ({len(to_update)}개)")
    for name in sorted(to_update):
        print(f"  ~ /{name}")

    if not to_add and not to_update:
        print("[OK] 동기화할 변경사항이 없습니다.")
        return 0

    print()
    print("---")

    # --dry-run이 아니면 실제 동기화 수행
    if dry_run:
        print(f"[DRY-RUN] 미리보기 완료")
        print(f"[TIP] 실제 동기화: oaiscommand sync (--dry-run 제거)")
    else:
        print("## 동기화 실행 중...\n")

        # 추가
        for name in to_add:
            src = SC_DIR / f"{name}.md"
            dst = V_COMMAND_DIR / f"{name}.md"
            content = src.read_text(encoding="utf-8")
            dst.write_text(content, encoding="utf-8")
            print(f"  [+] {name}.md 추가됨")

        # 업데이트
        for name in to_update:
            src = SC_DIR / f"{name}.md"
            dst = V_COMMAND_DIR / f"{name}.md"
            content = src.read_text(encoding="utf-8")
            dst.write_text(content, encoding="utf-8")
            print(f"  [~] {name}.md 업데이트됨")

        print(f"\n[OK] 동기화 완료: {len(to_add)}개 추가, {len(to_update)}개 업데이트")

    return 0


def cmd_adopt(args):
    """특정 외부 명령어를 v/command에 채택 (adopt 서브명령어)"""
    print("# oaiscommand adopt\n")

    if not args:
        print("[ERROR] 채택할 명령어 이름을 지정하세요.")
        print("사용법: oaiscommand adopt <명령어>")
        print()
        # 채택 가능한 명령어 목록
        sc_commands = extract_external_commands()
        v_commands = {c['name'] for c in extract_v_commands()}

        available = [c for c in sc_commands if c['name'] not in v_commands]
        if available:
            print("채택 가능한 명령어:")
            for cmd in available:
                print(f"  - {cmd['name']}")
        return 1

    target = args[0].replace("sc:", "").strip()

    # sc/에 있는지 확인
    src = SC_DIR / f"{target}.md"
    if not src.exists():
        print(f"[ERROR] sc/{target}.md 파일을 찾을 수 없습니다.")
        return 1

    # 이미 v/command에 있는지 확인
    dst = V_COMMAND_DIR / f"{target}.md"
    if dst.exists():
        print(f"[WARN] v/command/{target}.md 가 이미 존재합니다.")
        print("[INFO] 덮어쓰려면 --force 옵션을 사용하세요.")
        if "--force" not in sys.argv:
            return 1

    # 채택
    content = src.read_text(encoding="utf-8")
    dst.write_text(content, encoding="utf-8")

    print(f"[OK] /{target} 명령어를 채택했습니다.")
    print(f"    소스: {src}")
    print(f"    대상: {dst}")
    print(f"    크기: {len(content)} bytes")

    return 0


def print_usage():
    """사용법 출력"""
    print(f"Log started at {datetime.now()}")
    print("oaiscommand - 명령어 집계 및 문서화")
    print()
    print("사용법:")
    print("    oaiscommand run           전체 명령어 집계 및 문서화 (v/command/ 포함)")
    print("    oaiscommand update        d0007_command.md 업데이트")
    print("    oaiscommand list          v/command/ 명령어 목록 조회")
    print("    oaiscommand compare       외부 소스와 비교 (sc/)")
    print("    oaiscommand sync          외부 소스 변경사항 동기화")
    print("    oaiscommand adopt [명령어] 특정 외부 명령어 채택")
    print()
    print("옵션:")
    print("    --dry-run                 sync 시 미리보기만 (실제 실행 안 함)")
    print("    --force                   adopt 시 덮어쓰기")
    print()
    print("예시:")
    print("    python v/script/oaiscommand_run.py run")
    print("    python v/script/oaiscommand_run.py compare")
    print("    python v/script/oaiscommand_run.py adopt implement")


def main():
    # 서브명령어 없이 실행 시 도움말 출력
    if show_help_if_no_args("oaiscommand", sys.argv[1:]):
        return

    print(f"Log started at {datetime.now()}")

    args = sys.argv[1:]

    if not args:
        print_usage()
        return 0

    cmd = args[0].lower()
    cmd_args = args[1:]

    # 옵션 제거
    cmd_args = [a for a in cmd_args if not a.startswith("--")]

    if cmd == "run" or cmd == "update":
        return cmd_update()
    elif cmd == "list":
        return cmd_list()
    elif cmd == "compare":
        return cmd_compare()
    elif cmd == "sync":
        return cmd_sync()
    elif cmd == "adopt":
        return cmd_adopt(cmd_args)
    else:
        print(f"[ERROR] Unknown command: {cmd}")
        print_usage()
        return 1


if __name__ == "__main__":
    sys.exit(main())
