# v/command - 통합 명령어 디렉토리

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v02 | 2025-12-25 | oaiscommand command 서브명령어 반영 |
| v01 | 2025-12-25 | 최초 생성 (F016 Command 통합 체계화) |

---

## 1. 개요

이 디렉토리는 `.gemini/commands/sg/`와 `.claude/commands/sc/`의 명령어를 통합 관리합니다.

**핵심 목적:**
- SuperGemini (sg) / SuperClaude (sc) 명령어 통합
- 일관된 명령어 문서 형식 제공
- oaiscommand 스킬과 연동

**관련 문서:**
- `v/oaiscommand.md` - 명령어 관리 스킬
- `doc/d0007_command.md` - 명령어 집계 문서
- `.claude/COMMANDS.md` - SuperClaude 명령어 프레임워크

---

## 2. 명령어 목록

| 명령어 | 용도 | 원본 |
|--------|------|------|
| [analyze](analyze.md) | 코드 분석 (품질/보안/성능/아키텍처) | sg+sc |
| [build](build.md) | 프로젝트 빌드 | sg+sc |
| [cleanup](cleanup.md) | 프로젝트 정리, 기술 부채 감소 | sg+sc |
| [design](design.md) | 설계 오케스트레이션 | sg+sc |
| [document](document.md) | 문서화 생성 | sg+sc |
| [estimate](estimate.md) | 증거 기반 추정 | sg+sc |
| [explain](explain.md) | 교육적 설명 | sg+sc |
| [git](git.md) | Git 워크플로우 | sg+sc |
| [implement](implement.md) | 기능 구현 | sg+sc |
| [improve](improve.md) | 증거 기반 코드 개선 | sg+sc |
| [index](index.md) | 명령어 카탈로그 브라우징 | sg+sc |
| [load](load.md) | 프로젝트 컨텍스트 로딩 | sg+sc |
| [spawn](spawn.md) | 태스크 오케스트레이션 | sg+sc |
| [task](task.md) | 장기 프로젝트 관리 | sg+sc |
| [test](test.md) | 테스팅 워크플로우 | sg+sc |
| [troubleshoot](troubleshoot.md) | 문제 조사 | sg+sc |
| [workflow](workflow.md) | 워크플로우 생성 | sg+sc |

**총 17개 통합 명령어**

---

## 3. 명령어 문서 형식

각 명령어 문서는 다음 구조를 따릅니다:

```markdown
# [명령어명] - [제목]

## 문서 이력 관리
| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v01 | YYYY-MM-DD | 최초 생성 (sg/sc 통합) |

---

## 1. 개요
[명령어 용도 설명]

## 2. 사용법
```
[명령어] [인자] [옵션]
```

## 3. 인자 및 옵션
| 인자/옵션 | 설명 |
|-----------|------|
| ... | ... |

## 4. 실행 단계
1. ...
2. ...

## 5. 도구 연동
### Claude
- **allowed-tools**: [도구 목록]

### Gemini
- **MCP 플래그**: --seq, --c7, --magic

## 6. 예시
...

## 7. 관련 명령어/스킬
- [관련 항목]
```

---

## 4. 카테고리

### 4.1 개발 (Development)
- build, implement, design

### 4.2 분석 (Analysis)
- analyze, troubleshoot, explain

### 4.3 품질 (Quality)
- improve, cleanup

### 4.4 테스트 (Testing)
- test

### 4.5 문서화 (Documentation)
- document

### 4.6 버전 관리 (Version Control)
- git

### 4.7 계획 (Planning)
- workflow, estimate, task

### 4.8 메타 및 오케스트레이션 (Meta & Orchestration)
- index, load, spawn

---

## 5. oais 스킬과의 관계

| 통합 명령어 | 관련 oais 스킬 | 차이점 |
|------------|---------------|--------|
| analyze | oaischeck | analyze는 범용, oaischeck는 프로젝트 특화 |
| test | oaistest | test는 범용, oaistest는 프로젝트 특화 |
| implement | oaisfix | implement는 신규 구현, oaisfix는 수정 |
| document | oaisdoc | 유사 기능, oaisdoc은 프로젝트 문서 관리 |
| git | oaiscommit | git은 범용, oaiscommit는 커밋+이력 통합 |
| workflow | oaisbatch | workflow는 범용, oaisbatch는 전체 파이프라인 배치 실행 |

---

## 6. 사용 방법

### 6.1 직접 참조
```
v/command/analyze.md 참조하여 analyze 명령어 사용
```

### 6.2 oaiscommand 스킬 활용
```bash
oaiscommand command           # v/command 스캔 → d0007 섹션 4 갱신
oaiscommand list              # 통합 명령어 목록
oaiscommand sync              # 외부 명령어 동기화
oaiscommand compare           # 소스 간 비교
```

---

## 7. 동기화 정보

**마지막 동기화**: 2025-12-25
**소스 디렉토리**:
- `.gemini/commands/sg/` (18 파일)
- `.claude/commands/sc/` (17 파일)

**제외된 명령어**:
- `oaischeck.toml` (Gemini) - oais 스킬과 이름 충돌

---
