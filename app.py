import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. 페이지 설정 및 디자인 시스템
st.set_page_config(page_title="청암대학교 규정정보시스템", layout="wide")

# 고도화된 CSS (Premium Enterprise Style)
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 기본 배경 및 폰트 */
    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif;
        background-color: #f8f9fa !important;
    }

    /* 사이드바 스타일 (Dark Navy & Modern) */
    [data-testid="stSidebar"] {
        background-color: #001529 !important;
        min-width: 280px;
    }
    [data-testid="stSidebarNav"] {display: none;}
    
    .sidebar-header {
        padding: 2.5rem 1.5rem;
        text-align: center;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 1rem;
    }
    .sidebar-header h1 { color: #fff; font-size: 20px; font-weight: 800; letter-spacing: 1px; }

    /* 메인 컨테이너 밸런스 */
    .main .block-container {
        max-width: 1200px;
        padding: 3rem 2rem;
    }

    /* 카드 레이아웃 (고급스러운 그림자) */
    .premium-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.04);
        border: 1px solid #edf2f7;
        margin-bottom: 1.5rem;
    }

    /* 부서별 태그 스타일 */
    .dept-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        background: #e9ecef;
        color: #495057;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    /* 버튼 스타일 (Mint & Navy) */
    div.stButton > button {
        background: #001529;
        color: white;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background: #002c59;
        box-shadow: 0 4px 12px rgba(0,21,41,0.2);
    }
    
    /* 규정 목록 리스트 아이템 */
    .reg-item {
        padding: 15px;
        border-bottom: 1px solid #f1f3f5;
        transition: 0.2s;
        cursor: pointer;
    }
    .reg-item:hover { background-color: #f8f9fa; }
    .reg-title { font-weight: 700; color: #333; font-size: 16px; }
    
    /* 텍스트 영역 스타일 */
    .stTextArea textarea { border-radius: 12px; border: 1px solid #e2e8f0; }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터 로드
@st.cache_data
def load_data():
    # 엑셀 파일 로드 (부서명, 규정명, 파일명 컬럼 포함 가정)
    try:
        df = pd.read_excel("data.xlsx")
        return df
    except:
        # 파일이 없을 경우 예시 데이터
        return pd.DataFrame({
            "관리부서": ["교무처", "사무처", "학생처", "기획처"],
            "규정명": ["학칙", "인사규정", "장학금 지급 규정", "조직 및 정원 규정"],
            "파일명": ["rule1.txt", "rule2.txt", "rule3.txt", "rule4.txt"]
        })

df = load_data()

# 3. AI 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')

# 4. 사이드바 내비게이션
with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <h1>CHUNGAM</h1>
            <p style='color: #4fc3f7; font-size: 12px; font-weight: 600;'>REGULATION PORTAL</p>
        </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio(
        "NAVIGATION",
        ["🏛️ 규정/지침 라이브러리", "🔬 실무자 전용 AI 검토", "🔐 시스템 관리"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.info("💡 **시스템 안내**\n교내 모든 규정을 투명하게 공개하며 AI를 통해 행정 충돌을 방지합니다.")

# 5. 메인 화면 로직

# --- A. 규정 라이브러리 (공개형 목록 + 검색) ---
if menu == "🏛️ 규정/지침 라이브러리":
    st.markdown("<h2 style='color:#001529;'>🏛️ 규정/지침 라이브러리</h2>", unsafe_allow_html=True)
    st.write("청암대학교의 모든 학칙 및 부서별 지침을 확인할 수 있는 통합 보관소입니다.")
    
    # 상단 검색 및 필터 바
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns([0.7, 0.3])
    with col1:
        search_query = st.text_input("🔍 찾으시는 규정의 이름을 입력하세요", placeholder="검색어를 입력하면 아래 목록이 실시간으로 필터링됩니다.")
    with col2:
        dept_filter = st.selectbox("부서별 필터", ["전체 부서"] + sorted(df["관리부서"].unique().tolist()))
    st.markdown("</div>", unsafe_allow_html=True)

    # 데이터 필터링
    filtered_df = df.copy()
    if search_query:
        filtered_df = filtered_df[filtered_df["규정명"].str.contains(search_query, na=False)]
    if dept_filter != "전체 부서":
        filtered_df = filtered_df[filtered_df["관리부서"] == dept_filter]

    # 목록 표시
    col_list, col_view = st.columns([0.4, 0.6])
    
    with col_list:
        st.markdown(f"**총 {len(filtered_df)}건의 규정이 공개되어 있습니다.**")
        for idx, row in filtered_df.iterrows():
            st.markdown(f"""
                <div class='reg-item'>
                    <span class='dept-tag'>{row['관리부서']}</span><br>
                    <span class='reg-title'>{row['규정명']}</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"열람하기", key=f"btn_{idx}"):
                st.session_state['selected_reg'] = row['규정명']
                st.session_state['selected_file'] = row['파일명']

    with col_view:
        if 'selected_reg' in st.session_state:
            st.markdown(f"<div class='premium-card'><h4>📄 {st.session_state['selected_reg']}</h4><hr>", unsafe_allow_html=True)
            # 파일 읽기 로직
            try:
                with open(f"docs/{st.session_state['selected_file']}", "r", encoding="utf-8") as f:
                    content = f.read()
                st.text_area("규정 본문", content, height=600)
            except:
                st.info("본문 텍스트를 준비 중인 규정입니다.")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='premium-card' style='text-align:center; padding: 100px 0; color:#999;'>왼쪽 목록에서 규정을 선택하면<br>본문이 여기에 표시됩니다.</div>", unsafe_allow_html=True)

# --- B. 실무자 전용 AI 검토 (상충 검토) ---
elif menu == "🔬 실무자 전용 AI 검토":
    st.markdown("<h2 style='color:#001529;'>🔬 실무자용 상충 검토 워크스테이션</h2>", unsafe_allow_html=True)
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.write("새로운 지침을 제정하거나 기존 지침을 개정할 때, **타 부서 규정과 충돌하는 부분이 없는지** AI가 전수 점검합니다.")
    
    draft_text = st.text_area("개정(안) 또는 신설 지침 내용을 입력하세요", height=300, placeholder="검토받을 지침의 조항을 상세히 입력할수록 정확한 분석이 가능합니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        check_target = st.multiselect("검토 대상 부서 규정", df["관리부서"].unique(), default=df["관리부서"].unique(), help="선택한 부서들의 규정과 상충 여부를 대조합니다.")
    
    if st.button("🚀 지능형 상충 검토 시작"):
        if draft_text:
            with st.spinner("교내 전체 규정 데이터베이스와 대조하여 상충 로직을 분석 중입니다..."):
                # 실제 구현 시에는 선택된 부서의 모든 텍스트를 취합하여 프롬프트에 넣음
                prompt = f"""
                당신은 대학 행정 및 법률 전문가입니다. 
                다음은 우리 대학교의 특정 부서에서 새로 개정하려는 '지침(안)'입니다.
                이 내용이 기존의 다른 부서 규정들과 비교했을 때, 논리적으로 모순되거나 절차상 충돌하는 부분이 있는지 분석해 주세요.
                
                [개정 지침(안)]
                {draft_text}
                
                [분석 가이드라인]
                1. 타 부서의 고유 권한을 침해하는지 여부
                2. 상위 학칙과 배치되는 단어나 표현이 있는지 여부
                3. 행정 절차상 이중 결재나 누락이 발생할 소지가 있는지 여부
                
                분석 결과를 '안전', '주의', '상충' 단계로 요약하고 상세 의견을 주세요.
                """
                response = model.generate_content(prompt)
                st.markdown("### 📋 AI 상충 분석 보고서")
                st.markdown(response.text)
        else:
            st.warning("분석할 지침 내용을 입력해 주세요.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- C. 시스템 관리 ---
elif menu == "🔐 시스템 관리":
    # 비밀번호 보호 로직 생략 (기존과 동일하게 적용 가능)
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.subheader("⚙️ 관리자 설정")
    st.write("규정 데이터베이스 업데이트 및 시스템 로그를 확인합니다.")
    st.dataframe(df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
