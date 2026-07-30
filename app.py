import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="CHEONGAM UNIVERSITY | REGULATION", layout="wide")

# 2. 전문적인 메뉴 및 레이아웃 CSS
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 전체 폰트 및 배경 */
    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif;
        background-color: #ffffff !important;
        color: #1a1a1a;
    }

    /* 사이드바 : 정갈한 네이비 시스템 메뉴 */
    [data-testid="stSidebar"] {
        background-color: #001529 !important;
        border-right: 1px solid #e5e7eb;
    }
    [data-testid="stSidebarNav"] {display: none;} /* 기본 메뉴 숨김 */

    /* 메뉴 아이템 스타일링 */
    .stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 4px;
        padding: 0 10px;
    }
    .stRadio label {
        padding: 12px 20px !important;
        border-radius: 4px !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        color: #a6adb4 !important;
        background-color: transparent !important;
        border: none !important;
        transition: all 0.2s;
        cursor: pointer;
    }
    /* 메뉴 호버 및 활성화 상태 */
    .stRadio label:hover {
        color: #ffffff !important;
        background-color: rgba(255,255,255,0.05) !important;
    }
    .stRadio label[data-checked="true"] {
        color: #ffffff !important;
        background-color: #1890ff !important; /* 청암 블루 포인트 */
        font-weight: 600 !important;
    }
    
    /* 사이드바 하단 관리자 메뉴용 여백 */
    .sidebar-footer {
        position: fixed;
        bottom: 20px;
        width: 260px;
        padding: 0 20px;
    }

    /* 메인 콘텐츠 영역 밸런스 */
    .main .block-container {
        max-width: 1400px;
        padding: 3rem 4rem;
    }

    /* 편(Part) 구분선 및 제목 */
    .part-divider {
        font-size: 0.8rem;
        font-weight: 700;
        color: #8c8c8c;
        margin-top: 30px;
        margin-bottom: 10px;
        padding-bottom: 5px;
        border-bottom: 1px solid #f0f0f0;
        letter-spacing: 0.05em;
    }

    /* 규정 리스트 버튼 (투명 배경) */
    .stButton > button {
        text-align: left;
        background-color: transparent;
        border: none;
        color: #434343;
        padding: 8px 0;
        font-size: 0.95rem;
        transition: 0.2s;
    }
    .stButton > button:hover {
        color: #1890ff;
        padding-left: 5px;
        background-color: transparent;
    }

    /* 본문 뷰어 */
    .document-box {
        background-color: #ffffff;
        border: 1px solid #d9d9d9;
        border-radius: 2px;
        padding: 40px;
        min-height: 800px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 로드 (8개 편 구조)
def get_regulation_data():
    raw = [
        ["제 1 편 학교법인", "학교법인 청암학원 정관", "1-1.txt"],
        ["제 1 편 학교법인", "청암대학교 산학협력단 법인정관", "1-2.txt"],
        ["제 2 편 학 칙", "학 칙", "2-1.txt"],
        ["제 2 편 학 칙", "학사내규", "2-2.txt"],
        ["제 3 편 기획 및 교원인사", "감사 규정", "3-1.txt"],
        ["제 3 편 기획 및 교원인사", "교원인사 규정", "3-5.txt"],
        ["제 5 편 학 사", "장학 규정", "5-2-5.txt"],
        ["제 6 편 일반 행정", "교직원 복무 규정", "6-1.txt"]
    ]
    return pd.DataFrame(raw, columns=["편", "규정명", "파일명"])

df = get_regulation_data()

# 4. 사이드바 (메뉴다운 메뉴)
with st.sidebar:
    st.markdown("<div style='padding: 40px 20px;'><h2 style='color:white; margin:0; font-size:1.2rem; letter-spacing:1px;'>CHEONGAM</h2><p style='color:#595959; font-size:0.75rem; margin-top:5px;'>UNIVERSITY SYSTEM</p></div>", unsafe_allow_html=True)
    
    # 상단/중단 메뉴
    main_menu = st.radio("MAIN NAV", ["규정 보기/찾기", "규정 AI 검토"], label_visibility="collapsed")
    
    # 하단 배치 (관리자 메뉴)
    st.markdown("<div style='height: 40vh;'></div>", unsafe_allow_html=True) # 여백 확보
    st.markdown("---")
    admin_nav = st.radio("ADMIN NAV", ["관리자 메뉴"], label_visibility="collapsed")

# 5. 페이지별 로직 (실제로는 main_menu와 admin_nav를 통합 관리)
current_page = admin_nav if admin_nav == "관리자 메뉴" and st.session_state.get('last_nav') == 'admin' else main_menu

# --- 메인 레이아웃 ---
if main_menu == "규정 보기/찾기":
    st.markdown("<h2 style='font-weight:700; margin-bottom:20px;'>규정 보기/찾기</h2>", unsafe_allow_html=True)
    
    # 상단 검색 바
    search_q = st.text_input("검색", placeholder="찾으시는 규정명을 입력하십시오.", label_visibility="collapsed")
    
    col_list, col_content = st.columns([0.4, 0.6], gap="large")
    
    with col_list:
        for part in df["편"].unique():
            part_df = df[df["편"] == part]
            if search_q:
                part_df = part_df[part_df["규정명"].str.contains(search_q, na=False)]
            
            if not part_df.empty:
                st.markdown(f"<div class='part-divider'>{part}</div>", unsafe_allow_html=True)
                for _, row in part_df.iterrows():
                    if st.button(row['규정명'], key=f"list_{row['규정명']}", use_container_width=True):
                        st.session_state['active_reg'] = row['규정명']
                        st.session_state['active_file'] = row['파일명']

    with col_content:
        if 'active_reg' in st.session_state:
            st.markdown(f"<div style='border-bottom: 2px solid #000; padding-bottom:10px; margin-bottom:30px;'><h3 style='margin:0;'>{st.session_state['active_reg']}</h3></div>", unsafe_allow_html=True)
            st.text_area("CONTENT", f"[{st.session_state['active_reg']}] 본문\n\n청암대학교 규정 관리 원칙에 의거하여 본 내용을 공시합니다.", height=800, label_visibility="collapsed")
        else:
            st.markdown("<div style='height:600px; display:flex; align-items:center; justify-content:center; color:#bfbfbf; border:1px solid #f0f0f0;'>좌측 리스트에서 규정을 선택하십시오.</div>", unsafe_allow_html=True)

elif main_menu == "규정 AI 검토":
    st.markdown("<h2 style='font-weight:700; margin-bottom:20px;'>규정 AI 검토</h2>", unsafe_allow_html=True)
    st.write("작성 중인 개정안이 대학 전체 규정 체계와 상충하는지 AI가 행정 검토를 수행합니다.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    draft = st.text_area("개정(안) 내용 입력", height=400, placeholder="검토가 필요한 지침이나 규정의 조항 내용을 상세히 입력하십시오.")
    
    if st.button("행정 정합성 분석 실행", use_container_width=True):
        st.info("AI 행정 전문가 모듈이 분석을 시작합니다...")
        # (기존 AI 로직 연결)

# 사이드바 최하단 '관리자 메뉴' 선택 시
if admin_nav == "관리자 메뉴":
    # (관리자 페이지 로직 별도 구현)
    pass
