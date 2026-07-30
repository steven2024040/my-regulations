import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. 페이지 설정 및 프리미엄 테마 적용
st.set_page_config(page_title="CHEONGAM UNIVERSITY | 규정정보시스템", layout="wide")

# 고급스러운 UI를 위한 CSS
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 기본 배경 및 폰트 */
    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif;
        background-color: #f4f7fa !important;
    }

    /* 사이드바 스타일 (CHEONGAM Navy) */
    [data-testid="stSidebar"] {
        background-color: #002147 !important; /* 깊은 네이비 */
        min-width: 300px;
    }
    
    /* 사이드바 텍스트 컬러 고정 */
    [data-testid="stSidebar"] * { color: #ffffff !important; }

    /* 메인 영역 밸런스 */
    .main .block-container {
        max-width: 1400px;
        padding: 2rem 4rem;
    }

    /* 편(Part) 구분 카드 스타일 */
    .part-header {
        background: linear-gradient(90deg, #002147 0%, #004080 100%);
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* 규정 아이템 스타일 */
    .reg-card {
        background: white;
        padding: 12px 20px;
        border-radius: 8px;
        border-left: 5px solid #002147;
        margin-bottom: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: 0.2s;
    }
    .reg-card:hover {
        transform: translateX(5px);
        background: #f8f9ff;
    }

    /* 프리미엄 컨테이너 */
    .premium-container {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }

    /* 버튼 스타일 */
    .stButton>button {
        background-color: #002147;
        color: white;
        border-radius: 6px;
        font-weight: 600;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 목차 데이터 구조화 (샘플 기반 데이터프레임)
# 실제 운영 시에는 모든 목록을 엑셀에 넣고 '편' 컬럼을 추가하세요.
def get_full_data():
    data = [
        ["제 1 편 학교법인", "학교법인 청암학원 정관", "1-1.txt"],
        ["제 1 편 학교법인", "청암대학교 산학협력단 법인정관", "1-2.txt"],
        ["제 2 편 학 칙", "학 칙", "2-1.txt"],
        ["제 2 편 학 칙", "학사내규", "2-2.txt"],
        ["제 3 편 기획 및 교원인사", "교원인사 규정", "3-5.txt"],
        ["제 3 편 기획 및 교원인사", "교원임용 규정", "3-6.txt"],
        ["제 4 편 산학협력", "산학협력단 운영 규정", "4-2.txt"],
        ["제 5 편 학 사", "장학 규정", "5-2-5.txt"],
        ["제 6 편 일반 행정", "교직원 복무 규정", "6-1.txt"],
        ["제 7 편 부속/부설기관", "도서관 규정", "7-3.txt"],
        ["제 8 편 위원회", "교무위원회 규정", "8-1.txt"],
    ]
    return pd.DataFrame(data, columns=["편", "규정명", "파일명"])

df = get_full_data()

# AI 설정
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')

# --- 사이드바 ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>CHEONGAM</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity:0.7;'>UNIVERSITY</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    menu = st.radio("MAIN MENU", ["🏛️ 규정 라이브러리", "🤖 지능형 상충 검토", "⚙️ 관리자 설정"])
    
    st.markdown("---")
    st.caption("본 시스템은 대학의 모든 규정을 투명하게 공개하며 AI를 통해 행정 정합성을 유지합니다.")

# --- 메인 로직 ---

if menu == "🏛️ 규정 라이브러리":
    st.markdown("<h1 style='color:#002147;'>🏛️ 규정/지침 라이브러리</h1>", unsafe_allow_html=True)
    
    # 검색 섹션
    st.markdown("<div class='premium-container'>", unsafe_allow_html=True)
    search_q = st.text_input("🔍 검색어를 입력하세요 (예: 인사, 장학, 복무)", placeholder="200여 개의 규정을 실시간으로 검색합니다.")
    st.markdown("</div>", unsafe_allow_html=True)

    # 8개 편(Part)별로 그룹화하여 표시
    parts = ["제 1 편 학교법인", "제 2 편 학 칙", "제 3 편 기획 및 교원인사", "제 4 편 산학협력", 
             "제 5 편 학 사", "제 6 편 일반 행정", "제 7 편 부속/부설기관", "제 8 편 위원회"]

    col_view1, col_view2 = st.columns([0.45, 0.55])

    with col_view1:
        for part in parts:
            part_df = df[df["편"] == part]
            if search_q:
                part_df = part_df[part_df["규정명"].str.contains(search_q, na=False)]
            
            if not part_df.empty:
                st.markdown(f"<div class='part-header'>{part}</div>", unsafe_allow_html=True)
                for _, row in part_df.iterrows():
                    # 버튼 대신 클릭 가능한 카드 형태 구현
                    if st.button(f"📄 {row['규정명']}", key=f"lib_{row['규정명']}"):
                        st.session_state['current_reg'] = row['규정명']
                        st.session_state['current_file'] = row['파일명']

    with col_view2:
        if 'current_reg' in st.session_state:
            st.markdown(f"<div class='premium-container'><h3>{st.session_state['current_reg']}</h3>", unsafe_allow_html=True)
            # 파일 읽기 시뮬레이션
            st.text_area("규정 본문", f"[{st.session_state['current_reg']}]의 상세 내용이 여기에 표시됩니다.\n\n(실제 docs/{st.session_state['current_file']}의 내용 로드)", height=700)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='premium-container' style='text-align:center; padding:200px 0;'>규정을 선택하면 본문이 표시됩니다.</div>", unsafe_allow_html=True)

elif menu == "🤖 지능형 상충 검토":
    st.markdown("<h1 style='color:#002147;'>🤖 지능형 상충 검토</h1>", unsafe_allow_html=True)
    st.markdown("<div class='premium-container'>", unsafe_allow_html=True)
    st.subheader("신규/개정 지침 정책 정합성 테스트")
    st.write("작성 중인 지침안이 **청암대학교의 기존 8개 편 규정 체계**와 충돌하지 않는지 AI가 검토합니다.")
    
    draft = st.text_area("지침(안) 본문 입력", height=350, placeholder="검토받을 지침의 조항 내용을 상세히 입력하세요.")
    
    if st.button("🚀 정책 정합성 검토 실행"):
        if draft:
            with st.spinner("AI 행정 전문가가 전체 규정 체계와의 모순점을 분석 중입니다..."):
                # 실제 운영 시에는 관련 편(Part)의 텍스트를 모두 프롬프트에 제공
                prompt = f"""
                당신은 '청암대학교(CHEONGAM UNIVERSITY)'의 법무 행정 전문가입니다.
                새로 제안된 아래 지침안이 대학의 기존 8개 편 규정(정관, 학칙, 인사, 산학, 학사, 행정 등)과 
                논리적으로 충돌하거나 행정적 모순이 발생하는지 분석하세요.

                [신규 제안 지침안]
                {draft}

                [분석 요청 사항]
                1. 상위 규정(정관 및 학칙) 위배 여부
                2. 타 부서(사무, 학생, 산학 등) 규정과의 중복 또는 권한 침해 여부
                3. 용어의 통일성 및 행정 절차의 실현 가능성
                
                결과를 '적합', '주의', '상충'으로 구분하여 상세 리포트를 작성하세요.
                """
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown("### 📋 AI 행정 정합성 분석 결과")
                st.write(response.text)
        else:
            st.warning("분석할 내용을 입력하세요.")
    st.markdown("</div>", unsafe_allow_html=True)
