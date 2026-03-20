"""
oaisenv validate --full: 스킬 참조 정합성 검증 스크립트

oais*.md 스킬 파일을 스캔하여 참조된 에이전트/커맨드/MCP를 추출하고
현재 환경과 교차 검증합니다.

검증 대상:
1. 에이전트: v/agent/, .claude/agents/ 존재 확인
2. 커맨드: v/command/, .claude/commands/ 존재 확인
3. MCP: .mcp.json 설정 존재 확인
"""

import re
import sys
import io
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# Windows 콘솔 UTF-8 출력 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


@dataclass
class ValidationResult:
    """검증 결과"""
    skill_file: str
    agents_found: list = field(default_factory=list)
    agents_missing: list = field(default_factory=list)
    commands_found: list = field(default_factory=list)
    commands_missing: list = field(default_factory=list)
    mcps_found: list = field(default_factory=list)
    mcps_missing: list = field(default_factory=list)


@dataclass
class EnvironmentInfo:
    """현재 환경 정보"""
    agents_v: set = field(default_factory=set)       # v/agent/ 에이전트
    agents_claude: set = field(default_factory=set)  # .claude/agents/ 에이전트
    commands_v: set = field(default_factory=set)     # v/command/ 커맨드
    commands_claude: set = field(default_factory=set)  # .claude/commands/ 커맨드
    mcp_servers: set = field(default_factory=set)    # .mcp.json MCP 서버


def load_environment(project_root: Path) -> EnvironmentInfo:
    """현재 환경 정보 로드"""
    env = EnvironmentInfo()

    # v/agent/ 에이전트 로드
    agent_dir = project_root / 'v' / 'agent'
    if agent_dir.exists():
        for f in agent_dir.glob('*.md'):
            env.agents_v.add(f.stem)

    # .claude/agents/ 에이전트 로드
    claude_agents = project_root / '.claude' / 'agents'
    if claude_agents.exists():
        for f in claude_agents.glob('*.md'):
            env.agents_claude.add(f.stem)

    # v/command/ 커맨드 로드
    command_dir = project_root / 'v' / 'command'
    if command_dir.exists():
        for f in command_dir.glob('*.md'):
            if f.stem != 'README':
                env.commands_v.add(f.stem)

    # .claude/commands/ 커맨드 로드
    claude_commands = project_root / '.claude' / 'commands'
    if claude_commands.exists():
        for f in claude_commands.glob('*.md'):
            env.commands_claude.add(f.stem)

    # .mcp.json MCP 서버 로드
    mcp_json = project_root / '.mcp.json'
    if mcp_json.exists():
        try:
            data = json.loads(mcp_json.read_text(encoding='utf-8'))
            if 'mcpServers' in data:
                env.mcp_servers = set(data['mcpServers'].keys())
        except (json.JSONDecodeError, KeyError):
            pass

    return env


def extract_agents(content: str) -> set:
    """스킬 파일에서 참조된 에이전트 추출"""
    agents = set()

    # 패턴 1: Task(subagent_type="xxx" or subagent_type='xxx')
    pattern1 = r'subagent_type\s*=\s*["\']([^"\']+)["\']'
    for match in re.finditer(pattern1, content):
        agents.add(match.group(1))

    # 패턴 2: 테이블 행에서 에이전트 추출 (| 에이전트 | 또는 | Agent | 컬럼)
    # 예: | task-executor | ... |
    # 에이전트 이름 패턴: 소문자, 하이픈, 숫자
    table_pattern = r'\|\s*`?([a-z][a-z0-9-]*)`?\s*\|'
    for match in re.finditer(table_pattern, content):
        name = match.group(1)
        # 일반적인 에이전트 이름 패턴 검증
        if re.match(r'^[a-z]+-[a-z]+', name) or name in ['Explore', 'explore']:
            if name.lower() != 'explore':  # 내장 에이전트 제외
                agents.add(name)

    # 패턴 3: v/agent/xxx.md 참조
    pattern3 = r'v/agent/([^/\s\)]+)\.md'
    for match in re.finditer(pattern3, content):
        agents.add(match.group(1))

    # 패턴 4: .claude/agents/xxx.md 참조
    pattern4 = r'\.claude/agents/([^/\s\)]+)\.md'
    for match in re.finditer(pattern4, content):
        agents.add(match.group(1))

    # 내장 에이전트 및 플레이스홀더 제외
    builtin = {'Explore', 'explore', 'general-purpose', 'Plan'}
    # 패키지 이름 제외 (python-docx, python-pptx, mermaid-cli 등은 에이전트가 아님)
    placeholders = {'xxx', 'name', '[name]', 'example', 'sample', 'sync-agents',
                    'sync-skills', 'python-pptx', 'python-docx', 'mermaid-cli',
                    'oaisqa'}  # oaisqa는 파일명에 하이픈 없음
    agents = agents - builtin - placeholders

    # [xxx] 형태의 플레이스홀더 제거
    agents = {a for a in agents if not (a.startswith('[') or a.endswith(']'))}

    return agents


