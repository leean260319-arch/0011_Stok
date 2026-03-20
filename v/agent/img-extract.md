# 고급 디자인 시스템 추출 가이드

## 목표
업로드된 이미지에서 포괄적이고 재사용 가능한 디자인 시스템을 추출하여, 개발자나 AI 시스템이 일관된 UI 개발의 스타일링 기반으로 사용할 수 있는 JSON 참조 자료를 생성한다.

## 분석 대상
**INPUT:** 업로드된 UI 이미지/스크린샷
**OUTPUT:** `designs/design.json` 파일

## 전문적 분석 프로세스

### 1단계: 이미지 사전 분석
**시각적 구조 파악**
- **전체 레이아웃 구조** 분석 (헤더, 네비게이션, 콘텐츠 영역, 사이드바, 푸터)
- **정보 계층 구조** 식별 (주요-보조-세부 정보)
- **시각적 그리드 시스템** 감지 (컬럼, 행, 간격 패턴)
- **반복되는 UI 패턴** 추출 (카드, 리스트, 버튼 그룹)
- **브랜드 아이덴티티 요소** 파악 (로고 스타일, 브랜드 색상)

**기술적 구현 추론**
- **CSS 프레임워크 추정** (Bootstrap, Tailwind, Material Design 등)
- **컴포넌트 라이브러리 스타일** 감지
- **반응형 디자인 특성** 분석
- **접근성 고려사항** 식별

### 2단계: 디자인 토큰 체계적 추출

#### A. 색상 시스템 (Color System)
**기본 색상 팔레트**
```json
{
  "colors": {
    "primary": {
      "50": "#...",
      "100": "#...",
      "500": "#...",  // 기본 색상
      "900": "#..."
    },
    "secondary": { "..." },
    "neutral": {
      "white": "#ffffff",
      "gray-50": "#...",
      "gray-900": "#...",
      "black": "#000000"
    }
  }
}
```

**의미적 색상 (Semantic Colors)**
- **상태 색상:** success, warning, error, info
- **기능 색상:** background, surface, border, text
- **인터랙션 색상:** hover, active, focus, disabled

**색상 추출 방법론**
1. **주요 색상 식별:** 브랜드 컬러, 액센트 컬러
2. **색상 변형 계산:** 명도/채도 조절을 통한 팔레트 생성
3. **대비율 검증:** WCAG 접근성 기준 확인
4. **사용 맥락 분류:** 텍스트용, 배경용, 강조용

#### B. 타이포그래피 시스템 (Typography)
**폰트 계층 구조**
```json
{
  "typography": {
    "fontFamily": {
      "primary": ["Inter", "system-ui", "sans-serif"],
      "secondary": ["Georgia", "serif"],
      "mono": ["JetBrains Mono", "monospace"]
    },
    "fontSize": {
      "xs": "0.75rem",    // 12px
      "sm": "0.875rem",   // 14px
      "base": "1rem",     // 16px
      "lg": "1.125rem",   // 18px
      "xl": "1.25rem",    // 20px
      "2xl": "1.5rem",    // 24px
      "3xl": "1.875rem",  // 30px
      "4xl": "2.25rem"    // 36px
    },
    "fontWeight": {
      "light": 300,
      "regular": 400,
      "medium": 500,
      "semibold": 600,
      "bold": 700
    },
    "lineHeight": {
      "tight": 1.25,
      "normal": 1.5,
      "relaxed": 1.75
    },
    "letterSpacing": {
      "tight": "-0.025em",
      "normal": "0",
      "wide": "0.025em"
    }
  }
}
```

**텍스트 스타일 프리셋**
- **제목 계층:** h1, h2, h3, h4, h5, h6
- **본문 텍스트:** body-large, body, body-small
- **특수 텍스트:** caption, overline, button-text

#### C. 간격 시스템 (Spacing System)
**기본 간격 단위**
```json
{
  "spacing": {
    "base": "0.25rem",  // 4px
    "scale": {
      "0": "0",
      "1": "0.25rem",   // 4px
      "2": "0.5rem",    // 8px
      "3": "0.75rem",   // 12px
      "4": "1rem",      // 16px
      "5": "1.25rem",   // 20px
      "6": "1.5rem",    // 24px
      "8": "2rem",      // 32px
      "10": "2.5rem",   // 40px
      "12": "3rem",     // 48px
      "16": "4rem",     // 64px
      "20": "5rem",     // 80px
      "24": "6rem"      // 96px
    }
  }
}
```

