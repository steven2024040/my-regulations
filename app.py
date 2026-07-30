import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# 1. 페이지 설정 및 디자인 (CSS)
st.set_page_config(page_title="청암대학교 규정정보시스템", layout="wide")

# CSS 주입: 세련된 디자인 적용
st.markdown("""
    <style>
    /* 기본 배경색 */
    .main {
        background-color: #f8f9fa;
    }
    /* 타이틀 스타일 */
    .main-title {
        color: #003366;
        font-family: 'Pretendard', sans-serif;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 30px;
    }
    /* 카드 스타일 */
    .stCard {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    /* 버튼 스타일 */
    div.stButton > button:first-child {
        background-color: #003366;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background-color: #0055aa;
        transform: translateY(-2px);
    }
    /* 탭 메뉴 폰트 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre;
        font-weight: 700;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. AI 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')

# 3. 데이터 로드
@st.cache_data
def load_data():
    return pd.read_excel("data.xlsx")

df = load_data()

# --- 헤더 영역 ---
st.markdown("<h1 class='main-title'>🏛️ 청암대학교 규정/지침 통합 관리 시스템</h1>", unsafe_allow_html=True)

# --- 상단 탭 메뉴 (현대적인 UX) ---
tab1, tab2, tab3 = st.tabs(["🔍 규정/지침 열람", "🤖 AI 지능형 검토", "ℹ️ 시스템 안내"])

with tab1:
    st.markdown("<div class='stCard'>", unsafe_allow_html=True)
    col1, col2 = st.columns([0.3, 0.7])
    
    with col1:
        st.subheader("검색 및 필터")
        search_q = st.text_input("규정명 검색", placeholder="예: 복무, 장학")
        dept_filter = st.multiselect("부서별 보기", df["관리부서"].unique())
        
        filtered_df = df.copy()
        if search_q:
            filtered_df = filtered_df[filtered_df["규정명"].str.contains(search_q, na=False)]
        if dept_filter:
            filtered_df = filtered_df[filtered_df["관리부서"].isin(dept_filter)]
            
        st.write(f"검색 결과: {len(filtered_df)}건")
        selected_reg = st.selectbox("상세 내용을 볼 규정 선택", filtered_df["규정명"].tolist())

    with col2:
        if selected_reg:
            st.subheader(f"📄 {selected_reg}")
            file_info = df[df["규정명"] == selected_reg]
            file_name = file_info["파일명"].values[0]
            
            if pd.notna(file_name):
                try:
                    with open(f"docs/{file_name}", "r", encoding="utf-8") as f:
                        content = f.read()
                    st.text_area("규정 본문", content, height=600)
                except:
                    st.error("파일 내용을 불러올 수 없습니다.")
            else:
                st.info("이 규정은 본문 텍스트가 아직 등록되지 않았습니다.")
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='stCard'>", unsafe_allow_html=True)
    st.subheader("🤖 AI 상충 검토 워크스테이션")
    st.write("새로운 지침이 기존 규정과 충돌하는지 AI가 분석합니다.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        new_doc_content = st.text_area("1️⃣ 신규 지침(안) 내용을 입력하세요", height=350, placeholder="새로 제정하거나 개정하려는 내용을 붙여넣으세요.")
    with col_b:
        target_reg_name = st.selectbox("2️⃣ 비교할 상위 규정을 선택하세요", df["규정명"].tolist())
        target_file = df[df["규정명"] == target_reg_name]["파일명"].values[0]
        
        if st.button("🚀 교차 검토 실행"):
            if new_doc_content and pd.notna(target_file):
                with st.spinner("AI 분석 전문가가 검토 중입니다..."):
                    try:
                        with open(f"docs/{target_file}", "r", encoding="utf-8") as f:
                            target_content = f.read()
                        
                        prompt = f"대학 규정 전문가로서 다음 신규 지침이 기존 규정과 상충되는지 분석해줘.\n\n[기존 규정]\n{target_content}\n\n[신규 지침]\n{new_doc_content}"
                        response = model.generate_content(prompt)
                        
                        st.markdown("---")
                        st.markdown("### 📋 AI 검토 보고서")
                        st.write(response.text)
                    except:
                        st.error("기존 규정 파일을 찾을 수 없습니다.")
            else:
                st.warning("내용 입력과 규정 선택을 완료해주세요.")
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("<div class='stCard'>", unsafe_allow_html=True)
    st.subheader("시스템 가이드")
    st.write("""
    - **열람:** 학교의 모든 규정과 부서 지침을 한눈에 확인할 수 있습니다.
    - **검토:** 실무자가 새로운 지침을 올리기 전 상위 규정과의 충돌을 사전에 방지합니다.
    - **관리:** 규정 개정 시 엑셀 파일과 텍스트 파일만 업데이트하면 즉시 반영됩니다.
    """)
    st.info("문의: 기획처 규정관리 담당자 (내선: 0000)")
    st.markdown("</div>", unsafe_allow_html=True)