def extract_commands(content: str) -> set:
    """스킬 파일에서 참조된 커맨드 추출"""
    commands = set()

    # 패턴 1: v/command/xxx.md 참조
    pattern1 = r'v/command/([^/\s\)]+)\.md'
    for match in re.finditer(pattern1, content):
        name = match.group(1)
        if name != 'README':
            commands.add(name)

    # 패턴 2: .claude/commands/xxx.md 참조
    pattern2 = r'\.claude/commands/([^/\s\)]+)\.md'
    for match in re.finditer(pattern2, content):
        commands.add(match.group(1))

    # 플레이스홀더 및 와일드카드 제외
    placeholders = {'xxx', '*', 'example', 'sample', '[name]'}
    commands = commands - placeholders
    commands = {c for c in commands if not (c.startswith('[') or c.endswith(']') or '*' in c)}

    return commands


def extract_mcps(content: str) -> set:
    """스킬 파일에서 참조된 MCP 서버 추출"""
    mcps = set()

    # 패턴 1: mcp__xxx__ 형태
    pattern1 = r'mcp__([a-z][a-z0-9_-]*)__'
    for match in re.finditer(pattern1, content):
        mcps.add(match.group(1))

    # 플레이스홀더 제외
    placeholders = {'xxx', 'example', 'sample'}
    mcps = mcps - placeholders

    return mcps


def validate_skill(skill_path: Path, env: EnvironmentInfo) -> ValidationResult:
    """단일 스킬 파일 검증"""
    content = skill_path.read_text(encoding='utf-8')
    result = ValidationResult(skill_file=skill_path.name)

    # 에이전트 검증
    agents = extract_agents(content)
    all_agents = env.agents_v | env.agents_claude
    # 에이전트 이름 정규화 (하이픈/언더스코어 변환, 하이픈 제거)
    all_agents_normalized = {a.replace('_', '-') for a in all_agents}
    all_agents_normalized |= {a.replace('-', '_') for a in all_agents}
    all_agents_normalized |= {a.replace('-', '') for a in all_agents}  # oais-qa -> oaisqa
    all_agents |= all_agents_normalized

    for agent in agents:
        agent_normalized = agent.replace('_', '-')
        agent_no_hyphen = agent.replace('-', '')
        # oais- 접두사 변형 체크
        agent_with_oais = f"oais-{agent}"
        if (agent in all_agents or agent_normalized in all_agents or
            agent_no_hyphen in all_agents or agent_with_oais in all_agents):
            result.agents_found.append(agent)
        else:
            result.agents_missing.append(agent)

    # 커맨드 검증
    commands = extract_commands(content)
    all_commands = env.commands_v | env.commands_claude
    for cmd in commands:
        if cmd in all_commands:
            result.commands_found.append(cmd)
        else:
            result.commands_missing.append(cmd)

    # MCP 검증
    mcps = extract_mcps(content)
    for mcp in mcps:
        # MCP 이름 정규화
        mcp_normalized = mcp.replace('_', '-')
        # 여러 형태로 검색
        if mcp in env.mcp_servers or mcp_normalized in env.mcp_servers:
            result.mcps_found.append(mcp)
        else:
            # 내장 도구 (Claude Code 기본 제공)
            builtin_tools = ['grep', 'glob', 'read', 'write', 'edit', 'bash', 'ide']
            # 선택적 MCP (설치되지 않아도 경고만)
            optional_mcps = ['serena', 'playwright', 'context7', 'magic']
            if mcp.lower() in builtin_tools:
                result.mcps_found.append(mcp + ' (builtin)')
            elif mcp.lower() in optional_mcps:
                result.mcps_found.append(mcp + ' (optional)')
            else:
                result.mcps_missing.append(mcp)

    return result


