"""
oaisenv sync-agents / sync-skills: 내용 수준 병합 스크립트

[sync-agents]
Source of Truth: v/agent/
Targets: .claude/agents/, .gemini/agents/

[sync-skills]
Source of Truth: v/oais*.md
Targets: .claude/skills/oais*/SKILL.md

충돌 해결: Source 우선
"""

import re
import sys
import io
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

# Windows 콘솔 UTF-8 출력 설정
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


@dataclass
class Section:
    """마크다운 섹션을 나타내는 클래스"""
    heading: str  # 섹션 헤딩 (예: "## 1. 개요")
    level: int    # 헤딩 레벨 (1-6)
    content: str  # 섹션 내용 (헤딩 포함)

    def __eq__(self, other):
        if not isinstance(other, Section):
            return False
        return self.heading == other.heading and self.content == other.content

    def __hash__(self):
        return hash((self.heading, self.content))


@dataclass
class MergeResult:
    """병합 결과를 나타내는 클래스"""
    file_name: str
    added_sections: list = field(default_factory=list)      # Source에서 Target으로 추가
    overwritten_sections: list = field(default_factory=list) # Source 우선으로 덮어쓰기
    reverse_merge_candidates: list = field(default_factory=list)  # Target에만 존재 (역병합 후보)
    unchanged_sections: list = field(default_factory=list)   # 변경 없음


def parse_sections(content: str) -> list[Section]:
    """마크다운 내용을 섹션으로 파싱"""
    sections = []
    lines = content.split('\n')
    current_heading = None
    current_level = 0
    current_content = []

    heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$')

    for line in lines:
        match = heading_pattern.match(line)
        if match:
            # 이전 섹션 저장
            if current_heading is not None:
                sections.append(Section(
                    heading=current_heading,
                    level=current_level,
                    content='\n'.join(current_content).strip()
                ))

            # 새 섹션 시작
            current_level = len(match.group(1))
            current_heading = line
            current_content = [line]
        else:
            current_content.append(line)

    # 마지막 섹션 저장
    if current_heading is not None:
        sections.append(Section(
            heading=current_heading,
            level=current_level,
            content='\n'.join(current_content).strip()
        ))

    return sections


def get_section_key(section: Section) -> str:
    """섹션 식별을 위한 키 생성 (헤딩 텍스트에서 번호와 제목 추출)"""
    # "## 1.2 제목" -> "1.2 제목" 형태로 정규화
    heading_text = re.sub(r'^#+\s*', '', section.heading)
    return heading_text.strip()


def merge_sections(source_sections: list[Section], target_sections: list[Section]) -> tuple[list[Section], MergeResult]:
    """섹션 병합 수행 (Source 우선)"""
    result = MergeResult(file_name="")
    merged_sections = []

    source_dict = {get_section_key(s): s for s in source_sections}
    target_dict = {get_section_key(s): s for s in target_sections}

    # Source 섹션 순서대로 처리
    for key, source_section in source_dict.items():
        if key in target_dict:
            target_section = target_dict[key]
            if source_section.content == target_section.content:
                # 내용 동일 - 변경 없음
                result.unchanged_sections.append(key)
            else:
                # 내용 다름 - Source 우선 덮어쓰기
                result.overwritten_sections.append(key)
        else:
            # Source에만 존재 - Target에 추가
            result.added_sections.append(key)

        merged_sections.append(source_section)

    # Target에만 있는 섹션 (역병합 후보)
    for key, target_section in target_dict.items():
        if key not in source_dict:
            result.reverse_merge_candidates.append(key)
            # 역병합 후보도 결과에 포함 (유지)
            merged_sections.append(target_section)

    return merged_sections, result


def sections_to_content(sections: list[Section]) -> str:
    """섹션 목록을 마크다운 문자열로 변환"""
    return '\n\n'.join(s.content for s in sections)


def sync_file(source_path: Path, target_path: Path, dry_run: bool = False, verbose: bool = False) -> Optional[MergeResult]:
    """단일 파일 동기화"""
    if not source_path.exists():
        return None

    source_content = source_path.read_text(encoding='utf-8')
    source_sections = parse_sections(source_content)

    if target_path.exists():
        target_content = target_path.read_text(encoding='utf-8')
        target_sections = parse_sections(target_content)
    else:
        target_sections = []

    merged_sections, result = merge_sections(source_sections, target_sections)
    result.file_name = source_path.name

    if not dry_run:
        # 실제 파일 쓰기
        target_path.parent.mkdir(parents=True, exist_ok=True)
        merged_content = sections_to_content(merged_sections)
        target_path.write_text(merged_content, encoding='utf-8')

    if verbose:
        print(f"\n[{result.file_name}]")
        if result.added_sections:
            print(f"  + 추가: {', '.join(result.added_sections)}")
        if result.overwritten_sections:
            print(f"  * 덮어쓰기 (Source 우선): {', '.join(result.overwritten_sections)}")
        if result.reverse_merge_candidates:
            print(f"  ? 역병합 후보: {', '.join(result.reverse_merge_candidates)}")
        if result.unchanged_sections:
            print(f"  = 변경없음: {len(result.unchanged_sections)}개 섹션")

    return result