**컴포넌트별 간격 규칙**
- **패딩:** 내부 여백 표준
- **마진:** 외부 여백 표준
- **갭:** 플렉스/그리드 간격

#### D. 레이아웃 시스템 (Layout System)
**그리드 시스템**
```json
{
  "layout": {
    "breakpoints": {
      "sm": "640px",
      "md": "768px",
      "lg": "1024px",
      "xl": "1280px",
      "2xl": "1536px"
    },
    "container": {
      "maxWidth": {
        "sm": "640px",
        "md": "768px",
        "lg": "1024px",
        "xl": "1280px",
        "2xl": "1536px"
      },
      "padding": "1rem"
    },
    "grid": {
      "columns": 12,
      "gap": "1.5rem"
    }
  }
}
```

**구조적 요소**
- **컨테이너:** 최대 너비, 중앙 정렬
- **섹션:** 주요 콘텐츠 블록
- **카드:** 콘텐츠 그룹핑 요소

#### E. 컴포넌트 시스템 (Component System)
**버튼 시스템**
```json
{
  "components": {
    "button": {
      "base": {
        "fontSize": "1rem",
        "fontWeight": 500,
        "lineHeight": 1.5,
        "borderRadius": "0.375rem",
        "borderWidth": "1px",
        "cursor": "pointer",
        "transition": "all 0.2s"
      },
      "sizes": {
        "sm": {
          "padding": "0.5rem 0.75rem",
          "fontSize": "0.875rem"
        },
        "md": {
          "padding": "0.625rem 1rem",
          "fontSize": "1rem"
        },
        "lg": {
          "padding": "0.75rem 1.25rem",
          "fontSize": "1.125rem"
        }
      },
      "variants": {
        "primary": {
          "backgroundColor": "var(--color-primary-500)",
          "color": "white",
          "borderColor": "var(--color-primary-500)"
        },
        "secondary": {
          "backgroundColor": "transparent",
          "color": "var(--color-primary-500)",
          "borderColor": "var(--color-primary-500)"
        },
        "ghost": {
          "backgroundColor": "transparent",
          "color": "var(--color-gray-700)",
          "borderColor": "transparent"
        }
      },
      "states": {
        "hover": {
          "transform": "translateY(-1px)",
          "boxShadow": "0 4px 12px rgba(0,0,0,0.15)"
        },
        "active": {
          "transform": "translateY(0)"
        },
        "disabled": {
          "opacity": 0.5,
          "cursor": "not-allowed"
        }
      }
    }
  }
}
```

#### F. 시각적 효과 (Visual Effects)
**그림자 시스템**
```json
{
  "effects": {
    "boxShadow": {
      "none": "none",
      "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
      "base": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
      "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
      "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
      "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)"
    },
    "borderRadius": {
      "none": "0",
      "sm": "0.125rem",
      "base": "0.25rem",
      "md": "0.375rem",
      "lg": "0.5rem",
      "xl": "0.75rem",
      "2xl": "1rem",
      "full": "9999px"
    },
    "opacity": {
      "0": "0",
      "25": "0.25",
      "50": "0.5",
      "75": "0.75",
      "100": "1"
    }
  }
}
```

### 3단계: 고급 분석 기법

#### AI 기반 색상 추출
```javascript
// 이미지에서 주요 색상 자동 추출
const extractDominantColors = (image) => {
  // Canvas API를 사용한 픽셀 분석
  // K-means 클러스터링으로 주요 색상 그룹핑
  // HSL 색상 공간에서 조화로운 팔레트 생성
};
```

#### 패턴 인식 알고리즘
- **반복 요소 감지:** 버튼, 카드, 아이콘 패턴
- **간격 패턴 분석:** 일관된 여백 규칙 추출
- **타이포그래피 계층:** 폰트 크기와 굵기 관계 분석

#### 접근성 자동 검증
- **색상 대비율 계산:** WCAG AA/AAA 기준 검증
- **텍스트 가독성 분석:** 폰트 크기와 줄 간격 최적화
- **터치 타겟 크기:** 모바일 접근성 고려

### 4단계: JSON 구조 최적화

