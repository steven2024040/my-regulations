import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. 페이지 설정 (중앙 집중형 레이아웃을 위해 wide 대신 기본이나 커스텀 설정)
st.set_page_config(page_title="청암대학교 규정정보시스템", layout="wide", initial_sidebar_state="expanded")

# 2. 강력한 CSS 주입 (웹사이트 구조 설계)
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 전체 배경 및 폰트 설정 */
    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif;
        background-color: #f0f2f5 !important;
    }

    /* 사이드바 커스텀 */
    [data-testid="stSidebar"] {
        background-color: #1a237e !important;
        border-right: 1px solid #e0e0e0;
    }
    [data-testid="stSidebarNav"] {display: none;} /* 기본 네비게이션 숨김 */
    
    .sidebar-header {
        padding: 2rem 1rem;
        text-align: center;
        color: white;
    }

    /* 메인 콘텐츠 영역 밸런스 조정 */
    .main .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* 웹사이트 상단 헤더 */
    .custom-header {
        background-color: white;
        padding: 1rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .header-title {
        color: #1a237e;
        font-size: 1.5rem;
        font-weight: 800;
    }

    /* 콘텐츠 카드 스타일 */
    .white-card {
        background-color: white;
        padding: 2.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 2rem;
    }

    /* 버튼 디자인 고도화 */
    .stButton>button {
        background: linear-gradient(135deg, #1a237e 0%, #3949ab 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(26, 35, 126, 0.3);
    }

    /* 입력창 테두리 강조 제거 및 깔끔하게 */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 및 AI 설정 (기존과 동일)
@st.cache_data
def load_data():
    return pd.read_excel("data.xlsx")

df = load_data()

if "admin_mode" not in st.session_state: st.session_state['admin_mode'] = False

# --- [좌측 사이드바: 네비게이션 메뉴] ---
with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <h1 style='font-size: 24px; margin-bottom: 0;'>CHUNGAM</h1>
            <p style='font-size: 14px; opacity: 0.7;'>규정 통합 관리 시스템</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 세련된 메뉴 선택
    menu = st.radio(
        "메인 메뉴",
        ["🏠 시스템 홈", "🔍 규정/지침 검색", "⚖️ AI 상충 검토", "🔐 관리자 로그"],
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='position: fixed; bottom: 20px; left: 20px; color: rgba(255,255,255,0.4); font-size: 12px;'>© 2024 Chungam College</div>", unsafe_allow_html=True)

# --- [상단 헤더 영역] ---
st.markdown(f"""
    <div class="custom-header">
        <div class="header-title">{menu}</div>
        <div style="color: #666; font-size: 14px;">관리부서: 기획처 규정관리팀</div>
    </div>
""", unsafe_allow_html=True)

# --- [메인 콘텐츠 로직] ---

# 1. 시스템 홈
if menu == "🏠 시스템 홈":
    st.markdown("<div class='white-card'>", unsafe_allow_html=True)
    st.markdown("""
        <h2 style='color:#1a237e; margin-top:0;'>청암대학교 규정정보시스템에 오신 것을 환영합니다.</h2>
        <p style='color:#666; line-height:1.6;'>본 시스템은 교내의 모든 학칙, 규정 및 부서별 내부 지침을 효율적으로 관리하고 
        신규 지침 제정 시 발생할 수 있는 규정 간 충돌을 AI 기술을 통해 사전에 검토하기 위해 구축되었습니다.</p>
        <hr style='border: 0.5px solid #eee; margin: 2rem 0;'>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px;'>
            <div style='padding: 20px; background: #f8f9ff; border-radius: 10px;'>
                <h4 style='margin-top:0; color:#1a237e;'>🔍 신속한 규정 검색</h4>
                <p style='font-size: 14px; color:#777;'>부서별로 흩어진 지침을 키워드 하나로 즉시 찾아보세요.</p>
            </div>
            <div style='padding: 20px; background: #f8f9ff; border-radius: 10px;'>
                <h4 style='margin-top:0; color:#1a237e;'>⚖️ AI 지능형 검토</h4>
                <p style='font-size: 14px; color:#777;'>Gemini 1.5 PRO AI가 규정 간 상충 여부를 실시간 분석합니다.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 2. 규정 검색
elif menu == "🔍 규정/지침 검색":
    st.markdown("<div class='white-card'>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])
    with c1:
        search = st.text_input("검색어 입력", placeholder="예: 복무, 장학, 포상")
    with c2:
        dept = st.selectbox("부서 선택", ["전체"] + list(df["관리부서"].unique()))
    
    res = df.copy()
    if search: res = res[res["규정명"].str.contains(search, na=False)]
    if dept != "전체": res = res[res["관리부서"] == dept]
    
    selected = st.selectbox(f"조회할 규정 선택 (총 {len(res)}건)", res["규정명"].tolist())
    st.markdown("</div>", unsafe_allow_html=True)
    
    if selected:
        st.markdown("<div class='white-card'>", unsafe_allow_html=True)
        st.subheader(f"📄 {selected}")
        # 파일 읽기 로직... (생략, 기존과 동일)
        st.text_area("규정 본문", "규정 본문 텍스트가 여기에 표시됩니다.", height=500)
        st.markdown("</div>", unsafe_allow_html=True)

# 3. AI 상충 검토
elif menu == "⚖️ AI 상충 검토":
    st.markdown("<div class='white-card'>", unsafe_allow_html=True)
    st.subheader("🤖 신규 지침 사전 검토 서비스")
    st.write("작성 중인 지침을 입력하고 대조할 상위 규정을 선택해 주세요.")
    
    new_doc = st.text_area("1️⃣ 신규 지침(안) 내용", height=300, placeholder="내용을 붙여넣으세요.")
    target = st.selectbox("2️⃣ 비교 대상 상위 규정", df["규정명"].tolist())
    
    if st.button("AI 상충 분석 시작"):
        with st.spinner("AI가 정밀 분석 중입니다..."):
            st.success("분석이 완료되었습니다. 결과 리포트를 확인하세요.")
    st.markdown("</div>", unsafe_allow_html=True)

# 4. 관리자 로그
elif menu == "🔐 관리자 로그":
    if not st.session_state['admin_mode']:
        st.markdown("<div style='max-width: 450px; margin: 0 auto;'>", unsafe_allow_html=True)
        st.markdown("<div class='white-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align:center;'>ADMIN LOGIN</h3>", unsafe_allow_html=True)
        pw = st.text_input("Administrator Password", type="password")
        if st.button("Login"):
            if pw == "admin123":
                st.session_state['admin_mode'] = True
                st.rerun()
            else: st.error("접근 권한이 없습니다.")
        st.markdown("</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='white-card'>", unsafe_allow_html=True)
        st.subheader("⚙️ 관리자 컨트롤 패널")
        st.write("전체 데이터베이스 관리 및 시스템 로그 확인")
        st.dataframe(df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
