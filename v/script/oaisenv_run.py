#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""oaisenv_run.py - 개발 환경 분석 및 자동 수정 (상세: doc/a0009_script.md)"""

import sys
import subprocess
import shutil
import json
import os
from pathlib import Path
from datetime import datetime
from oais_common import (
    show_help_if_no_args, PROJECT_ROOT, DOC_DIR, SCRIPT_DIR,
    log_ok, log_warn, log_info, log_error, log_dry_run
)

MCP_JSON_PATH = PROJECT_ROOT / ".mcp.json"
ENV_REPORT_PATH = DOC_DIR / "d0009_env.md"
TEMPLATE_DIR = PROJECT_ROOT / "v" / "template"
ENV_TEMPLATE_PATH = TEMPLATE_DIR / "oaisenv_template.md"

# Dev group required tools
DEV_TOOLS = ["pylint", "mypy", "pytest", "black", "isort"]

# Plugin names for O/X status check (details in template)
PLUGIN_NAMES = [
    "code-review", "commit-commands", "frontend-design", "feature-dev",
    "context7", "serena", "playwright", "typescript-lsp",
    "pyright-lsp", "security-guidance", "paper-search-tools", "oh-my-claudecode"
]

# Claude skill names for O/X status check (details in template)
CLAUDE_SKILL_NAMES = [
    "algorithmic-art", "brand-guidelines", "canvas-design", "doc-coauthoring",
    "docx", "internal-comms", "mcp-builder", "pdf", "pptx", "skill-creator",
    "slack-gif-creator", "theme-factory", "webapp-testing", "web-artifacts-builder", "xlsx"
]

# Agent registry (v/agent/*.md)
# Format: "agent_name": "description"
AGENT_REGISTRY = {
    "academic-researcher": "학술 연구",
    "ai-engineer": "AI 엔지니어링",
    "codebase_investigator": "코드베이스 조사",
    "code-error-checker": "코드 에러 체크",
    "data-analyst": "데이터 분석",
    "data-engineer": "데이터 엔지니어링",
    "data-scientist": "데이터 사이언스",
    "frontend-developer": "프론트엔드 개발",
    "img-extract": "이미지 추출",
    "jupyter-specialist": "Jupyter 전문가",
    "oaisppt-agent": "PPT 생성",
    "oaisqa": "품질 분석",
    "oaiswebdesigner": "웹 디자이너",
    "oais-web-test-orchestrator": "웹 테스트",
    "python-code-reviewer": "Python 코드 리뷰",
    "streamlit-code-reviewer": "Streamlit 코드 리뷰",
    "streamlit-implementer": "Streamlit 구현",
    "streamlit-page-designer": "Streamlit 페이지 설계",
    "streamlit-page-planner": "Streamlit 페이지 계획",
    "task-checker": "태스크 검증",
    "task-executor": "태스크 실행",
    "translator": "번역",
    "web-design-expert": "웹 디자인",
}

# Command registry (v/command/*.md)
# Format: "command_name": "description"
COMMAND_REGISTRY = {
    "analyze": "코드 분석",
    "build": "프로젝트 빌드",
    "cleanup": "코드 및 프로젝트 정리",
    "design": "시스템 및 컴포넌트 설계",
    "document": "집중 문서화",
    "estimate": "개발 추정",
    "explain": "코드 및 개념 설명",
    "git": "Git 작업",
    "implement": "기능 구현",
    "improve": "코드 개선",
    "index": "프로젝트 인덱싱",
    "load": "프로젝트 컨텍스트 로드",
    "spawn": "태스크 분할 및 병렬 실행",
    "task": "태스크 관리",
    "test": "테스트 실행",
    "troubleshoot": "문제 해결",
    "workflow": "워크플로우 생성",
}

