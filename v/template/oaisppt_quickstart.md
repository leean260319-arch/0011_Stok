# PPT 생성 빠른 시작 템플릿

> 중앙 안내: 상세한 에이전트 활용 원칙 및 공통 가이드라인은 `v/guide/common_guide.md`의 '2. 에이전트 활용 원칙' 섹션을 참조하십시오.

## 템플릿 설명

이 템플릿은 OAIS 스타일 PPT를 생성하는 기본 코드 구조를 제공합니다.
프로젝트별로 슬라이드 내용과 파일명을 커스터마이즈하여 사용하세요.

## 기본 코드 템플릿

```python
import sys
sys.path.insert(0, 'v/script')
from oaisppt_pptx import OAISPresentation

pres = OAISPresentation()

# 1. 커버 슬라이드
pres.add_cover_slide(
    title="[프레젠테이션 제목]",
    subtitle="[부제목]",
    description="[설명]",
    badge_text="[배지 텍스트]",
    footer_items=[
        {"label": "Topic", "value": "[토픽]"},
        {"label": "Date", "value": "[날짜]"}
    ]
)

# 2. 소개 슬라이드
pres.add_about_slide(
    icon="[아이콘]",
    name="[이름]",
    subtitle="[부제목]",
    badge_text="OVERVIEW",
    headline="[헤드라인]",
    description="[설명]",
    stats=[
        {"value": "[값1]", "label": "[레이블1]"},
        {"value": "[값2]", "label": "[레이블2]"},
        {"value": "[값3]", "label": "[레이블3]"}
    ]
)

# 3. 그리드 슬라이드 (선택사항)
pres.add_grid_slide(
    badge_text="[섹션명]",
    subtitle="[서브타이틀]",
    cards=[
        {"icon": "[아이콘1]", "title": "[제목1]", "desc": "[설명1]", "label": "[레이블1]"},
        {"icon": "[아이콘2]", "title": "[제목2]", "desc": "[설명2]", "label": "[레이블2]"},
        # 추가 카드...
    ]
)

# 4. 기능 슬라이드 (선택사항)
pres.add_features_slide(
    badge_text="[배지]",
    subtitle="[서브타이틀]",
    features=[
        {"title": "[기능1]", "desc": "[설명1]"},
        {"title": "[기능2]", "desc": "[설명2]"},
        # 추가 기능...
    ],
    quote="[인용구]",
    quote_author="[저자]"
)

# 5. 팁 슬라이드 (선택사항)
pres.add_tips_slide(
    badge_text="[배지]",
    subtitle="[서브타이틀]",
    tips=[
        {"icon": "[아이콘1]", "title": "[팁1]", "desc": "[설명1]"},
        {"icon": "[아이콘2]", "title": "[팁2]", "desc": "[설명2]"},
        # 추가 팁...
    ]
)

# 6. 마무리 슬라이드
pres.add_closing_slide(
    title="감사합니다",
    subtitle="[마무리 부제목]",
    badge_text="THANK YOU",
    footer_items=[
        {"label": "Contact", "value": "[연락처]"},
        {"label": "Date", "value": "[날짜]"}
    ],
    closing_text="[마무리 문구]"
)

pres.save("[출력파일명].pptx")
```

## 커스터마이즈 예시

프로젝트별로 다음 요소들을 변경:

- 슬라이드 제목과 내용
- 아이콘과 이미지
- 색상과 스타일
- 슬라이드 순서와 개수