def sync_agents(
    source_dir: Path,
    target_dirs: list[Path],
    dry_run: bool = False,
    verbose: bool = False,
    reverse: bool = False,
    section_filter: Optional[str] = None
) -> list[MergeResult]:
    """에이전트 폴더 동기화 실행"""

    if reverse:
        # 역방향: Target -> Source
        print("[역방향 동기화] Target -> Source")
        source_dir, target_dirs = target_dirs[0], [source_dir]

    results = []

    # Source 파일 목록
    source_files = list(source_dir.glob('*.md'))

    print(f"Source: {source_dir}")
    print(f"Targets: {', '.join(str(t) for t in target_dirs)}")
    print(f"파일 수: {len(source_files)}")
    if dry_run:
        print("[DRY-RUN] 실제 변경 없이 미리보기만 수행합니다.")
    print("-" * 50)

    for source_file in source_files:
        for target_dir in target_dirs:
            target_file = target_dir / source_file.name
            result = sync_file(source_file, target_file, dry_run, verbose)
            if result:
                results.append(result)

    return results


def sync_skills(
    project_root: Path,
    dry_run: bool = False,
    verbose: bool = False,
    reverse: bool = False,
    section_filter: Optional[str] = None
) -> list[MergeResult]:
    """스킬 폴더 동기화 실행

    Source: v/oais*.md
    Target: .claude/skills/oais*/SKILL.md

    매핑: v/oaischeck.md -> .claude/skills/oaischeck/SKILL.md
    """

    source_dir = project_root / 'v'
    target_base = project_root / '.claude' / 'skills'

    # Source 파일 목록 (v/oais*.md)
    source_files = list(source_dir.glob('oais*.md'))

    results = []

    print(f"[스킬 동기화]")
    print(f"Source: {source_dir}/oais*.md")
    print(f"Target: {target_base}/oais*/SKILL.md")
    print(f"파일 수: {len(source_files)}")
    if dry_run:
        print("[DRY-RUN] 실제 변경 없이 미리보기만 수행합니다.")
    print("-" * 50)

    for source_file in source_files:
        # 매핑: v/oaischeck.md -> .claude/skills/oaischeck/SKILL.md
        skill_name = source_file.stem  # "oaischeck"
        target_file = target_base / skill_name / 'SKILL.md'

        if reverse:
            # 역방향: Target -> Source
            source_file, target_file = target_file, source_file

        if not source_file.exists():
            continue

        result = sync_file(source_file, target_file, dry_run, verbose)
        if result:
            results.append(result)

    return results


def print_summary(results: list[MergeResult]):
    """결과 요약 출력"""
    print("\n" + "=" * 50)
    print("동기화 결과 요약")
    print("=" * 50)

    total_added = sum(len(r.added_sections) for r in results)
    total_overwritten = sum(len(r.overwritten_sections) for r in results)
    total_reverse = sum(len(r.reverse_merge_candidates) for r in results)
    total_unchanged = sum(len(r.unchanged_sections) for r in results)

    print(f"+ 추가된 섹션: {total_added}")
    print(f"* 덮어쓴 섹션 (Source 우선): {total_overwritten}")
    print(f"? 역병합 후보: {total_reverse}")
    print(f"= 변경 없음: {total_unchanged}")

    if total_reverse > 0:
        print("\n[역병합 후보 상세]")
        for r in results:
            if r.reverse_merge_candidates:
                for section in r.reverse_merge_candidates:
                    print(f"  - [{r.file_name}] {section}")


def main():
    parser = argparse.ArgumentParser(
        description='에이전트/스킬 폴더 내용 수준 병합 (oaisenv sync-agents / sync-skills)'
    )
    parser.add_argument('mode', nargs='?', default='agents',
                        choices=['agents', 'skills'],
                        help='동기화 모드: agents (기본) 또는 skills')
    parser.add_argument('--dry-run', action='store_true',
                        help='실제 변경 없이 미리보기만')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='상세 변경 내역 출력')
    parser.add_argument('--reverse', action='store_true',
                        help='Target -> Source 역방향 동기화')
    parser.add_argument('--section', type=str, default=None,
                        help='특정 섹션만 동기화')
    parser.add_argument('--source', type=str, default=None,
                        help='Source 디렉토리 (agents 모드 기본: v/agent)')
    parser.add_argument('--targets', type=str, nargs='+',
                        default=None,
                        help='Target 디렉토리 목록 (agents 모드 기본: .claude/agents .gemini/agents)')

    args = parser.parse_args()

    # 프로젝트 루트 찾기
    project_root = Path.cwd()
    while project_root != project_root.parent:
        if (project_root / 'v').exists():
            break
        project_root = project_root.parent

    if args.mode == 'skills':
        # 스킬 동기화 모드
        if args.reverse:
            print("[역방향 동기화] Target -> Source")
        results = sync_skills(
            project_root=project_root,
            dry_run=args.dry_run,
            verbose=args.verbose,
            reverse=args.reverse,
            section_filter=args.section
        )
    else:
        # 에이전트 동기화 모드 (기본)
        source = args.source or 'v/agent'
        targets = args.targets or ['.claude/agents', '.gemini/agents']

        source_dir = project_root / source
        target_dirs = [project_root / t for t in targets]

        if not source_dir.exists():
            print(f"Source 디렉토리가 존재하지 않습니다: {source_dir}")
            return 1

        results = sync_agents(
            source_dir=source_dir,
            target_dirs=target_dirs,
            dry_run=args.dry_run,
            verbose=args.verbose,
            reverse=args.reverse,
            section_filter=args.section
        )

    print_summary(results)

    return 0


if __name__ == '__main__':
    exit(main())