# Known MCP server package mappings
# Format: "server_name": {"role": "description", "package": "npm_package", "env": {}, "api_key_required": bool}
MCP_SERVER_REGISTRY = {
    "sequential-thinking": {
        "role": "복잡한 다단계 분석/추론",
        "package": "@modelcontextprotocol/server-sequential-thinking",
        "env": {},
        "api_key_required": False
    },
    "github": {
        "role": "GitHub 저장소/이슈/PR 관리",
        "package": "@modelcontextprotocol/server-github",
        "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"},
        "api_key_required": True,
        "api_key_name": "GITHUB_PERSONAL_ACCESS_TOKEN"
    },
    "filesystem": {
        "role": "파일 시스템 접근/관리",
        "package": "@modelcontextprotocol/server-filesystem",
        "env": {},
        "api_key_required": False
    },
    "puppeteer": {
        "role": "브라우저 자동화/스크래핑",
        "package": "@modelcontextprotocol/server-puppeteer",
        "env": {},
        "api_key_required": False
    },
    "brave-search": {
        "role": "Brave 검색 엔진 연동",
        "package": "@modelcontextprotocol/server-brave-search",
        "env": {"BRAVE_API_KEY": "${BRAVE_API_KEY}"},
        "api_key_required": True,
        "api_key_name": "BRAVE_API_KEY"
    },
    "google-maps": {
        "role": "Google Maps API 연동",
        "package": "@modelcontextprotocol/server-google-maps",
        "env": {"GOOGLE_MAPS_API_KEY": "${GOOGLE_MAPS_API_KEY}"},
        "api_key_required": True,
        "api_key_name": "GOOGLE_MAPS_API_KEY"
    },
    "slack": {
        "role": "Slack 메시지/채널 관리",
        "package": "@modelcontextprotocol/server-slack",
        "env": {"SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}"},
        "api_key_required": True,
        "api_key_name": "SLACK_BOT_TOKEN"
    },
    "memory": {
        "role": "대화 컨텍스트 메모리 관리",
        "package": "@modelcontextprotocol/server-memory",
        "env": {},
        "api_key_required": False
    },
    "postgres": {
        "role": "PostgreSQL DB 연동",
        "package": "@modelcontextprotocol/server-postgres",
        "env": {"POSTGRES_CONNECTION_STRING": "${POSTGRES_CONNECTION_STRING}"},
        "api_key_required": True,
        "api_key_name": "POSTGRES_CONNECTION_STRING"
    },
    "sqlite": {
        "role": "SQLite DB 연동",
        "package": "@modelcontextprotocol/server-sqlite",
        "env": {},
        "api_key_required": False
    },
    "taskmaster-ai": {
        "role": "AI 기반 태스크 관리",
        "package": "task-master-ai",
        "env": {},
        "api_key_required": False
    },
    "context7-mcp": {
        "role": "라이브러리 문서 조회 (MCP)",
        "package": "@upstash/context7-mcp",
        "smithery": True,
        "env": {},
        "api_key_required": False
    },
    "google": {
        "role": "Google API 연동",
        "package": "@anthropic/mcp-server-google",
        "env": {"GOOGLE_API_KEY": "${GOOGLE_API_KEY}"},
        "api_key_required": True,
        "api_key_name": "GOOGLE_API_KEY"
    },
}


def check_command(command: str) -> bool:
    """Check if a command exists in the path."""
    return shutil.which(command) is not None


def run_command(cmd: list, description: str, capture: bool = True) -> tuple:
    """Run a command and return (success, output)."""
    try:
        if capture:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                check=False,
                cwd=str(PROJECT_ROOT)
            )
            return result.returncode == 0, result.stdout + result.stderr
        else:
            result = subprocess.run(cmd, check=False, cwd=str(PROJECT_ROOT))
            return result.returncode == 0, ""
    except Exception as e:
        return False, str(e)


def check_dev_tools() -> dict:
    """Check dev tools installation status."""
    status = {}
    for tool in DEV_TOOLS:
        status[tool] = check_command(tool)
    return status


