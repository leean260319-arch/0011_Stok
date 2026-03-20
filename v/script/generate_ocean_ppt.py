# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-pptx",
#     "Pillow",
# ]
# ///

import os
import sys
from pathlib import Path

# Add script directory to path for local module import
_script_dir = Path(__file__).parent
if str(_script_dir) not in sys.path:
    sys.path.insert(0, str(_script_dir))

from oaisppt_pptx import OAISPresentation

def main():
    pres = OAISPresentation()

    # 1. Cover
    pres.add_cover_slide(
        title="신비로운 바다",
        subtitle="지구의 푸른 심장",
        description="우리의 생명을 지탱하고 지구를 조절하는 거대한 바다에 대한 탐험",
        badge_text="THE OCEAN",
        footer_items=[
            {"label": "Topic", "value": "Nature"},
            {"label": "Date", "value": "2025"}
        ]
    )

    # 2. About
    pres.add_about_slide(
        icon="🌊",
        name="The Ocean",
        subtitle="Earth's Life Support",
        badge_text="OVERVIEW",
        headline="지구 표면의 70%를 덮고 있는 생명의 근원",
        description="바다는 기후를 조절하고, 산소를 공급하며, 수많은 생명체의 보금자리입니다. 우리는 바다에 대해 아직도 모르는 것이 많습니다.",
        stats=[
            {"value": "71%", "label": "지구 표면적"},
            {"value": "97%", "label": "지구의 물"},
            {"value": "23만", "label": "알려진 종"}
        ]
    )

    # 3. Grid (Marine Zones or Groups)
    pres.add_grid_slide(
        badge_text="ZONES",
        subtitle="바다의 깊이별 구역",
        cards=[
            {"icon": "☀️", "title": "표해수층 (Epipelagic)", "desc": "햇빛이 닿는 200m까지의 구간, 광합성 가능", "label": "0-200m"},
            {"icon": "🌑", "title": "중심해층 (Mesopelagic)", "desc": "약한 빛만 도달하는 200~1000m 구간", "label": "200-1000m"},
            {"icon": "🔦", "title": "점심해층 (Bathypelagic)", "desc": "빛이 없는 1000~4000m 어둠의 구간", "label": "1000-4000m"},
            {"icon": "🕳️", "title": "심해저 (Abyssopelagic)", "desc": "바닥에 가까운 4000m 이하의 심연", "label": ">4000m"}
        ]
    )

    # 4. Features (Roles)
    pres.add_features_slide(
        badge_text="ROLES",
        subtitle="바다의 중요한 역할",
        features=[
            {"title": "기후 조절", "desc": "막대한 양의 열과 이산화탄소를 흡수하여 지구 기온을 안정화합니다."},
            {"title": "산소 생산", "desc": "해양 플랑크톤은 지구 산소의 50% 이상을 생산합니다."},
            {"title": "식량 자원", "desc": "수십억 인구에게 단백질 공급원을 제공합니다."},
            {"title": "생물 다양성", "desc": "지구상에서 가장 다양한 생태계를 유지합니다."}
        ],
        quote="우리는 바다를 보호함으로써 우리 자신을 보호합니다.",
        quote_author="Sylvia Earle"
    )

    # 5. Tips (Conservation)
    pres.add_tips_slide(
        badge_text="ACTION",
        subtitle="바다를 지키는 방법",
        tips=[
            {"icon": "🚫", "title": "플라스틱 줄이기", "desc": "일회용품 사용을 줄여 해양 오염을 방지합시다."},
            {"icon": "🐟", "title": "지속 가능 소비", "desc": "MSC 인증 수산물을 선택하여 남획을 막습니다."},
            {"icon": "👣", "title": "탄소 발자국 감소", "desc": "에너지를 절약하여 해양 산성화를 늦춥니다."}
        ]
    )

    # 6. Closing
    pres.add_closing_slide(
        title="감사합니다",
        subtitle="바다와 함께하는 미래",
        badge_text="THANK YOU",
        footer_items=[
            {"label": "Campaign", "value": "Save the Ocean"},
            {"label": "Contact", "value": "ocean@earth.com"}
        ],
        closing_text="Together for Nature"
    )

    # Save
    output_path = os.path.join(os.getcwd(), 'ocean_presentation.pptx')
    pres.save(output_path)
    print(f"Presentation saved to: {output_path}")

if __name__ == "__main__":
    main()
