# oaissync - Vibe 환경 동기화

## 문서 이력 관리

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v11 | 2026-01-18 | .claude/ 동기화 대상 확대 (commands/, skills/, agents/ 포함) |
| v10 | 2026-01-15 | 에이전트 출력 규칙 섹션 추가 (스크립트 출력만 표시) |
| v09 | 2026-01-15 | `run --push-only` 명령어 추가 (push만 필요한 프로젝트 일괄 동기화) |
| v08 | 2026-01-15 | list 출력 형식 박스 테이블로 변경 |
| v07 | 2026-01-13 | .claude/settings.local.json 동기화 제외 추가 |

---

> 프로젝트 간 vibe 코딩 환경 파일 동기화 | ref: `v/guide/common_guide.md`

## 개요

현재 프로젝트(vibe)와 다른 프로젝트 간에 vibe 관련 파일/폴더를 비교하고 동기화합니다.
- 한쪽에만 있는 파일 감지
- 양쪽에 있지만 버전이 다른 파일 감지
- 사용자 판단에 따라 가져오기(pull) 또는 보내기(push)

## 명령어

| 명령어 | 설명 |
|--------|------|
| `oaissync status` | 서브명령어 리스트, 동기화 대상 현황 |
| `oaissync version` | 스킬 버전 정보 (v11) |
| `oaissync list` | 동기화 가능한 프로젝트 목록 조회 |
| `oaissync files` | 동기화 대상 파일/폴더 목록 |
| `oaissync view [project]` | 대상 프로젝트와 차이점 비교 (읽기 전용) |
| `oaissync diff [project] [file]` | 특정 파일 내용 비교 (unified diff) |
| `oaissync merge [project] [file]` | **양쪽 파일 병합** (버전 이력 + 섹션 통합) |
| `oaissync run [project]` | 동기화 실행 (대화형) |
| `oaissync run --push-only` | **push만 필요한 모든 프로젝트 일괄 동기화** |

실행: `uv run python v/script/oaissync_run.py [subcommand] [args]`

## 서브명령어 상세

### oaissync list

`../` 경로에서 프로젝트를 스캔하여 vibe 환경 구축 여부를 판별합니다.

**판별 기준**:
| 상태 | 조건 |
|------|------|
| Full | `.claude/` AND `v/` 폴더 모두 존재 |
| Partial | `.claude/` 또는 `v/` 중 하나만 존재 |
| None | vibe 환경 없음 (동기화 대상 가능) |

**Sync 컬럼** (v03 추가):
| 값 | 설명 |
|-----|------|
| OK | 동기화 완료 (차이 없음) |
| 숫자 | 동기화 필요 (차이 파일 수) |
| - | 비교 불가 (Full 상태 아님) |

**출력 예시** (박스 테이블 형식):
```
┌────┬─────────────────┬─────────┬──────────┬─────┬──────┐
│ #  │ Project         │  Status │ .claude/ │  v/ │ Sync │
├────┼─────────────────┼─────────┼──────────┼─────┼──────┤
│  1 │ 0003_CCone      │   Full  │    O     │  O  │  OK  │
│  2 │ 0013_dualbranck │   Full  │    O     │  O  │  3   │
│  3 │ 0000_sandbox    │   None  │    X     │  X  │  -   │
└────┴─────────────────┴─────────┴──────────┴─────┴──────┘
```

### oaissync files

동기화 대상 파일/폴더 목록을 표시합니다.

**기본 동기화 대상** (v/ 폴더 전체):
```
v/
├── *.md                    # 스킬 문서
├── agent/                  # 에이전트 정의
├── command/                # 명령어 정의
├── guide/                  # 가이드 문서
├── script/                 # 스크립트
└── template/               # 템플릿

.claude/
├── *.md                    # SuperClaude 문서 (CLAUDE, COMMANDS, FLAGS 등)
├── commands/               # 슬래시 명령어 정의
├── skills/                 # 스킬 정의
└── agents/                 # 에이전트 정의

루트 설정:
├── CLAUDE.md               # 프로젝트 진입점
├── run_claude.bat          # Windows 실행 스크립트
├── run_claude.sh           # Linux/Mac 실행 스크립트
├── pyproject.toml          # (선택) Python 프로젝트 설정
└── .mcp.json               # (선택) MCP 설정
```

### oaissync view [project]

대상 프로젝트와 차이점을 비교하여 표시합니다 (읽기 전용).

**출력 정보**:
- 파일별 상태 (→/←/>>/<<)
- 수정일 비교
- 상태별 요약 통계

**사용 예시**:
```bash
oaissync view 0003_CCone
```

### oaissync diff [project] [file]

두 프로젝트 간 특정 파일의 내용을 비교하여 unified diff 형식으로 표시합니다.

**출력 정보**:
- 파일 존재 여부
- 수정일 비교
- 줄 단위 차이점 (unified diff)
- 변경 요약 (추가/삭제 줄 수)

**사용 예시**:
```bash
# CLAUDE.md 파일 비교
oaissync diff 0003_CCone CLAUDE.md

# v/ 하위 파일 비교
oaissync diff 0013_dualbranck v/oaissync.md
```

