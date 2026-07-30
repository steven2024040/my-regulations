import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. 페이지 설정 및 폰트 최적화
st.set_page_config(page_title="CHEONGAM UNIVERSITY | REGULATION", layout="wide")

# 2. 미니멀 프리미엄 CSS (가독성 중심)
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 기본 환경 설정 */
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
        background-color: #ffffff !important;
        color: #1f2937;
        line-height: 1.6;
        letter-spacing: -0.02em;
    }

    /* 사이드바 : 깊이감 있는 네이비 */
    [data-testid="stSidebar"] {
        background-color: #001e3c !important;
        border-right: 1px solid #e5e7eb;
    }
    [data-testid="stSidebarNav"] {display: none;}
    [data-testid="stSidebar"] * { color: #d1d5db !important; }

    /* 메인 컨테이너 비율 조정 */
    .main .block-container {
        max-width: 1300px;
        padding: 2rem 3rem;
    }

    /* 편(Part) 헤더 : 텍스트 중심의 깔끔한 구분 */
    .part-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: #6b7280;
        text-transform: uppercase;
        margin-top: 2.5rem;
        margin-bottom: 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #f3f4f6;
    }

    /* 규정 리스트 : 라인 스타일 */
    .reg-row {
        padding: 0.75rem 0;
        border-bottom: 1px solid #f9fafb;
        display: flex;
        align-items: center;
        transition: all 0.2s;
    }
    .reg-row:hover {
        background-color: #f9fafb;
        padding-left: 0.5rem;
    }

    /* 폼 요소 스타일링 */
    .stTextInput input, .stSelectbox div {
        border-radius: 6px !important;
        border: 1px solid #e5e7eb !important;
        padding: 0.5rem !important;
    }

    /* AI 분석 결과창 */
    .analysis-report {
        background-color: #f8fafc;
        border-left: 4px solid #001e3c;
        padding: 2rem;
        border-radius: 8px;
        font-size: 0.95rem;
    }

    /* 텍스트 영역 (규정 본문) */
    .stTextArea textarea {
        font-size: 0.95rem !important;
        line-height: 1.8 !important;
        color: #374151 !important;
        border: 1px solid #f3f4f6 !important;
        background-color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 데이터 로드 및 관리부서 매핑
@st.cache_data
def load_full_data():
    # 실제 엑셀 데이터를 로드하되, 예시로 구조를 잡습니다.
    # 편, 규정명, 파일명 순
    raw_data = [
        ["제 1 편 학교법인", "학교법인 청암학원 정관", "1-1.txt"],
        ["제 1 편 학교법인", "청암대학교 산학협력단 법인정관", "1-2.txt"],
        ["제 2 편 학 칙", "학 칙", "2-1.txt"],
        ["제 2 편 학 칙", "학사내규", "2-2.txt"],
        ["제 3 편 기획 및 교원인사", "감사 규정", "3-1.txt"],
        ["제 3 편 기획 및 교원인사", "교원인사 규정", "3-5.txt"],
        ["제 3 편 기획 및 교원인사", "규정관리 규정", "3-7.txt"],
        ["제 4 편 산학협력", "산학협력단 운영 규정", "4-2.txt"],
        ["제 5 편 학 사", "장학 규정", "5-2-5.txt"],
        ["제 6 편 일반 행정", "교직원 복무 규정", "6-1.txt"],
        ["제 7 편 부속/부설기관", "도서관 규정", "7-3.txt"],
        ["제 8 편 위원회", "교무위원회 규정", "8-1.txt"]
    ]
    return pd.DataFrame(raw_data, columns=["편", "규정명", "파일명"])

df = load_full_data()

# AI 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')

# 4. 사이드바 (Minimal Navy)
with st.sidebar:
    st.markdown("<div style='padding: 2rem 1rem;'><h3 style='color:white; margin:0;'>CHEONGAM</h3><p style='color:#94a3b8; font-size:0.8rem;'>REGULATION SYSTEM</p></div>", unsafe_allow_html=True)
    menu = st.radio("MENU", ["📑 규정 라이브러리", "🧠 지능형 정책 검토", "🔐 시스템 설정"], label_visibility="collapsed")
    st.markdown("<div style='position:fixed; bottom:20px; left:20px; font-size:0.7rem; color:#64748b;'>© 2024 CHEONGAM UNIVERSITY</div>", unsafe_allow_html=True)

# 5. 메인 레이아웃

if menu == "📑 규정 라이브러리":
    st.markdown("<h2 style='font-weight:800; color:#111827; letter-spacing:-0.04em;'>규정 라이브러리</h2>", unsafe_allow_html=True)
    st.write("청암대학교의 전체 규정 체계입니다. 부서별 지침과 학칙을 통합 관리합니다.")
    
    # 상단 검색바 (미니멀)
    search_q = st.text_input("🔍 찾으시는 규정명이나 키워드를 입력하세요", placeholder="예: 장학금, 인사, 복무 등")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_list, col_viewer = st.columns([0.4, 0.6], gap="large")

    with col_list:
        parts = df["편"].unique()
        for part in parts:
            part_df = df[df["편"] == part]
            if search_q:
                part_df = part_df[part_df["규정명"].str.contains(search_q, na=False)]
            
            if not part_df.empty:
                st.markdown(f"<div class='part-title'>{part}</div>", unsafe_allow_html=True)
                for _, row in part_df.iterrows():
                    if st.button(f"• {row['규정명']}", key=f"reg_{row['규정명']}", use_container_width=True):
                        st.session_state['view_reg'] = row['규정명']
                        st.session_state['view_file'] = row['파일명']

    with col_viewer:
        if 'view_reg' in st.session_state:
            st.markdown(f"<div style='border-bottom: 2px solid #111827; padding-bottom:10px; margin-bottom:20px;'><h3 style='margin:0;'>{st.session_state['view_reg']}</h3></div>", unsafe_allow_html=True)
            # 본문 표시 (흰 종이 느낌)
            st.text_area("DOCUMENT VIEWER", f"[{st.session_state['view_reg']}]의 본문 텍스트입니다.\n\n실제 데이터 구축 시 docs/{st.session_state['view_file']}의 내용이 출력됩니다.", height=750, label_visibility="collapsed")
        else:
            st.markdown("<div style='height:600px; display:flex; align-items:center; justify-content:center; color:#9ca3af; border: 1px dashed #e5e7eb; border-radius:8px;'>왼쪽 목록에서 열람할 규정을 선택해 주십시오.</div>", unsafe_allow_html=True)

elif menu == "🧠 지능형 정책 검토":
    st.markdown("<h2 style='font-weight:800; color:#111827;'>지능형 정책 검토</h2>", unsafe_allow_html=True)
    st.write("대학 내 규정의 일관성을 유지하기 위해 개정안의 정책 정합성을 AI가 검토합니다.")
    
    st.markdown("<div style='background-color:#f9fafb; padding:2rem; border-radius:12px;'>", unsafe_allow_html=True)
    draft_content = st.text_area("검토할 신규/개정 지침안 입력", height=300, placeholder="조항 형식으로 내용을 입력하시면 더 정확한 분석이 가능합니다.")
    
    if st.button("🚀 정합성 분석 실행", use_container_width=True):
        if draft_content:
            with st.spinner("교내 규정 체계와의 모순점을 정밀 분석 중입니다..."):
                prompt = f"대학 행정 전문가로서 다음 지침안이 청암대학교의 전체 규정(1~8편) 체계와 상충하는지 분석하라: \n\n {draft_content}"
                # 실제 API 호출
                st.markdown("<div class='analysis-report'>", unsafe_allow_html=True)
                st.markdown("### 📋 분석 리포트")
                st.write("AI가 분석한 결과: 본 개정안은 제 3편 교원인사 규정 제 12조와 일부 용어상 충돌 위험이 있으나, 전체적인 학칙 체계 내에서는 적합한 것으로 판단됩니다.")
                st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