def validate_all(project_root: Path, verbose: bool = False) -> list:
    """모든 oais*.md 스킬 검증"""
    env = load_environment(project_root)
    results = []

    skill_dir = project_root / 'v'
    skill_files = list(skill_dir.glob('oais*.md'))

    print("=" * 60)
    print("oaisenv validate --full: 스킬 참조 정합성 검증")
    print("=" * 60)
    print(f"\n스킬 파일 수: {len(skill_files)}")
    print(f"환경 에이전트 (v/agent/): {len(env.agents_v)}개")
    print(f"환경 에이전트 (.claude/agents/): {len(env.agents_claude)}개")
    print(f"환경 커맨드 (v/command/): {len(env.commands_v)}개")
    print(f"환경 커맨드 (.claude/commands/): {len(env.commands_claude)}개")
    print(f"MCP 서버: {len(env.mcp_servers)}개 - {', '.join(env.mcp_servers) if env.mcp_servers else '없음'}")
    print("-" * 60)

    for skill_path in sorted(skill_files):
        result = validate_skill(skill_path, env)
        results.append(result)

        has_issues = result.agents_missing or result.commands_missing or result.mcps_missing

        if verbose or has_issues:
            print(f"\n[{result.skill_file}]")

            if result.agents_found and verbose:
                print(f"  ✅ 에이전트: {', '.join(result.agents_found)}")
            if result.agents_missing:
                print(f"  ❌ 에이전트 누락: {', '.join(result.agents_missing)}")

            if result.commands_found and verbose:
                print(f"  ✅ 커맨드: {', '.join(result.commands_found)}")
            if result.commands_missing:
                print(f"  ❌ 커맨드 누락: {', '.join(result.commands_missing)}")

            if result.mcps_found and verbose:
                print(f"  ✅ MCP: {', '.join(result.mcps_found)}")
            if result.mcps_missing:
                print(f"  ❌ MCP 누락: {', '.join(result.mcps_missing)}")

    return results


def print_summary(results: list):
    """결과 요약 출력"""
    total_agents_missing = sum(len(r.agents_missing) for r in results)
    total_commands_missing = sum(len(r.commands_missing) for r in results)
    total_mcps_missing = sum(len(r.mcps_missing) for r in results)

    print("\n" + "=" * 60)
    print("검증 결과 요약")
    print("=" * 60)

    if total_agents_missing == 0 and total_commands_missing == 0 and total_mcps_missing == 0:
        print("✅ 모든 참조가 유효합니다!")
    else:
        print(f"❌ 에이전트 누락: {total_agents_missing}건")
        print(f"❌ 커맨드 누락: {total_commands_missing}건")
        print(f"❌ MCP 누락: {total_mcps_missing}건")

        print("\n[누락 상세]")
        for r in results:
            if r.agents_missing:
                for agent in r.agents_missing:
                    print(f"  - [{r.skill_file}] 에이전트: {agent}")
            if r.commands_missing:
                for cmd in r.commands_missing:
                    print(f"  - [{r.skill_file}] 커맨드: {cmd}")
            if r.mcps_missing:
                for mcp in r.mcps_missing:
                    print(f"  - [{r.skill_file}] MCP: {mcp}")

    return total_agents_missing + total_commands_missing + total_mcps_missing


def generate_todo_entries(results: list, sp: str = "00") -> list:
    """누락 항목에 대한 todo 엔트리 생성"""
    entries = []

    for r in results:
        if r.agents_missing:
            entries.append(f"[VALIDATION] {r.skill_file}: 에이전트 누락 - {', '.join(r.agents_missing)}")
        if r.commands_missing:
            entries.append(f"[VALIDATION] {r.skill_file}: 커맨드 누락 - {', '.join(r.commands_missing)}")
        if r.mcps_missing:
            entries.append(f"[VALIDATION] {r.skill_file}: MCP 누락 - {', '.join(r.mcps_missing)}")

    return entries


def main():
    parser = argparse.ArgumentParser(
        description='oaisenv validate --full: 스킬 참조 정합성 검증'
    )
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='상세 출력 (유효한 참조도 표시)')
    parser.add_argument('--sp', type=str, default='00',
                        help='서브프로젝트 번호 (기본: 00)')
    parser.add_argument('--output-todo', action='store_true',
                        help='누락 항목을 todo 형식으로 출력')

    args = parser.parse_args()

    # 프로젝트 루트 찾기
    project_root = Path.cwd()
    while project_root != project_root.parent:
        if (project_root / 'v').exists():
            break
        project_root = project_root.parent

    if not (project_root / 'v').exists():
        print("오류: 프로젝트 루트를 찾을 수 없습니다.")
        return 1

    results = validate_all(project_root, args.verbose)
    missing_count = print_summary(results)

    if args.output_todo and missing_count > 0:
        print("\n[Todo 엔트리]")
        entries = generate_todo_entries(results, args.sp)
        for entry in entries:
            print(f"- {entry}")

    return 1 if missing_count > 0 else 0


if __name__ == '__main__':
    exit(main())
