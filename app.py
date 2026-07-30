import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# 1. 페이지 설정
st.set_page_config(page_title="청암대학교 규정정보시스템", layout="wide")

# 2. 고도화된 Custom CSS (디자인 핵심)
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    * { font-family: 'Pretendard', sans-serif; }
    
    .main { background-color: #f4f7f9; }

    /* 왼쪽 사이드바 디자인 */
    [data-testid="stSidebar"] {
        background-color: #002855 !important; /* 다크 네이비 */
        color: white;
        min-width: 260px;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    
    /* 사이드바 메뉴 버튼 스타일 */
    .stRadio > div { display: flex; flex-direction: column; gap: 10px; }
    .stRadio label {
        background-color: rgba(255,255,255,0.05);
        padding: 15px 20px !important;
        border-radius: 10px;
        transition: 0.3s;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .stRadio label:hover { background-color: rgba(255,255,255,0.2); }
    [data-checked="true"] { 
        background-color: #20c997 !important; /* 포인트 민트색 */
        font-weight: bold;
    }

    /* 상단 히로 섹션 스타일 (서울대 느낌) */
    .hero-section {
        background: linear-gradient(135deg, #002855 0%, #0055aa 100%);
        padding: 60px 40px;
        border-radius: 20px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    .hero-title { font-size: 42px; font-weight: 800; margin-bottom: 10px; }
    .hero-subtitle { font-size: 18px; opacity: 0.8; }

    /* 카드형 컨텐츠 영역 */
    .content-card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* 버튼 스타일 개편 */
    .stButton>button {
        background-color: #20c997;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 세션 상태 관리 (로그인 등)
if 'admin_mode' not in st.session_state:
    st.session_state['admin_mode'] = False

# 4. 데이터 로드
@st.cache_data
def load_data():
    return pd.read_excel("data.xlsx")

df = load_data()

# AI 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')

# --- 사이드바 구성 ---
with st.sidebar:
    st.markdown("<div style='padding: 20px 0; text-align: center;'><h2 style='color:white;'>🏛️ CHUNGAM</h2><p style='opacity:0.6;'>Regulation System</p></div>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("MENU", ["🏠 홈 / 규정 검색", "⚖️ AI 상충 검토", "🔐 관리자 패널"], label_visibility="collapsed")
    
    st.markdown("---")
    if st.session_state['admin_mode']:
        st.write("👤 관리자 접속 중")
        if st.button("로그아웃"):
            st.session_state['admin_mode'] = False
            st.rerun()

# --- 메인 페이지 로직 ---

# 1. 홈 / 규정 검색 페이지
if menu == "🏠 홈 / 규정 검색":
    # 히로 섹션
    st.markdown("""
        <div class="hero-section">
            <div class="hero-title">청암대학교 학칙 및 규정</div>
            <div class="hero-subtitle">본 시스템을 통해 학교의 모든 학칙, 규정 및 부서별 지침을 통합 검색할 수 있습니다.</div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([0.4, 0.6])
    
    with col1:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.subheader("🔍 통합 검색")
        q = st.text_input("규정명 또는 키워드를 입력하세요", placeholder="예: 장학, 복무, 교직원")
        
        dept = st.selectbox("부서 필터", ["전체"] + list(df["관리부서"].unique()))
        
        filtered = df.copy()
        if q: filtered = filtered[filtered["규정명"].str.contains(q, na=False)]
        if dept != "전체": filtered = filtered[filtered["관리부서"] == dept]
        
        selected = st.selectbox(f"검색 결과 ({len(filtered)}건)", filtered["규정명"].tolist())
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if selected:
            st.markdown("<div class='content-card'>", unsafe_allow_html=True)
            st.subheader(f"📄 {selected}")
            file_name = df[df["규정명"] == selected]["파일명"].values[0]
            if pd.notna(file_name):
                try:
                    with open(f"docs/{file_name}", "r", encoding="utf-8") as f:
                        st.text_area("규정 본문", f.read(), height=550)
                except: st.error("파일을 읽을 수 없습니다.")
            st.markdown("</div>", unsafe_allow_html=True)

# 2. AI 상충 검토 페이지
elif menu == "⚖️ AI 상충 검토":
    st.markdown("<h2>⚖️ 지능형 규정 상충 검토</h2>", unsafe_allow_html=True)
    st.write("신규 지침 제정 시 기존 규정과의 충돌 여부를 AI가 사전에 검토합니다.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        new_text = st.text_area("1️⃣ 신규 지침 내용을 입력하세요", height=400)
        st.markdown("</div>", unsafe_allow_html=True)
    with col_b:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        target = st.selectbox("2️⃣ 비교 대상 규정 선택", df["규정명"].tolist())
        if st.button("🚀 AI 분석 시작"):
            # (AI 로직 호출 부분...)
            st.info("분석 중입니다...")
        st.markdown("</div>", unsafe_allow_html=True)

# 3. 관리자 패널
elif menu == "🔐 관리자 패널":
    if not st.session_state['admin_mode']:
        st.markdown("<div style='max-width:400px; margin: 100px auto;'>", unsafe_allow_html=True)
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.subheader("관리자 로그인")
        pw = st.text_input("비밀번호", type="password")
        if st.button("Login"):
            if pw == "admin123": # 비밀번호 설정
                st.session_state['admin_mode'] = True
                st.rerun()
            else: st.error("비밀번호가 올바르지 않습니다.")
        st.markdown("</div></div>", unsafe_allow_html=True)
    else:
        st.header("⚙️ 시스템 관리자 모드")
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.write("데이터 수정 및 파일 업로드 공간")
        st.dataframe(df)
        st.markdown("</div>", unsafe_allow_html=True)
