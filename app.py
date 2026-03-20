"""
OCR 성능 비교 대시보드 - 커스텀 라우터
version: 2.4.0
"""

import streamlit as st
from src.td3000_styles import inject_css

st.set_page_config(
    page_title="OCR Compare",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="auto",
)

inject_css()

NAV_LABELS = ["대시보드", "OCR 테스트", "배치 테스트", "전처리 상세", "결과 분석"]

PAGES = {
    "대시보드":    "pages/home.py",
    "OCR 테스트":  "pages/ocr_test.py",
    "배치 테스트": "pages/batch_test.py",
    "전처리 상세": "pages/preprocessing.py",
    "결과 분석":   "pages/results.py",
}

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "대시보드"

# 쿼리 파라미터 처리
if "nav" in st.query_params:
    nav_target = st.query_params["nav"]
    if nav_target in PAGES:
        st.session_state["current_page"] = nav_target
    del st.query_params["nav"]
    st.rerun()

# 사이드바
with st.sidebar:
    # 활성 버튼 강조 CSS (nth-child로 정확히 타겟팅)
    # 구조: [1] 이 CSS 마크다운 [2] 로고 마크다운 [3~7] 버튼 [8] 버전 바
    active_idx = NAV_LABELS.index(st.session_state["current_page"])
    active_nth = active_idx + 3  # 1-indexed + CSS markdown(1) + logo(1)
    st.markdown(f"""
    <style>
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"]
      > [data-testid="stElementContainer"]:nth-child({active_nth})
      [data-testid="stButton"] > button {{
        background: #227fcd !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"]
      > [data-testid="stElementContainer"]:nth-child({active_nth})
      [data-testid="stButton"] > button:hover {{
        background: #1a6bb5 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # 로고
    st.markdown("""
    <div style="padding:20px 20px 16px 20px;border-bottom:1px solid #243f5e;margin-bottom:8px;">
        <div style="font-size:16px;font-weight:700;color:#ffffff;letter-spacing:0.5px;">🔍 OCR Compare</div>
        <div style="font-size:11px;color:#64748b;margin-top:2px;">성능 비교 대시보드</div>
    </div>
    """, unsafe_allow_html=True)

    # 네비게이션 버튼
    for label in NAV_LABELS:
        if st.button(label, key=f"nav_{label}", use_container_width=True):
            st.session_state["current_page"] = label
            st.rerun()

    # 버전 바
    st.markdown("""
    <div style="border-top:1px solid #243f5e;margin-top:12px;padding:12px 20px;
                display:flex;align-items:center;gap:8px;">
        <div style="width:8px;height:8px;border-radius:50%;background:#22c55e;flex-shrink:0;"></div>
        <span style="color:#64748b;font-size:12px;">v0.1.0</span>
    </div>
    """, unsafe_allow_html=True)

# 현재 페이지 렌더링
current = st.session_state["current_page"]
page_file = PAGES.get(current)

if page_file:
    import importlib.util
    spec = importlib.util.spec_from_file_location("_page", page_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.render()
