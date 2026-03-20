# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-pptx",
#     "Pillow",
# ]
# ///

import os
import sys
import re
import argparse
from pathlib import Path

# Add script directory to path for local module import
_script_dir = Path(__file__).parent
if str(_script_dir) not in sys.path:
    sys.path.insert(0, str(_script_dir))

from oaisppt_pptx import OAISPresentation


# Maximum file size limit (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024


# Function to parse test.md and extract sections

def parse_test_md(file_path):
    # Check file size before reading
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        raise ValueError(f"File too large: {file_size} bytes (max: {MAX_FILE_SIZE} bytes)")

    with open(file_path, 'r', encoding='utf-8') as f:

        content = f.read()



    sections = re.split(r'^\* \[([^\]]+)\]', content, flags=re.MULTILINE)

    sections = [s.strip() for s in sections if s.strip()]



    parsed_sections = {}

    for i in range(1, len(sections), 2):

        title = sections[i]

        body = sections[i+1] if i+1 < len(sections) else ""

        parsed_sections[title] = body



    return parsed_sections



def main(input_md_path, output_pptx_path):

    # Load test.md content

    sections = parse_test_md(input_md_path)



    pres = OAISPresentation()



    # 1. Cover

    pres.add_cover_slide(

        title="Vibe 개발 메모 & 명령어",

        subtitle="실전 개발자를 위한 실용 노트",

        description="test.md의 내용을 기반으로 자동 생성된 PPT",

        badge_text="AUTO GENERATED",

        footer_items=[

            {"label": "Source", "value": "test.md"},

            {"label": "Date", "value": "2025"}

        ]

    )



    # 2. About

    pres.add_about_slide(

        icon="📄",

        name="Test.md Summary",

        subtitle="자동 파싱된 내용",

        badge_text="OVERVIEW",

        headline="test.md 파일의 주요 섹션을 슬라이드로 변환",

        description=f"총 {len(sections)}개의 섹션이 파싱되었습니다.",

        stats=[

            {"value": str(len(sections)), "label": "섹션"},

            {"value": "자동", "label": "생성"},

            {"value": "OAIS", "label": "스타일"}

        ]

    )



    # Dynamically add slides based on sections

    for title, body in list(sections.items())[:6]:  # Limit to 6 sections for demo

        if 'Emacs' in title:

            pres.add_features_slide(

                badge_text="EMACS",

                subtitle=title,

                features=[

                    {"title": "단축키", "desc": body[:100] + "..." if len(body) > 100 else body},

                    {"title": "기능", "desc": "Emacs 주요 기능 설명"},

                    {"title": "팁", "desc": "편집 팁"}

                ],

                quote="Emacs는 OS다.",

                quote_author="Emacs User"

            )

        elif 'screen' in title.lower():

            pres.add_features_slide(

                badge_text="SCREEN",

                subtitle=title,

                features=[

                    {"title": "관리", "desc": body[:100] + "..." if len(body) > 100 else body},

                    {"title": "명령어", "desc": "screen 명령어 모음"}

                ],

                quote="멀티태스킹의 핵심",

                quote_author="Terminal User"

            )

        elif 'jupyter' in title.lower():

            pres.add_features_slide(

                badge_text="JUPYTER",

                subtitle=title,

                features=[

                    {"title": "단축키", "desc": body[:100] + "..." if len(body) > 100 else body},

                    {"title": "매직", "desc": "Jupyter 매직 명령어"}

                ],

                quote="데이터 과학의 필수 도구",

                quote_author="Data Scientist"

            )

        else:

            pres.add_features_slide(

                badge_text=title[:10].upper(),

                subtitle=title,

                features=[

                    {"title": "내용", "desc": body[:200] + "..." if len(body) > 200 else body}

                ],

                quote="개발 메모",

                quote_author="Vibe"

            )

            

    # 3. Grid (Main Tools)

    pres.add_grid_slide(

        badge_text="TOOLS",

        subtitle="주요 개발 도구",

        cards=[

            {"icon": "🤖", "title": "Claude/Vibe", "desc": "AI 명령어 및 프로젝트 관리", "label": "AI"},

            {"icon": "🖥️", "title": "Emacs", "desc": "단축키, org-mode, 편집 팁", "label": "Editor"},

            {"icon": "💻", "title": "VSCode", "desc": "단축키, 플러그인, 코드 정리", "label": "IDE"},

            {"icon": "📊", "title": "Jupyter", "desc": "노트북, 매직커맨드, 확장", "label": "Notebook"}

        ]

    )



    # 4. Features (핵심 명령어)

    pres.add_features_slide(

        badge_text="KEY COMMANDS",

        subtitle="핵심 명령어 모음",

        features=[

            {"title": "Claude MCP", "desc": "claude mcp add --transport http playwright ..."},

            {"title": "Screen 관리", "desc": "screen -r, screen -S, screen -ls, C-a d"},

            {"title": "Emacs 빈줄삭제", "desc": "M-x flush-lines ^$"},

            {"title": "VSCode 전체접기", "desc": "C-k C-0"}

        ],

        quote="생산성은 작은 습관에서 시작된다.",

        quote_author="Vibe Developer"

    )



    # 5. Tips (실전 팁)

    pres.add_tips_slide(

        badge_text="TIPS",

        subtitle="실전 개발 팁",

        tips=[

            {"icon": "🔍", "title": "파일 수 카운트", "desc": "find . -type f | wc -l"},

            {"icon": "⚡", "title": "GPU 모니터링", "desc": "watch -n 1 -d nvidia-smi"},

            {"icon": "📝", "title": "Emacs org block", "desc": "C-c C-,"}

        ]

    )



    # 6. Closing

    pres.add_closing_slide(

        title="감사합니다",

        subtitle="Vibe 개발 노트",

        badge_text="THANK YOU",

        footer_items=[

            {"label": "문의", "value": "oais7koo"},

            {"label": "정리일", "value": "2025-12-24"}

        ],

        closing_text="Happy Coding!"

    )





    pres.save(output_pptx_path)

    print(f"Presentation saved to: {output_pptx_path}")



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate a PowerPoint presentation from a Markdown file.")

    parser.add_argument("input_md", help="Path to the input Markdown file (e.g., src/test.md).")

    parser.add_argument("-o", "--output", default="vibe_presentation.pptx",

                        help="Output PowerPoint file name (default: vibe_presentation.pptx).")

    args = parser.parse_args()

    

    main(args.input_md, args.output)