def install_dev_group(dry_run: bool = False) -> bool:
    """Install UV dev group."""
    print("\n## UV Dev Group Install")

    if dry_run:
        print("[DRY-RUN] Will run: uv sync --group dev")
        return True

    print("Running: uv sync --group dev")
    success, output = run_command(["uv", "sync", "--group", "dev"], "UV dev group install")

    if success:
        print("[OK] Dev group installed")
    else:
        print(f"[ERROR] Install failed: {output[:200]}")

    return success


def check_uv_status() -> dict:
    """Check UV dependency status."""
    result = {
        "uv_installed": check_command("uv"),
        "outdated": [],
        "missing": []
    }

    if not result["uv_installed"]:
        return result

    # Check installed packages with uv pip list
    success, output = run_command(["uv", "pip", "list"], "package list")

    return result


def check_plugins(verbose: bool = False) -> dict:
    """Check plugin status."""
    result = {
        "superpowers": False,
        "message": ""
    }

    # superpowers plugin check (only meaningful in Claude Code environment)
    # Return basic status here
    result["message"] = "Check plugin status in Claude Code environment."

    return result


# ============================================================
# MCP Server Management Functions
# ============================================================

def read_mcp_json() -> dict:
    """Read .mcp.json file."""
    if not MCP_JSON_PATH.exists():
        return {"mcpServers": {}}

    with open(MCP_JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_mcp_json(data: dict) -> bool:
    """Write .mcp.json file."""
    try:
        with open(MCP_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent='\t', ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to write .mcp.json: {e}")
        return False


def get_installed_mcp_servers() -> list:
    """Get list of installed MCP servers from .mcp.json."""
    mcp_data = read_mcp_json()
    return list(mcp_data.get("mcpServers", {}).keys())


def get_missing_mcp_from_validation() -> list:
    """Get missing MCP servers from validation script output."""
    missing = []
    validate_script = SCRIPT_DIR / "oaisenv_validate_full.py"

    if not validate_script.exists():
        return missing

    success, output = run_command(
        ["uv", "run", "python", str(validate_script)],
        "validation check"
    )

    # Parse output to find missing MCP servers
    # Look for lines like: "  - [oaispaper.md] MCP: paperswithcode"
    for line in output.split('\n'):
        if 'MCP:' in line and '[' in line:
            # Extract MCP server name
            parts = line.split('MCP:')
            if len(parts) > 1:
                mcp_name = parts[1].strip()
                if mcp_name and mcp_name not in missing:
                    missing.append(mcp_name)

    return missing


def generate_mcp_config(server_name: str) -> dict:
    """Generate MCP server configuration for .mcp.json."""
    registry_info = MCP_SERVER_REGISTRY.get(server_name)

    if not registry_info:
        # Unknown server - create basic config
        return {
            "type": "stdio",
            "command": "cmd",
            "args": ["/c", "npx", "-y", server_name],
            "disabled": True,  # Disabled by default for unknown servers
            "_note": "Unknown server - verify package name and enable manually"
        }

    package = registry_info["package"]

    # Check if it uses smithery
    if registry_info.get("smithery"):
        config = {
            "type": "stdio",
            "command": "cmd",
            "args": ["/c", "npx", "-y", "@smithery/cli@latest", "run", package]
        }
    else:
        config = {
            "type": "stdio",
            "command": "cmd",
            "args": ["/c", "npx", "-y", package]
        }

    # Add environment variables if needed
    if registry_info.get("env"):
        config["env"] = registry_info["env"]

    # Add note about API key if required
    if registry_info.get("api_key_required"):
        config["_api_key_required"] = registry_info.get("api_key_name", "API_KEY")

    return config


def install_mcp_server(server_name: str, dry_run: bool = False) -> bool:
    """Install MCP server by adding to .mcp.json."""
    mcp_data = read_mcp_json()

    if server_name in mcp_data.get("mcpServers", {}):
        print(f"  [SKIP] {server_name} already configured")
        return True

    config = generate_mcp_config(server_name)
    registry_info = MCP_SERVER_REGISTRY.get(server_name)

    if dry_run:
        print(f"  [DRY-RUN] Would add: {server_name}")
        if registry_info and registry_info.get("api_key_required"):
            print(f"    [INFO] Requires API key: {registry_info.get('api_key_name')}")
        return True

    # Add to mcp_data
    if "mcpServers" not in mcp_data:
        mcp_data["mcpServers"] = {}

    mcp_data["mcpServers"][server_name] = config

    if write_mcp_json(mcp_data):
        print(f"  [OK] Added: {server_name}")
        if registry_info and registry_info.get("api_key_required"):
            print(f"    [INFO] Set {registry_info.get('api_key_name')} in .env")
        return True
    else:
        print(f"  [ERROR] Failed to add: {server_name}")
        return False


def check_mcp_status() -> dict:
    """Check MCP server status."""
    result = {
        "installed": get_installed_mcp_servers(),
        "missing": [],
        "unknown": []
    }

    # Get missing from validation
    missing_from_validation = get_missing_mcp_from_validation()

    for server in missing_from_validation:
        if server in MCP_SERVER_REGISTRY:
            result["missing"].append(server)
        else:
            result["unknown"].append(server)

    return result


def run_validation(verbose: bool = False) -> dict:
    """Run validation check."""
    result = {
        "passed": True,
        "issues": []
    }

    # Check if validate_full script exists
    validate_script = SCRIPT_DIR / "oaisenv_validate_full.py"
    if validate_script.exists():
        success, output = run_command(
            ["uv", "run", "python", str(validate_script)],
            "validation check"
        )
        if not success:
            result["passed"] = False
            result["issues"].append("Validation check failed")

    return result


def get_python_version() -> str:
    """Get Python version."""
    success, output = run_command(["python", "--version"], "python version")
    if success:
        return output.strip()
    return "Unknown"


def get_uv_version() -> str:
    """Get UV version."""
    success, output = run_command(["uv", "--version"], "uv version")
    if success:
        return output.strip()
    return "Unknown"


def get_node_version() -> str:
    """Get Node.js version."""
    success, output = run_command(["node", "--version"], "node version")
    if success:
        return output.strip()
    return "Not installed"


def get_npm_version() -> str:
    """Get npm version."""
    success, output = run_command(["npm", "--version"], "npm version")
    if success:
        return output.strip()
    return "Not installed"


def get_git_version() -> str:
    """Get Git version."""
    success, output = run_command(["git", "--version"], "git version")
    if success:
        return output.strip()
    return "Not installed"


def get_pandoc_version() -> str:
    """Get Pandoc version."""
    success, output = run_command(["pandoc", "--version"], "pandoc version")
    if success:
        return output.split('\n')[0].strip()
    return "Not installed"


def get_installed_packages() -> list:
    """Get list of installed Python packages."""
    success, output = run_command(["uv", "pip", "list", "--format=columns"], "package list")
    packages = []
    if success:
        lines = output.strip().split('\n')
        for line in lines[2:]:  # Skip header
            parts = line.split()
            if len(parts) >= 2:
                packages.append({"name": parts[0], "version": parts[1]})
    return packages


def get_pytorch_info() -> tuple:
    """Get PyTorch version and CUDA availability."""
    pytorch_version = "미설치"
    cuda_available = "-"

    # Check if torch is installed
    success, output = run_command(
        ["uv", "run", "python", "-c", "import torch; print(torch.__version__)"],
        "pytorch version"
    )
    if success and output.strip():
        pytorch_version = output.strip()

        # Check CUDA availability
        success2, output2 = run_command(
            ["uv", "run", "python", "-c", "import torch; print('GPU' if torch.cuda.is_available() else 'CPU')"],
            "cuda check"
        )
        if success2:
            cuda_available = output2.strip()

    return pytorch_version, cuda_available


def get_oais_skills() -> list:
    """Get list of oais*.md skill files."""
    skills_dir = PROJECT_ROOT / "v"
    skills = []
    if skills_dir.exists():
        for f in sorted(skills_dir.glob("oais*.md")):
            skills.append(f.name)
    return skills


def get_agents() -> list:
    """Get list of agent files."""
    agents = []
    agent_dirs = [
        PROJECT_ROOT / "v" / "agent",
        PROJECT_ROOT / ".claude" / "agents"
    ]
    for agent_dir in agent_dirs:
        if agent_dir.exists():
            for f in sorted(agent_dir.glob("*.md")):
                agents.append(f.name)
    return list(set(agents))


def get_commands() -> list:
    """Get list of command files."""
    commands = []
    cmd_dirs = [
        PROJECT_ROOT / "v" / "command",
        PROJECT_ROOT / ".claude" / "commands"
    ]
    for cmd_dir in cmd_dirs:
        if cmd_dir.exists():
            for f in sorted(cmd_dir.glob("*.md")):
                commands.append(f.name)
    return list(set(commands))


def get_claude_skills() -> list:
    """Get list of installed Claude skills from .claude/skills/."""
    skills = []
    skills_dir = PROJECT_ROOT / ".claude" / "skills"
    if skills_dir.exists():
        for d in sorted(skills_dir.iterdir()):
            if d.is_dir():
                skills.append(d.name)
    return skills


def get_claude_plugins() -> list:
    """Get list of installed Claude plugins from installed_plugins.json."""
    import os
    plugins = []

    # Path to installed_plugins.json
    user_home = Path(os.environ.get('USERPROFILE', os.environ.get('HOME', '')))
    plugins_file = user_home / ".claude" / "plugins" / "installed_plugins.json"

    if plugins_file.exists():
        data = json.loads(plugins_file.read_text(encoding='utf-8'))
        if 'plugins' in data:
            for plugin_key in sorted(data['plugins'].keys()):
                # Extract plugin name (before @)
                plugin_name = plugin_key.split('@')[0]
                plugins.append(plugin_name)

    return plugins


def generate_env_report(
    tool_status: dict,
    mcp_status: dict,
    validation: dict,
    issues_found: int,
    issues_fixed: int
) -> str:
    """Generate d0009_env.md content using template."""
    now = datetime.now()

    # Read template
    if not ENV_TEMPLATE_PATH.exists():
        print(f"[WARN] Template not found: {ENV_TEMPLATE_PATH}")
        return _generate_env_report_fallback(
            tool_status, mcp_status, validation, issues_found, issues_fixed
        )

    template = ENV_TEMPLATE_PATH.read_text(encoding='utf-8')

    # Get versions
    python_ver = get_python_version()
    uv_ver = get_uv_version()
    node_ver = get_node_version()
    npm_ver = get_npm_version()
    git_ver = get_git_version()
    pandoc_ver = get_pandoc_version()

    # Get project info
    project_skills = get_oais_skills()
    claude_skills = get_claude_skills()
    claude_plugins = get_claude_plugins()
    agents = get_agents()
    commands = get_commands()
    packages = get_installed_packages()
    pytorch_ver, cuda_status = get_pytorch_info()

    # Build dev tools table
    dev_tools_table = ""
    for tool, installed in tool_status.items():
        status = "OK" if installed else "X"
        dev_tools_table += f"| {tool} | {status} |\n"

    # Build MCP status table (using MCP_SERVER_REGISTRY)
    mcp_status_table = ""
    mcp_installed_count = 0
    installed_servers = mcp_status['installed']
    for server_name, info in MCP_SERVER_REGISTRY.items():
        is_installed = server_name in installed_servers
        if is_installed:
            mcp_installed_count += 1
        status = "O" if is_installed else "X"
        if is_installed:
            install_cmd = "-"
        else:
            install_cmd = f"npx -y {info['package']}"
            if info.get('api_key_required'):
                install_cmd += f" (requires {info.get('api_key_name', 'API_KEY')})"
        mcp_status_table += f"| {server_name} | {info['role']} | {status} | `{install_cmd}` |\n"

    # Build plugins O/X status (details in template)
    plugins_installed_count = 0
    plugin_status = {}
    for plugin_name in PLUGIN_NAMES:
        is_installed = plugin_name in claude_plugins
        if is_installed:
            plugins_installed_count += 1
        plugin_status[plugin_name] = "O" if is_installed else "X"

    # Build Claude skills O/X status (details in template)
    claude_skills_installed_count = 0
    claude_skill_status = {}
    for skill_name in CLAUDE_SKILL_NAMES:
        is_installed = skill_name in claude_skills
        if is_installed:
            claude_skills_installed_count += 1
        claude_skill_status[skill_name] = "O" if is_installed else "X"

    # Build Claude skills table
    if claude_skills:
        claude_skills_table = "| 스킬 |\n|------|\n"
        for skill in claude_skills:
            claude_skills_table += f"| {skill} |\n"
    else:
        claude_skills_table = "설치된 Claude 스킬이 없습니다.\n"

    # Build project skills table
    if project_skills:
        skills_table = "| 스킬 파일 |\n|------|\n"
        for skill in project_skills:
            skills_table += f"| {skill} |\n"
    else:
        skills_table = "스킬 파일이 없습니다.\n"

    # Build agents table (registry-based with O/X status)
    installed_agents = [a.replace('.md', '') for a in agents]
    agents_installed_count = 0
    agents_table = ""
    for agent_name, description in sorted(AGENT_REGISTRY.items()):
        is_installed = agent_name in installed_agents
        if is_installed:
            agents_installed_count += 1
        status = "O" if is_installed else "X"
        agents_table += f"| {agent_name} | {status} | {description} |\n"

    # Build commands table (registry-based with O/X status)
    installed_commands = [c.replace('.md', '') for c in commands if c != 'README.md']
    commands_installed_count = 0
    commands_table = ""
    for cmd_name, description in sorted(COMMAND_REGISTRY.items()):
        is_installed = cmd_name in installed_commands
        if is_installed:
            commands_installed_count += 1
        status = "O" if is_installed else "X"
        commands_table += f"| {cmd_name} | {status} | {description} |\n"

    # Build packages table
    if packages:
        packages_table = "| 패키지 | 버전 |\n|------|------|\n"
        for pkg in packages[:50]:
            packages_table += f"| {pkg['name']} | {pkg['version']} |\n"
        if len(packages) > 50:
            packages_table += f"\n... 외 {len(packages) - 50}개\n"
    else:
        packages_table = "설치된 패키지가 없습니다.\n"

    # Build validation issues section
    validation_issues_section = ""
    if validation.get('issues'):
        validation_issues_section = "### 9.1 검증 이슈\n\n"
        for issue in validation['issues']:
            validation_issues_section += f"- {issue}\n"

    # Replace placeholders
    content = template
    replacements = {
        '{{DATE}}': now.strftime('%Y-%m-%d'),
        '{{DATETIME}}': now.strftime('%Y-%m-%d %H:%M:%S'),
        '{{PYTHON_VERSION}}': python_ver,
        '{{UV_VERSION}}': uv_ver,
        '{{NODE_VERSION}}': node_ver,
        '{{NPM_VERSION}}': npm_ver,
        '{{GIT_VERSION}}': git_ver,
        '{{PANDOC_VERSION}}': pandoc_ver,
        '{{DEV_TOOLS_TABLE}}': dev_tools_table.rstrip(),
        '{{MCP_INSTALLED_COUNT}}': str(mcp_installed_count),
        '{{MCP_TOTAL_COUNT}}': str(len(MCP_SERVER_REGISTRY)),
        '{{MCP_STATUS_TABLE}}': mcp_status_table.rstrip(),
        '{{PLUGINS_INSTALLED_COUNT}}': str(plugins_installed_count),
        '{{CLAUDE_SKILLS_INSTALLED_COUNT}}': str(claude_skills_installed_count),
        '{{CLAUDE_SKILLS_COUNT}}': str(len(claude_skills)),
        '{{CLAUDE_SKILLS_TABLE}}': claude_skills_table.rstrip(),
        '{{OAIS_SKILLS_COUNT}}': str(len(project_skills)),
        '{{SKILLS_TABLE}}': skills_table.rstrip(),
        '{{AGENTS_INSTALLED_COUNT}}': str(agents_installed_count),
        '{{AGENTS_TOTAL_COUNT}}': str(len(AGENT_REGISTRY)),
        '{{AGENTS_TABLE}}': agents_table.rstrip(),
        '{{COMMANDS_INSTALLED_COUNT}}': str(commands_installed_count),
        '{{COMMANDS_TOTAL_COUNT}}': str(len(COMMAND_REGISTRY)),
        '{{COMMANDS_TABLE}}': commands_table.rstrip(),
        '{{PACKAGES_COUNT}}': str(len(packages)),
        '{{PYTORCH_VERSION}}': pytorch_ver,
        '{{CUDA_AVAILABLE}}': cuda_status,
        '{{ISSUES_FOUND}}': str(issues_found),
        '{{ISSUES_FIXED}}': str(issues_fixed),
        '{{ISSUES_REMAINING}}': str(issues_found - issues_fixed),
        '{{VALIDATION_STATUS}}': 'PASS' if validation['passed'] else 'FAIL',
        '{{VALIDATION_ISSUES_SECTION}}': validation_issues_section.rstrip(),
    }

    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)

    # Replace plugin status placeholders ({{P_plugin-name}} -> O/X)
    for plugin_name, status in plugin_status.items():
        content = content.replace(f'{{{{P_{plugin_name}}}}}', status)

    # Replace Claude skill status placeholders ({{S_skill-name}} -> O/X)
    for skill_name, status in claude_skill_status.items():
        content = content.replace(f'{{{{S_{skill_name}}}}}', status)

    return content


def _generate_env_report_fallback(
    tool_status: dict,
    mcp_status: dict,
    validation: dict,
    issues_found: int,
    issues_fixed: int
) -> str:
    """Fallback report generation when template is not available."""
    now = datetime.now()
    return f"""# d0009_env.md - 개발 환경 현황

> 생성 시간: {now.strftime('%Y-%m-%d %H:%M:%S')}
> 경고: 템플릿 파일을 찾을 수 없어 기본 형식으로 생성되었습니다.

## 검증 결과

- 발견된 이슈: {issues_found}
- 수정된 이슈: {issues_fixed}
- 검증 상태: {'PASS' if validation['passed'] else 'FAIL'}

---

*템플릿 파일 위치: v/template/d0009_env_template.md*
"""


def write_env_report(
    tool_status: dict,
    mcp_status: dict,
    validation: dict,
    issues_found: int,
    issues_fixed: int
) -> bool:
    """Write environment report to d0009_env.md."""
    DOC_DIR.mkdir(parents=True, exist_ok=True)

    content = generate_env_report(
        tool_status, mcp_status, validation, issues_found, issues_fixed
    )

    ENV_REPORT_PATH.write_text(content, encoding='utf-8')
    print(f"\n[OK] Environment report: {ENV_REPORT_PATH}")
    return True


def run_context_command(args: list) -> int:
    """Run context subcommand via oaisenv_context.py."""
    context_script = SCRIPT_DIR / "oaisenv_context.py"
    if not context_script.exists():
        print(f"[ERROR] Context script not found: {context_script}")
        return 1

    cmd = ["uv", "run", "python", str(context_script)] + args
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    return result.returncode


def main():
    # 서브명령어 없이 실행 시 도움말 출력
    if show_help_if_no_args("oaisenv", sys.argv[1:]):
        return

    args = sys.argv[1:]

    # Handle context subcommand
    if args and args[0] == "context":
        return run_context_command(args[1:])

    # Check for --dry-run flag
    dry_run = "--dry-run" in args

    print("# oaisenv run - Development Environment Check\n")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mode: {'Check only (dry-run)' if dry_run else 'Auto-fix + Verbose'}")
    print("=" * 60)

    issues_found = 0
    issues_fixed = 0

    # 1. UV install check
    print("\n## 1. UV Status")
    if not check_command("uv"):
        print("[ERROR] UV is not installed.")
        print("Install: https://docs.astral.sh/uv/getting-started/installation/")
        return 1
    print("[OK] UV installed")

    # 2. Dev tools status
    print("\n## 2. Dev Tools Status")
    print("| Tool | Status |")
    print("|------|--------|")

    tool_status = check_dev_tools()
    missing_tools = []

    for tool, installed in tool_status.items():
        status = "[OK]" if installed else "[X]"
        print(f"| {tool} | {status} |")
        if not installed:
            missing_tools.append(tool)
            issues_found += 1

    # 3. Auto-install missing tools
    if missing_tools:
        print(f"\n[WARN] Missing tools: {', '.join(missing_tools)}")

        if install_dev_group(dry_run):
            if not dry_run:
                # Re-check
                new_status = check_dev_tools()
                fixed = sum(1 for t in missing_tools if new_status.get(t, False))
                issues_fixed += fixed
                print(f"[OK] {fixed} tools installed")
    else:
        print("\n[OK] All dev tools installed")

    # 4. MCP Server Check
    print("\n## 3. MCP Server Status")
    mcp_status = check_mcp_status()

    print(f"Installed: {len(mcp_status['installed'])} servers")
    for server in mcp_status['installed']:
        print(f"  - {server}")

    # Handle missing MCP servers
    if mcp_status['missing'] or mcp_status['unknown']:
        print(f"\nMissing (known): {len(mcp_status['missing'])}")
        for server in mcp_status['missing']:
            print(f"  - {server}")
            issues_found += 1

        print(f"Missing (unknown): {len(mcp_status['unknown'])}")
        for server in mcp_status['unknown']:
            print(f"  - {server} [manual setup required]")
            issues_found += 1

        # Auto-install known missing servers
        if mcp_status['missing']:
            print("\n## MCP Server Install")
            for server in mcp_status['missing']:
                if install_mcp_server(server, dry_run):
                    if not dry_run:
                        issues_fixed += 1

        # Create placeholder for unknown servers
        if mcp_status['unknown'] and not dry_run:
            print("\n## Unknown MCP Servers (disabled)")
            for server in mcp_status['unknown']:
                install_mcp_server(server, dry_run)
    else:
        print("[OK] All required MCP servers configured")

    # 5. Validation check (final)
    print("\n## 4. Validation Check")
    validation = run_validation(True)
    if validation["passed"]:
        print("[OK] Validation passed")
    else:
        for issue in validation["issues"]:
            print(f"[WARN] {issue}")
            # Don't double-count issues already counted from MCP check

    # 6. Generate environment report
    write_env_report(tool_status, mcp_status, validation, issues_found, issues_fixed)

    # 7. Summary
    print("\n" + "=" * 60)
    print("# Summary")
    print("=" * 60)
    print(f"\nIssues found: {issues_found}")
    print(f"Issues fixed: {issues_fixed}")

    if issues_found > issues_fixed:
        remaining = issues_found - issues_fixed
        print(f"Remaining issues: {remaining}")
        print("\n[WARN] Some issues require manual action.")
        return 1
    else:
        print("\n[OK] Development environment ready")
        return 0


if __name__ == "__main__":
    sys.exit(main())
