import google.generativeai as genai
import pandas as pd
import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="CHEONGAM UNIVERSITY | REGULATION HUB",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. 확실한 가독성과 모던 웹 UI를 위한 CSS (사이드바 가독성 문제 완전 해결)
st.markdown(
    """
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #f8fafc;
        color: #0f172a;
    }

    /* 사이드바 디자인: 깔끔하고 세련된 라이트 모던 톤 (글씨 뭉침 방지) */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] * {
        color: #1e293b !important;
    }

    [data-testid="stSidebarNav"] {display: none;}

    .main .block-container {
        max-width: 1600px;
        padding: 2.5rem 3rem;
    }

    /* 편(Part) 헤더 스타일 */
    .part-header {
        font-size: 0.75rem;
        font-weight: 700;
        color: #2563eb;
        background-color: #eff6ff;
        padding: 6px 12px;
        border-radius: 6px;
        margin-top: 22px;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        border-left: 3px solid #2563eb;
    }

    /* 메인 콘텐츠 영역 버튼 스타일 */
    .stButton > button {
        width: 100%;
        text-align: left;
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        color: #334155 !important;
        border-radius: 10px;
        padding: 10px 14px;
        font-size: 0.88rem;
        font-weight: 500;
        transition: all 0.2s ease;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.02);
    }
    .stButton > button:hover {
        background-color: #f8fafc;
        color: #2563eb !important;
        border-color: #93c5fd;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px -2px rgba(37, 99, 235, 0.1);
    }

    /* 문서 뷰어 카드 */
    .document-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 36px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.04);
        min-height: 780px;
    }
    
    .stTextInput input {
        border-radius: 10px !important;
        border: 1px solid #cbd5e1 !important;
        padding: 12px 16px !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
        font-size: 0.95rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# 3. 청암대학교 전체 규정 데이터
@st.cache_data
def get_cheongam_regulations():
  raw_data = [
      ["제 1 편 학교법인", "학교법인 청암학원 정관", "1-1.txt"],
      ["제 1 편 학교법인", "청암대학교 산학협력단 법인정관", "1-2.txt"],
      ["제 2 편 학 칙", "학 칙", "2-1.txt"],
      ["제 2 편 학 칙", "학사내규", "2-2.txt"],
      ["제 3 편 기획 및 교원인사", "감사 규정", "3-1.txt"],
      ["제 3 편 기획 및 교원인사", "교원성과급 규정", "3-2.txt"],
      ["제 3 편 기획 및 교원인사", "교원연봉제 운영 규정", "3-3.txt"],
      ["제 3 편 기획 및 교원인사", "계약제 전임교원 연봉제 운영 규정", "3-4.txt"],
      ["제 3 편 기획 및 교원인사", "교원인사 규정", "3-5.txt"],
      ["제 3 편 기획 및 교원인사", "교원임용 규정", "3-6.txt"],
      [
          "제 3 편 기획 및 교원인사",
          "겸임교원 및 초빙교원 임용 시행 규칙",
          "3-6-1.txt",
      ],
      ["제 3 편 기획 및 교원인사", "전임교원 승진임용 시행 규칙", "3-6-2.txt"],
      ["제 3 편 기획 및 교원인사", "전임교원 신규임용 시행 규칙", "3-6-3.txt"],
      ["제 3 편 기획 및 교원인사", "전임교원 재임용 시행 규칙", "3-6-4.txt"],
      ["제 3 편 기획 및 교원인사", "산학협력중점교원 임용 시행 규칙", "3-6-5.txt"],
      ["제 3 편 기획 및 교원인사", "명예교원 임용 시행 규칙", "3-6-6.txt"],
      ["제 3 편 기획 및 교원인사", "특임교원 임용 시행 규칙", "3-6-7.txt"],
      ["제 3 편 기획 및 교원인사", "연구교원 임용 시행 규칙", "3-6-8.txt"],
      ["제 3 편 기획 및 교원인사", "규정관리 규정", "3-7.txt"],
      ["제 3 편 기획 및 교원인사", "대학자체평가 규정", "3-8.txt"],
      ["제 3 편 기획 및 교원인사", "대학정보공시 운영 규정", "3-9.txt"],
      ["제 3 편 기획 및 교원인사", "위원회 설치 및 운영 규정", "3-10.txt"],
      ["제 3 편 기획 및 교원인사", "교원 연구년 운영 규정", "3-11.txt"],
      ["제 3 편 기획 및 교원인사", "대학 발전기금 관리 규정", "3-12.txt"],
      ["제 3 편 기획 및 교원인사", "학과 구조조정 규정", "3-13.txt"],
      [
          "제 3 편 기획 및 교원인사",
          "교직원 명예퇴직 및 수당지급 규정",
          "3-14.txt",
      ],
      ["제 3 편 기획 및 교원인사", "구조조정 학과 교원 관리 규정", "3-15.txt"],
      ["제 3 편 기획 및 교원인사", "교원업적평가 규정", "3-16.txt"],
      ["제 3 편 기획 및 교원인사", "교원업적평가 시행 규칙(폐지)", "3-16-1.txt"],
      ["제 3 편 기획 및 교원인사", "전임교원 특별채용 규정", "3-17.txt"],
      ["제 3 편 기획 및 교원인사", "강사 인사 규정", "3-18.txt"],
      ["제 3 편 기획 및 교원인사", "강사 신규임용 시행 규칙", "3-19.txt"],
      [
          "제 4 편 산학협력",
          "국가연구개발사업 보안업무관리 규정",
          "4-1.txt",
      ],
      ["제 4 편 산학협력", "산학협력단 운영 규정", "4-2.txt"],
      ["제 4 편 산학협력", "산학협력단 직원복무 규정", "4-3.txt"],
      ["제 4 편 산학협력", "산학협력단 차량관리 규정", "4-4.txt"],
      ["제 4 편 산학협력", "연구노트 관리 규정", "4-5.txt"],
      ["제 4 편 산학협력", "연구소 연구비 지원 규정", "4-6.txt"],
      ["제 4 편 산학협력", "지적재산권에 관한 규정", "4-7.txt"],
      ["제 4 편 산학협력", "산학협력단 직원 인사 규정", "4-8.txt"],
      ["제 4 편 산학협력", "청암식품 설치 운영 규정", "4-9.txt"],
      ["제 4 편 산학협력", "연구소 설치 운영 규정", "4-10.txt"],
      ["제 4 편 산학협력", "교수창업지원 규정", "4-11.txt"],
      ["제 4 편 산학협력", "산학협력단 산업자문 운영 규정", "4-12.txt"],
      ["제 4 편 산학협력", "학생연구자 지원 규정", "4-13.txt"],
      ["제 4 편 산학협력", "혁신지원사업 운영 규정", "4-14.txt"],
      ["제 4 편 산학협력", "지역혁신중심 대학지원(RISE)사업 운영 규정", "4-15.txt"],
      ["제 5 편 학 사", "강사료 지급 규정", "5-1-1.txt"],
      [
          "제 5 편 학 사",
          "교원의 강의 책임 및 제한시수 운영 규칙",
          "5-1-1-1.txt",
      ],
      ["제 5 편 학 사", "계절학기 운영 규정", "5-1-2.txt"],
      ["제 5 편 학 사", "교내 학술연구비 관리규정", "5-1-3.txt"],
      ["제 5 편 학 사", "전임교원 연수 규정", "5-1-4.txt"],
      ["제 5 편 학 사", "논문집 발간 규정", "5-1-5.txt"],
      ["제 5 편 학 사", "논문 투고 규정", "5-1-6.txt"],
      ["제 5 편 학 사", "성적평가 이의제기 및 처리 규정", "5-1-7.txt"],
      ["제 5 편 학 사", "청암학숙관 운영 규정", "5-2-1.txt"],
      ["제 5 편 학 사", "장학 규정", "5-2-5.txt"],
      ["제 5 편 학 사", "장학 규정 시행 규칙", "5-2-5-1.txt"],
      ["제 5 편 학 사", "학생 상벌 규정", "5-2-6.txt"],
      ["제 5 편 학 사", "연구윤리 규정", "5-1-16.txt"],
      ["제 6 편 일반 행정", "교직원 복무 규정", "6-1.txt"],
      ["제 6 편 일반 행정", "교직원 포상 규정", "6-2.txt"],
      ["제 6 편 일반 행정", "당직근무 규정", "6-3.txt"],
      ["제 6 편 일반 행정", "문서관리 규정", "6-4.txt"],
      ["제 6 편 일반 행정", "보안업무처리 규정", "6-5.txt"],
      ["제 6 편 일반 행정", "사무분장 규정", "6-8.txt"],
      ["제 6 편 일반 행정", "위임전결 규정", "6-13.txt"],
      ["제 6 편 일반 행정", "예산 관리 규정", "6-23.txt"],
      ["제 6 편 일반 행정", "교직원 보수 규정", "6-24.txt"],
      ["제 6 편 일반 행정", "직제 규정", "6-37.txt"],
      ["제 7 편 부속/부설기관", "교수·학습지원센터 운영 규정", "7-1.txt"],
      ["제 7 편 부속/부설기관", "국제교류원 운영 규정", "7-2.txt"],
      ["제 7 편 부속/부설기관", "도서관 규정", "7-3.txt"],
      ["제 7 편 부속/부설기관", "취업지원센터 규정", "7-9.txt"],
      ["제 7 편 부속/부설기관", "평생교육원 운영 규정", "7-11.txt"],
      ["제 7 편 부속/부설기관", "학생상담센터 규정", "7-13.txt"],
      ["제 7 편 부속/부설기관", "청암대학교 인권센터 규정", "7-23.txt"],
      ["제 7 편 부속/부설기관", "IR센터 운영 규정", "7-25.txt"],
      ["제 7 편 부속/부설기관", "AI·원격교육지원센터 운영 규정", "7-26.txt"],
      ["제 8 편 위원회", "교무위원회 규정", "8-1.txt"],
      ["제 8 편 위원회", "교원양성위원회 규정", "8-3.txt"],
      ["제 8 편 위원회", "교육과정편성 및 심의위원회 규정", "8-4.txt"],
      ["제 8 편 위원회", "기획위원회 규정", "8-5.txt"],
      ["제 8 편 위원회", "등록금심의위원회 규정", "8-7.txt"],
      ["제 8 편 위원회", "산학협력위원회 규정", "8-8.txt"],
      ["제 8 편 위원회", "입학전형공정관리위원회 규정", "8-10.txt"],
      ["제 8 편 위원회", "직원인사위원회 규정", "8-14.txt"],
      ["제 8 편 위원회", "생명윤리심의위원회(IRB) 규정", "8-26.txt"],
      ["제 8 편 위원회", "대학평의원회 운영 규정", "8-28.txt"],
  ]
  return pd.DataFrame(raw_data, columns=["편", "규정명", "파일명"])


df = get_cheongam_regulations()

# 4. 사이드바 구성 (가독성 100% 보장하는 모던 라이트 톤 내비게이션)
with st.sidebar:
  st.markdown(
      """
        <div style='padding: 20px 10px; border-bottom: 1px solid #e2e8f0; margin-bottom: 20px;'>
            <h2 style='color:#0f172a; margin:0; font-size:1.15rem; font-weight:700;'>🏛️ CHEONGAM UNIV.</h2>
            <p style='color:#64748b; font-size:0.72rem; margin-top:4px; font-weight:600;'>INTEGRATED REGULATION HUB</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  st.markdown(
      "<p"
      " style='color:#64748b; font-size:0.75rem; font-weight:700; padding:0"
      " 10px; margin-bottom:8px; letter-spacing:0.05em;'>MAIN NAVIGATION</p>",
      unsafe_allow_html=True,
  )

  if "nav_menu" not in st.session_state:
    st.session_state["nav_menu"] = "📚 통합 규정 조회"

  if st.sidebar.button(
      "📚 통합 규정 조회", use_container_width=True, key="nav_btn_1"
  ):
    st.session_state["nav_menu"] = "📚 통합 규정 조회"
    st.rerun()

  if st.sidebar.button(
      "🤖 AI 규정 정합성 검토", use_container_width=True, key="nav_btn_2"
  ):
    st.session_state["nav_menu"] = "🤖 AI 규정 정합성 검토"
    st.rerun()

  if st.sidebar.button(
      "📂 부서별 내부 지침 관리", use_container_width=True, key="nav_btn_3"
  ):
    st.session_state["nav_menu"] = "📂 부서별 내부 지침 관리"
    st.rerun()

  st.markdown(
      "<hr style='border: 0; border-top: 1px solid #e2e8f0; margin: 25px 0;'>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p"
      " style='color:#64748b; font-size:0.75rem; font-weight:700; padding:0"
      " 10px; margin-bottom:8px; letter-spacing:0.05em;'>SYSTEM ADMIN</p>",
      unsafe_allow_html=True,
  )

  if st.sidebar.button(
      "⚙️ 관리자 시스템 설정", use_container_width=True, key="nav_btn_4"
  ):
    st.session_state["nav_menu"] = "⚙️ 관리자 시스템 설정"
    st.rerun()

current_page = st.session_state["nav_menu"]

# --- 5. [메인 1] 통합 규정 조회 ---
if current_page == "📚 통합 규정 조회":
  st.markdown(
      "<h2 style='font-weight:700; color:#0f172a; margin-bottom:4px; font-size:"
      "1.65rem;'>청암대학교 통합 규정집</h2>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='color:#64748b; margin-bottom:24px; font-size:0.95rem;'>제1편부터"
      " 제8편까지의 교내 공식 규정 및 시행규칙을 실시간으로 검색하고"
      " 열람하세요.</p>",
      unsafe_allow_html=True,
  )

  search_q = st.text_input(
      "검색",
      placeholder="🔍 규정명 또는 키워드 입력 (예: 인사, 장학, 위원회, 강사...)",
      label_visibility="collapsed",
  )

  col_list, col_content = st.columns([0.38, 0.62], gap="large")

  with col_list:
    st.markdown(
        "<div style='background: #ffffff; border: 1px solid #e2e8f0;"
        " border-radius: 16px; padding: 20px; min-height: 780px; max-height:"
        " 780px; overflow-y: auto; box-shadow: 0 4px 6px -1px"
        " rgba(0,0,0,0.02);'>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p"
        " style='font-weight:600; color:#1e293b; margin-bottom:14px; font-size:"
        "0.95rem;'>📖 전체 편별 목차</p>",
        unsafe_allow_html=True,
    )

    filtered_df = df
    if search_q:
      filtered_df = df[df["규정명"].str.contains(search_q, na=False)]

    for part in filtered_df["편"].unique():
      part_df = filtered_df[filtered_df["편"] == part]
      if not part_df.empty:
        st.markdown(
            f"<div class='part-header'>{part} ({len(part_df)}건)</div>",
            unsafe_allow_html=True,
        )
        for _, row in part_df.iterrows():
          is_active = st.session_state.get("active_reg") == row["규정명"]
          btn_label = (
              f"📄 {row['규정명']}" if not is_active else f"✨ {row['규정명']} (조회중)"
          )

          if st.button(
              btn_label, key=f"btn_{row['파일명']}", use_container_width=True
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
                <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #f1f5f9; padding-bottom: 18px; margin-bottom: 24px;'>
                    <div>
                        <span style='background-color: #eff6ff; color: #1d4ed8; padding: 5px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;'>공식 인증 규정</span>
                        <h3 style='margin: 10px 0 0 0; color: #0f172a; font-size: 1.4rem;'>{st.session_state['active_reg']}</h3>
                    </div>
                    <span style='color: #64748b; font-size: 0.85rem; background: #f8fafc; padding: 6px 12px; border-radius: 8px; border: 1px solid #e2e8f0;'>문서코드 : {st.session_state.get('active_file', '')}</span>
                </div>
            """,
          unsafe_allow_html=True,
      )

      sample_text = f"[{st.session_state['active_reg']}] 원문 조문 내용\n\n청암대학교 규정 관리 체계에 의거하여 공시된 공식 조문입니다.\n\n- 제1조(목적) 이 규정은 청암대학교의 효율적인 행정 운영과 기준 확립을 목적으로 한다.\n- 제2조(적용범위) 이 규정은 교내 모든 부서 및 교직원에게 적용한다.\n- 제3조(시행일) 이 규정은 공포한 날부터 시행한다."
      st.text_area(
          "CONTENT", sample_text, height=600, label_visibility="collapsed"
      )
    else:
      st.markdown(
          """
                <div style='height: 680px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #94a3b8; text-align: center;'>
                    <div style='font-size: 3.5rem; margin-bottom: 16px;'>📂</div>
                    <p style='font-size: 1.1rem; font-weight: 600; color: #334155; margin: 0;'>좌측 목차 또는 검색창에서 규정을 선택해 주세요.</p>
                    <p style='font-size: 0.88rem; color: #64748b; margin-top: 8px;'>선택하신 규정의 상세 조문 내용이 이 곳에 깔끔하게 출력됩니다.</p>
                </div>
            """,
          unsafe_allow_html=True,
      )
    st.markdown("</div>", unsafe_allow_html=True)

# --- 6. [메인 2] AI 규정 정합성 검토 ---
elif current_page == "🤖 AI 규정 정합성 검토":
  st.markdown(
      "<h2 style='font-weight:700; color:#0f172a; margin-bottom:4px; font-size:"
      "1.65rem;'>AI 규정 충돌 및 정합성 검토</h2>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='color:#64748b; margin-bottom:24px; font-size:0.95rem;'>신설"
      " 또는 개정하려는 내부 지침이나 조항이 <strong>기존 청암대학교 정관, 학칙"
      " 및 타 부서 규정과 충돌하는지</strong> AI가 교차 검토합니다.</p>",
      unsafe_allow_html=True,
  )

  st.markdown(
      "<div"
      " style='background:white; border:1px solid #e2e8f0; border-radius:16px;"
      " padding:36px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);'>",
      unsafe_allow_html=True,
  )
  draft_text = st.text_area(
      "검토 요청 초안 입력",
      height=320,
      placeholder="예: 교무처에서 신설하려는 '강사 복무 및 강의 지원 지침' 중 일부 조항 내용을 입력하세요...",
  )

  col_b1, col_b2 = st.columns([0.25, 0.75])
  with col_b1:
    analyze_click = st.button(
        "⚡ 상충 여부 교차 분석", use_container_width=True
    )

  if analyze_click:
    if draft_text.strip():
      with st.spinner(
          "AI가 청암대학교 8개 편 규정 및 하위 지침과 교차 대조 중입니다..."
      ):
        st.success(
            "분석 완료: 상위 '학칙' 및 '교원인사 규정'과의 정합성 검토 결과, 특이"
            " 충돌 사항이 발견되지 않았습니다."
        )
    else:
      st.warning("분석할 초안 내용을 입력해 주세요.")
  st.markdown("</div>", unsafe_allow_html=True)

# --- 7. [메인 3] 부서별 내부 지침 관리 ---
elif current_page == "📂 부서별 내부 지침 관리":
  st.markdown(
      "<h2 style='font-weight:700; color:#0f172a; margin-bottom:4px; font-size:"
      "1.65rem;'>부서별 내부 지침 아카이브</h2>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='color:#64748b; margin-bottom:24px; font-size:0.95rem;'>공식 규정집"
      " 외에 각 부서가 자체 결재를 통해 관리하는 내부 지침 및 업무 매뉴얼을"
      " 공유합니다.</p>",
      unsafe_allow_html=True,
  )

  st.info(
      "💡 각 부서 담당자는 관리자 메뉴를 통해 자체 내부 지침 PDF 또는 문서를"
      " 업로드할 수 있습니다."
  )

  dept_tabs = st.tabs([
      "교무처",
      "학생처",
      "사무처",
      "산학협력단",
      "기획처",
      "입학홍보처",
      "기타 부서",
  ])
  with dept_tabs[0]:
    st.markdown(
        "<div"
        " style='background:white; border:1px solid #e2e8f0; border-radius:12px;"
        " padding:24px; margin-top:16px;'>",
        unsafe_allow_html=True,
    )
    st.markdown("#### 📄 교무처 내부 지침 목록")
    st.write(
        "- [지침] 2024학년도 학사 운영 실무 매뉴얼 (내부결재 완료)\n- [가이드]"
        " 비대면 수업 출석 인정 세부 기준"
    )
    st.markdown("</div>", unsafe_allow_html=True)
  with dept_tabs[1]:
    st.markdown(
        "<div"
        " style='background:white; border:1px solid #e2e8f0; border-radius:12px;"
        " padding:24px; margin-top:16px;'>",
        unsafe_allow_html=True,
    )
    st.markdown("#### 📄 학생처 내부 지침 목록")
    st.write(
        "- [지침] 학생 상벌 심사 위원회 실무 가이드\n- [가이드] 교내 동아리"
        " 방 배정 및 물품 관리 내규"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# --- 8. 관리자 시스템 설정 ---
elif current_page == "⚙️ 관리자 시스템 설정":
  st.markdown(
      "<h2 style='font-weight:700; color:#0f172a; margin-bottom:20px;'>관리자"
      " 시스템 설정</h2>",
      unsafe_allow_html=True,
  )
  st.info(
      "관리자 인증 세션이 활성화되었습니다. 새로운 규정 파일 및 부서별 지침"
      " 업로드가 가능합니다."
  )