#### 개발자 친화적 구조
```json
{
  "designSystem": {
    "meta": {
      "name": "추출된 디자인 시스템",
      "version": "1.0.0",
      "extractedFrom": "이미지 파일명",
      "extractedDate": "2024-01-01",
      "framework": "framework-agnostic"
    },
    "tokens": {
      "colors": { "..." },
      "typography": { "..." },
      "spacing": { "..." },
      "layout": { "..." },
      "effects": { "..." }
    },
    "components": {
      "button": { "..." },
      "input": { "..." },
      "card": { "..." },
      "navigation": { "..." }
    },
    "patterns": {
      "layouts": { "..." },
      "compositions": { "..." }
    }
  }
}
```

#### CSS 변수 생성
```css
/* 자동 생성된 CSS 변수 */
:root {
  /* Colors */
  --color-primary-50: #eff6ff;
  --color-primary-500: #3b82f6;
  --color-primary-900: #1e3a8a;

  /* Typography */
  --font-family-primary: Inter, system-ui, sans-serif;
  --font-size-base: 1rem;
  --font-weight-medium: 500;

  /* Spacing */
  --spacing-1: 0.25rem;
  --spacing-4: 1rem;
  --spacing-8: 2rem;

  /* Effects */
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --radius-md: 0.375rem;
}
```

### 5단계: 품질 보증 및 검증

#### 자동 검증 체크리스트
- [ ] **색상 접근성:** 모든 색상 조합이 WCAG 기준 충족
- [ ] **일관성 검사:** 유사한 요소들의 스타일 일관성
- [ ] **확장성 검증:** 새로운 컴포넌트 추가 시 호환성
- [ ] **프레임워크 독립성:** 모든 주요 CSS 프레임워크에서 사용 가능
- [ ] **반응형 적합성:** 다양한 화면 크기에서 적용 가능

#### 수동 검토 포인트
- [ ] **브랜드 일관성:** 추출된 요소가 브랜드 아이덴티티 반영
- [ ] **사용성 고려:** 실제 사용 시나리오에서의 적합성
- [ ] **현대적 표준:** 최신 디자인 트렌드와 모범 사례 준수
- [ ] **문서화 품질:** 개발자가 쉽게 이해하고 적용 가능

### 6단계: 출력 형식 다양화

#### 다중 포맷 출력
```bash
designs/
├── design.json           # 기본 JSON 형식
├── design.css           # CSS 변수 버전
├── design.scss          # Sass 변수 버전
├── design.js            # JavaScript 객체 버전
├── tokens.json          # Design Tokens 표준 형식
└── figma-tokens.json    # Figma Tokens 플러그인 형식
```

#### 프레임워크별 변환
- **Tailwind CSS:** `tailwind.config.js` 생성
- **Material-UI:** `theme.js` 파일 생성
- **Styled Components:** 테마 객체 생성
- **CSS-in-JS:** 각 라이브러리별 형식 제공

### 7단계: 지속적 개선 시스템

#### 버전 관리
```json
{
  "version": "1.2.0",
  "changelog": [
    {
      "version": "1.2.0",
      "date": "2024-01-15",
      "changes": [
        "새로운 색상 팔레트 추가",
        "타이포그래피 스케일 개선",
        "접근성 대비율 최적화"
      ]
    }
  ]
}
```

#### 사용 통계 및 피드백
- **인기 컴포넌트 추적:** 가장 많이 사용되는 디자인 토큰
- **오류 보고 시스템:** 개발자 피드백 수집
- **자동 업데이트 제안:** 새로운 이미지 분석 시 개선 사항 제안

### 8단계: 문서화 및 가이드라인

#### 사용 가이드 생성
```markdown
# 디자인 시스템 사용 가이드

## 빠른 시작
1. `design.json` 파일을 프로젝트에 복사
2. CSS 변수를 HTML에 포함
3. 컴포넌트 스타일 적용

## 색상 사용법
- 주요 액션: `var(--color-primary-500)`
- 텍스트: `var(--color-gray-900)`
- 배경: `var(--color-gray-50)`

## 컴포넌트 예제
...
```

#### 라이브 스타일가이드 생성
- **Storybook 통합:** 컴포넌트 미리보기
- **패턴 라이브러리:** 사용 예제와 코드 스니펫
- **접근성 가이드:** 올바른 사용법과 주의사항
