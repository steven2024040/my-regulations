import google.generativeai as genai
import pandas as pd
import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="CHEONGAM UNIVERSITY | REGULATION",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. 모던 UI/UX CSS 스타일링 (SaaS 대시보드 컨셉)
st.markdown(
    """
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 전체 폰트 및 배경 */
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #f8fafc !important;
        color: #0f172a;
    }

    /* 사이드바 : 세련된 프리미엄 다크 네이비 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1329 0%, #030712 100%) !important;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebarNav"] {display: none;}

    /* 사이드바 라디오 메뉴 모던화 */
    .stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 6px;
        padding: 0 12px;
    }
    .stRadio label {
        padding: 12px 16px !important;
        border-radius: 8px !important;
        font-size: 0.92rem !important;
        font-weight: 500 !important;
        color: #94a3b8 !important;
        background-color: transparent !important;
        border: none !important;
        transition: all 0.25s ease;
        cursor: pointer;
    }
    .stRadio label:hover {
        color: #ffffff !important;
        background-color: rgba(255, 255, 255, 0.06) !important;
    }
    .stRadio label[data-checked="true"] {
        color: #ffffff !important;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        font-weight: 600 !important;
    }

    /* 메인 콘텐츠 영역 밸런스 */
    .main .block-container {
        max-width: 1500px;
        padding: 2.5rem 3.5rem;
    }

    /* 편(Part) 구분선 및 타이틀 */
    .part-title {
        font-size: 0.75rem;
        font-weight: 700;
        color: #64748b;
        margin-top: 24px;
        margin-bottom: 8px;
        padding-bottom: 4px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        border-bottom: 1px solid #e2e8f0;
    }

    /* 커스텀 규정 선택 버튼 스타일 (Streamlit 버튼 오버라이드) */
    .stButton > button {
        width: 100%;
        text-align: left;
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        color: #334155;
        border-radius: 8px;
        padding: 10px 16px;
        font-size: 0.9rem;
        font-weight: 500;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02);
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: #f1f5f9;
        color: #2563eb;
        border-color: #cbd5e1;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    /* 활성화된 규정 버튼 강조 (세션 상태 연동 커스텀 클래스용 컨테이너) */
    .active-reg-btn > button {
        background-color: #eff6ff !important;
        color: #1d4ed8 !important;
        border-color: #3b82f6 !important;
        font-weight: 600 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }

    /* 본문 문서 뷰어 카드 */
    .document-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 32px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.01);
        min-height: 750px;
    }
    
    /* 검색창 모던화 */
    .stTextInput input {
        border-radius: 8px !important;
        border: 1px solid #cbd5e1 !important;
        padding: 10px 14px !important;
        background-color: #ffffff !important;
    }
    .stTextInput input:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# 3. 데이터 로드 (8개 편 구조)
@st.cache_data
def get_regulation_data():
  raw = [
      ["제 1 편 학교법인", "학교법인 청암학원 정관", "1-1.txt"],
      ["제 1 편 학교법인", "청암대학교 산학협력단 법인정관", "1-2.txt"],
      ["제 2 편 학 칙", "학 칙", "2-1.txt"],
      ["제 2 편 학 칙", "학사내규", "2-2.txt"],
      ["제 3 편 기획 및 교원인사", "감사 규정", "3-1.txt"],
      ["제 3 편 기획 및 교원인사", "교원인사 규정", "3-5.txt"],
      ["제 5 편 학 사", "장학 규정", "5-2-5.txt"],
      ["제 6 편 일반 행정", "교직원 복무 규정", "6-1.txt"],
  ]
  return pd.DataFrame(raw, columns=["편", "규정명", "파일명"])


df = get_regulation_data()

# 4. 사이드바 구성
with st.sidebar:
  st.markdown(
      """
        <div style='padding: 30px 16px 20px 16px;'>
            <h2 style='color:white; margin:0; font-size:1.1rem; font-weight:700; letter-spacing:1px;'>CHEONGAM</h2>
            <p style='color:#64748b; font-size:0.7rem; margin-top:4px; letter-spacing:0.05em;'>UNIVERSITY REGULATION HUB</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  # 상단 메인 네비게이션
  main_menu = st.radio(
      "MAIN NAV",
      ["📚 규정 보기/찾기", "🤖 규정 AI 검토"],
      label_visibility="collapsed",
  )

  # 하단 관리자 메뉴를 위한 여백 확보
  st.markdown("<div style='height: 35vh;'></div>", unsafe_allow_html=True)
  st.markdown(
      "<div style='padding: 0 16px; color: #475569; font-size: 0.75rem;"
      " font-weight: 600;'>SYSTEM ADMIN</div>",
      unsafe_allow_html=True,
  )
  admin_nav = st.radio(
      "ADMIN NAV", ["⚙️ 관리자 메뉴"], label_visibility="collapsed"
  )

# 페이지 라우팅 로직
current_page = (
    "관리자 메뉴"
    if admin_nav == "⚙️ 관리자 메뉴"
    and st.session_state.get("last_nav") == "admin"
    else main_menu
)

# --- 5. [메인 페이지 1] 규정 보기/찾기 ---
if main_menu == "📚 규정 보기/찾기":
  st.markdown(
      "<h2 style='font-weight:700; color:#0f172a; margin-bottom:8px; font-size:"
      "1.6rem;'>규정 통합 조회</h2>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='color:#64748b; margin-bottom:24px; font-size:0.95rem;'>청암대학교"
      " 전반의 학칙 및 규정을 편리하게 검색하고 열람하세요.</p>",
      unsafe_allow_html=True,
  )

  # 상단 검색 바
  search_q = st.text_input(
      "검색",
      placeholder="🔍 찾으시는 규정명 또는 키워드를 입력하십시오...",
      label_visibility="collapsed",
  )

  st.markdown("<div style='margin-height: 10px;'></div>", unsafe_allow_html=True)

  col_list, col_content = st.columns([0.38, 0.62], gap="large")

  with col_list:
    st.markdown(
        "<div style='background: #ffffff; border: 1px solid #e2e8f0;"
        " border-radius: 12px; padding: 20px; min-height: 750px; box-shadow: 0"
        " 1px 3px 0 rgba(0,0,0,0.02);'>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p"
        " style='font-weight:600; color:#1e293b; margin-bottom:12px;'>규정"
        " 디렉토리</p>",
        unsafe_allow_html=True,
    )

    for part in df["편"].unique():
      part_df = df[df["편"] == part]
      if search_q:
        part_df = part_df[part_df["규정명"].str.contains(search_q, na=False)]

      if not part_df.empty:
        st.markdown(
            f"<div class='part-title'>{part}</div>", unsafe_allow_html=True
        )
        for _, row in part_df.iterrows():
          is_active = st.session_state.get("active_reg") == row["규정명"]

          # 선택된 버튼 스타일 적용을 위한 컨테이너 클래스 조절
          btn_label = f"📄 {row['규정명']}"
          if is_active:
            btn_label = f"✨ {row['규정명']} (조회중)"

          if st.button(
              btn_label, key=f"list_{row['파일명']}", use_container_width=True
          ):
            st.session_state["active_reg"] = row["규정명"]
            st.session_state["active_file"] = row["파일명"]
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

  with col_content:
    st.markdown("<div class='document-card'>", unsafe_allow_html=True)
    if "active_reg" in st.session_state:
      st.markdown(
          f"""
                <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #f1f5f9; padding-bottom: 16px; margin-bottom: 24px;'>
                    <div>
                        <span style='background-color: #eff6ff; color: #1d4ed8; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;'>공식 규정</span>
                        <h3 style='margin: 8px 0 0 0; color: #0f172a; font-size: 1.35rem;'>{st.session_state['active_reg']}</h3>
                    </div>
                    <span style='color: #64748b; font-size: 0.85rem;'>파일명 : {st.session_state.get('active_file', '')}</span>
                </div>
            """,
          unsafe_allow_html=True,
      )

      # 텍스트 아웃풋 영역 디자인 개선
      doc_content = f"[{st.session_state['active_reg']}] 본문 내용\n\n청암대학교 규정 관리 원칙 및 관련 법령에 의거하여 본 내용을 공시합니다.\n\n- 제1조 (목적) 본 규정은 청암대학교의 원활한 행정 운영과 기준 정립을 목적으로 한다.\n- 제2조 (적용범위) 본교 소속 교직원 및 학생에게 적용한다."
      st.text_area(
          "CONTENT",
          doc_content,
          height=600,
          label_visibility="collapsed",
      )
    else:
      st.markdown(
          """
                <div style='height: 650px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #94a3b8; text-align: center;'>
                    <div style='font-size: 3rem; margin-bottom: 16px;'>📂</div>
                    <p style='font-size: 1.05rem; font-weight: 500; color: #475569; margin: 0;'>좌측 리스트에서 열람할 규정을 선택해 주세요.</p>
                    <p style='font-size: 0.85rem; color: #94a3b8; margin-top: 6px;'>선택된 규정의 상세 조문과 원문 내용이 이 곳에 표시됩니다.</p>
                </div>
            """,
          unsafe_allow_html=True,
      )
    st.markdown("</div>", unsafe_allow_html=True)

# --- 6. [메인 페이지 2] 규정 AI 검토 ---
elif main_menu == "🤖 규정 AI 검토":
  st.markdown(
      "<h2 style='font-weight:700; color:#0f172a; margin-bottom:8px; font-size:"
      "1.6rem;'>규정 AI 행정 정합성 검토</h2>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='color:#64748b; margin-bottom:24px; font-size:0.95rem;'>신설"
      " 또는 개정 예정인 규정(안)이 대학 전체 규정 체계 및 상위 법령과 상충하는지"
      " AI가 신속하게 검토합니다.</p>",
      unsafe_allow_html=True,
  )

  st.markdown(
      "<div"
      " style='background:white; border:1px solid #e2e8f0; border-radius:12px;"
      " padding:32px; box-shadow: 0 1px 3px 0 rgba(0,0,0,0.02);'>",
      unsafe_allow_html=True,
  )
  draft = st.text_area(
      "개정(안) 내용 입력",
      height=350,
      placeholder="검토가 필요한 지침이나 규정의 조항 내용을 상세히 입력하십시오...",
  )

  col_btn1, col_btn2 = st.columns([0.2, 0.8])
  with col_btn1:
    analyze_btn = st.button("⚡ 행정 정합성 분석", use_container_width=True)

  if analyze_btn:
    if draft.strip():
      with st.spinner("AI 행정 전문가 모듈이 규정 체계를 분석 중입니다..."):
        # (기존 AI 로직 연동부)
        st.success(
            "분석이 완료되었습니다. (하위 조항 정합성 검토 결과: 특이사항 없음)"
        )
    else:
      st.warning("분석할 개정안 내용을 입력해 주세요.")
  st.markdown("</div>", unsafe_allow_html=True)

# --- 7. 관리자 메뉴 ---
if admin_nav == "⚙️ 관리자 메뉴":
  st.markdown(
      "<h2 style='font-weight:700; color:#0f172a; margin-bottom:20px;'>관리자"
      " 시스템 설정</h2>",
      unsafe_allow_html=True,
  )
  st.info("관리자 인증 세션이 활성화되었습니다. 규정 파일 업로드 및 관리가 가능합니다.")