**출력 예시**:
```diff
--- [대상] 0003_CCone/CLAUDE.md
+++ [소스] 0001_vibe/CLAUDE.md
@@ -1,5 +1,6 @@
 # CLAUDE.md
+## 새로운 섹션
 ...
```

### oaissync merge [project] [file]

두 프로젝트의 파일을 지능적으로 병합하여 양쪽의 기능을 통합합니다.

**병합 워크플로우**:
```
1. 양쪽 파일 읽기 (source + target)
     ↓
2. 버전/이력 분석 (문서 이력 관리 섹션 파싱)
     ↓
3. 섹션별 차이점 비교
     ↓
4. 병합 전략 결정:
   - 양쪽에만 있는 섹션 → 모두 포함
   - 동일 섹션 다른 내용 → 최신 버전 선택
     ↓
5. 병합 버전 생성 (버전 +1, 이력 통합)
     ↓
6. 저장 (source) + push (target) 옵션
```

**사용 예시**:
```bash
# 자동 병합 (source에 저장)
oaissync merge 0013 v/oaisreport.md

# 미리보기 (실제 저장 없음)
oaissync merge 0013 v/oaisreport.md --dry-run

# 양쪽에 저장 (source + target)
oaissync merge 0013 v/oaisreport.md --both
```

**옵션**:
| 옵션 | 설명 |
|------|------|
| `--dry-run` | 병합 결과 미리보기 (저장 안 함) |
| `--both` | source와 target 양쪽에 저장 |
| `--prefer-source` | 충돌 시 source 우선 |
| `--prefer-target` | 충돌 시 target 우선 |

**병합 규칙**:
1. **문서 이력 관리**: 양쪽 이력 통합 + 병합 버전 추가
2. **서브명령어 표**: 양쪽 명령어 합집합
3. **섹션**: 한쪽에만 있으면 추가, 양쪽 있으면 최신 버전
4. **의존성**: 양쪽 패키지 합집합

### oaissync run [project]

선택한 프로젝트와 파일을 비교하고 동기화를 수행합니다.

**비교 기준**:
| 상태 | 설명 | 표시 |
|------|------|------|
| ONLY_SOURCE | 현재 프로젝트에만 존재 | `→` |
| ONLY_TARGET | 대상 프로젝트에만 존재 | `←` |
| NEWER_SOURCE | 현재 프로젝트가 최신 | `>>` |
| NEWER_TARGET | 대상 프로젝트가 최신 | `<<` |
| SAME | 동일 | `==` |

**동기화 옵션**:
| 액션 | 설명 |
|------|------|
| push | 현재 → 대상으로 복사 |
| pull | 대상 → 현재로 복사 |
| skip | 건너뛰기 |
| diff | 차이점 보기 |

## 워크플로우

```
oaissync list
    ↓
프로젝트 선택
    ↓
oaissync run [project]
    ↓
파일별 비교 결과 표시
    ↓
사용자 동기화 결정 (push/pull/skip)
    ↓
동기화 실행
    ↓
결과 리포트
```

## 설정

### 동기화 제외 대상

다음 파일/폴더는 동기화에서 제외됩니다:
- `__pycache__/`
- `*.pyc`
- `.git/`
- `tmp/`
- `data/`
- `.venv/`
- `node_modules/`
- `.claude/settings.local.json` - 프로젝트별 로컬 설정 (권한, MCP 등)

### 프로젝트별 커스텀 설정

프로젝트 루트에 `.oaissync.json`을 생성하여 설정을 커스터마이즈할 수 있습니다:

```json
{
  "include": ["v/", ".claude/", "CLAUDE.md"],
  "exclude": ["v/0_claude미사용/", "tmp/"],
  "auto_push": false,
  "confirm_overwrite": true
}
```

## 에이전트 출력 규칙

**중요**: oaissync 명령어 실행 시 다음 규칙을 준수합니다.

| 규칙 | 설명 |
|------|------|
| 스크립트 출력만 표시 | 스크립트가 출력하는 내용 그대로 표시 |
| 별도 요약 금지 | 에이전트가 임의로 요약/통계 추가하지 않음 |
| 템플릿 형식 준수 | 각 명령어별 템플릿(`v/template/oaissync_*.md`) 형식 따름 |

**이유**:
- 스크립트 출력이 이미 템플릿에 따라 완전한 정보 포함
- 프로젝트별 상세 정보가 테이블에 명확히 표시됨
- 중복 요약은 불필요한 정보 노이즈 발생

**올바른 예시**:
```
사용자: oaissync list
에이전트: [스크립트 실행 후 출력 결과만 표시]
```

**잘못된 예시**:
```
사용자: oaissync list
에이전트: [스크립트 출력]

         **요약**: Full 7개, Partial 6개...  ← 금지
```

## 서브에이전트

| 단계 | 에이전트 | 역할 | 병렬 |
|------|----------|------|:----:|
| 스캔 | Explore | 프로젝트 구조 탐색 | O |
| 동기화 | task-executor | 파일 복사/동기화 실행 | O |
| 검증 | task-checker | 동기화 결과 검증 | - |

## 관련 명령어

| 명령어 | 용도 |
|--------|------|
| `v/command/load.md` | 프로젝트 로드 |

## 관련 문서

`v/oaisstart.md` | `v/oaisenv.md` | `v/guide/common_guide.md`
