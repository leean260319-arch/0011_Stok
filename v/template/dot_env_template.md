# .env 환경변수 템플릿

## 사용법

1. 이 템플릿을 복사하여 프로젝트 루트에 `.env` 파일 생성
2. 실제 값으로 교체
3. `.gitignore`에 `.env` 추가 확인

## 참조 .env 경로

> **공통 환경변수**: `d:\3_code\0003_CCone\.env`

프로젝트 간 환경변수 공유 시 위 파일을 참조합니다.

---

## 환경변수 템플릿

```env
# ============================================================================
# 환경 설정
# ============================================================================
ENVIRONMENT=development          # development | staging | production
DEBUG_MODE=true                  # true | false

# ============================================================================
# 테스트 로그인 설정
# ============================================================================
# 테스트 계정 정보 (테스트 로그인 버튼 및 자동 로그인에서 사용)
TEST_USER_ID={테스트_유저_ID}
TEST_USER_PASSWORD={테스트_비밀번호}

# 테스트 로그인 버튼 표시 여부 (로그인 화면에서 "테스트 로그인" 버튼)
ENABLE_TEST_LOGIN=true           # true: 개발환경 | false: 운영환경

# 자동 로그인 활성화 (페이지 로드 시 자동으로 로그인 처리)
ENABLE_AUTO_LOGIN=true           # true: 자동 로그인 | false: 수동 로그인

# ============================================================================
# 외부 API 설정
# ============================================================================
# Hyphen API (법인상태확인)
HYPHEN_API_KEY={API_KEY}
HYPHEN_USER_ID={USER_ID}

# ============================================================================
# 데이터베이스 설정 (해당 시)
# ============================================================================
# DATABASE_URL=sqlite:///db/app.db
# DATABASE_URL=postgresql://user:pass@host:5432/dbname

# ============================================================================
# OpenAI API (해당 시)
# ============================================================================
# OPENAI_API_KEY={OPENAI_API_KEY}
```

---

## 환경별 설정 가이드

| 환경 | ENVIRONMENT | DEBUG_MODE | ENABLE_TEST_LOGIN | ENABLE_AUTO_LOGIN |
|------|-------------|------------|-------------------|-------------------|
| 개발 | development | true | true | true |
| 스테이징 | staging | false | true | false |
| 운영 | production | false | false | false |

## 보안 주의사항

- `.env` 파일은 **절대 Git에 커밋하지 마세요**
- 운영 환경에서는 `ENABLE_TEST_LOGIN=false` 필수
- 민감한 API 키는 환경변수 또는 시크릿 매니저 사용
- 테스트 계정 정보는 운영에서 비워두기

## Python에서 로드

```python
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# 또는 외부 프로젝트 .env 참조
load_dotenv("d:/3_code/0003_CCone/.env")

# 환경변수 사용
env = os.getenv("ENVIRONMENT", "development")
debug = os.getenv("DEBUG_MODE", "false").lower() == "true"
```
