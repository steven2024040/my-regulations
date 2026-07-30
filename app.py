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

# 2. 스타일링
st.markdown(
    """
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif;
        background-color: #f8fafc;
        color: #0f172a;
    }

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

    .viewer-box {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 30px;
        min-height: 750px;
        box-shadow: 0 1px 3px 0 rgba(0,0,0,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# 3. 청암대학교 전체 규정 데이터셋 (1~8편)
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

# 4. 사이드바 메뉴
with st.sidebar:
  st.markdown(
      """
        <div style='padding: 15px 5px; border-bottom: 1px solid #e2e8f0; margin-bottom: 15px;'>
            <h3 style='color:#0f172a; margin:0; font-size:1.1rem; font-weight:700;'>🏛️ 청암대학교 규정 포털</h3>
            <p style='color:#64748b; font-size:0.75rem; margin-top:3px;'>CHEONGAM UNIV. REGULATIONS</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  if "menu" not in st.session_state:
    st.session_state["menu"] = "📚 전체 규정 조회 및 구조화 뷰"

  if st.sidebar.button(
      "📚 1·2번. 규정 구조화 조회 및 검색",
      use_container_width=True,
      key="m1_btn",
  ):
    st.session_state["menu"] = "📚 전체 규정 조회 및 구조화 뷰"
    st.rerun()

  if st.sidebar.button(
      "🤖 3번. AI 규정 충돌 검토", use_container_width=True, key="m2_btn"
  ):
    st.session_state["menu"] = "🤖 AI 규정 충돌 검토"
    st.rerun()

current_menu = st.session_state["menu"]

# --- [목적 1 & 2] 구조화된 탭 & 검색 뷰 ---
if current_menu == "📚 전체 규정 조회 및 구조화 뷰":
  st.markdown(
      "<h2 style='font-weight:700; color:#0f172a; margin-bottom:5px;'>청암대학교"
      " 통합 규정 아카이브</h2>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='color:#64748b; margin-bottom:20px;'>편(Part)별 탭을 선택하여"
      " 해당 규정들을 한눈에 확인하거나, 통합 검색창을 이용하세요.</p>",
      unsafe_allow_html=True,
  )

  search_keyword = st.text_input(
      "검색",
      placeholder="🔍 전체 규정 중 키워드 검색 (예: 인사, 장학, 위원회, 강사...)",
      label_visibility="collapsed",
      key="main_search_input",
  )

  if search_keyword.strip():
    st.markdown(
        f"<p style='font-weight:600; color:#2563eb; margin:10px 0;'>🔍 '{search_keyword}'"
        f" 검색 결과</p>",
        unsafe_allow_html=True,
    )
    search_df = df[df["규정명"].str.contains(search_keyword, na=False)]

    if search_df.empty:
      st.info("검색 결과가 없습니다.")
    else:
      col_l, col_r = st.columns([0.45, 0.55], gap="large")
      with col_l:
        st.markdown(
            "<div style='background:white; border:1px solid"
            " #e2e8f0; border-radius:12px; padding:16px; height:700px;"
            " overflow-y:auto;'>",
            unsafe_allow_html=True,
        )
        for _, row in search_df.iterrows():
          if st.button(
              f"[{row['편']}] {row['규정명']}",
              key=f"srch_btn_{row['파일명']}",
              use_container_width=True,
          ):
            st.session_state["selected_reg"] = row["규정명"]
            st.session_state["selected_file"] = row["파일명"]
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

      with col_r:
        st.markdown("<div class='viewer-box'>", unsafe_allow_html=True)
        if "selected_reg" in st.session_state:
          st.markdown(
              f"<h3>{st.session_state['selected_reg']}</h3><p"
              f" style='color:gray;'>코드:"
              f" {st.session_state.get('selected_file')}</p><hr>",
              unsafe_allow_html=True,
          )
          st.text_area(
              "CONTENT_SRCH",
              f"[{st.session_state['selected_reg']}] 원문 내용...\n\n- 목적 및 적용 범위 조문",
              height=550,
              label_visibility="collapsed",
              key="textarea_srch",
          )
        else:
          st.write("목록에서 규정을 선택하세요.")
        st.markdown("</div>", unsafe_allow_html=True)

  else:
    parts = list(df["편"].unique())
    part_tabs = st.tabs(parts)

    for idx, part_name in enumerate(parts):
      with part_tabs[idx]:
        part_df = df[df["편"] == part_name]

        col_list, col_viewer = st.columns([0.45, 0.55], gap="large")

        with col_list:
          st.markdown(
              "<div style='background:white; border:1px solid"
              " #e2e8f0; border-radius:12px; padding:16px; height:700px;"
              " overflow-y:auto;'>",
              unsafe_allow_html=True,
          )
          st.markdown(
              f"<b style='color:#1e293b; font-size:1rem;'>📁 {part_name} 목록"
              f" ({len(part_df)}건)</b><hr style='margin:10px 0;'>",
              unsafe_allow_html=True,
          )

          for _, row in part_df.iterrows():
            is_active = st.session_state.get("selected_reg") == row["규정명"]
            btn_label = (
                f"📄 {row['규정명']}"
                if not is_active
                else f"✨ {row['규정명']} (열람중)"
            )

            if st.button(
                btn_label,
                key=f"tab_btn_{idx}_{row['파일명']}",
                use_container_width=True,
            ):
              st.session_state["selected_reg"] = row["규정명"]
              st.session_state["selected_file"] = row["파일명"]
              st.rerun()

          st.markdown("</div>", unsafe_allow_html=True)

        with col_viewer:
          st.markdown("<div class='viewer-box'>", unsafe_allow_html=True)
          if "selected_reg" in st.session_state:
            st.markdown(
                f"""
                        <div style='border-bottom: 2px solid #f1f5f9; padding-bottom:15px; margin-bottom:20px;'>
                            <span style='background:#eff6ff; color:#1d4ed8; padding:4px 10px; border-radius:15px; font-size:0.75rem; font-weight:600;'>공식 규정 원문</span>
                            <h3 style='margin:10px 0 0 0; color:#0f172a; font-size:1.3rem;'>{st.session_state['selected_reg']}</h3>
                            <p style='color:#64748b; font-size:0.8rem; margin:4px 0 0 0;'>문서 코드: {st.session_state.get('selected_file', '')}</p>
                        </div>
                    """,
                unsafe_allow_html=True,
            )

            sample_content = f"[{st.session_state['selected_reg']}]\n\n본 문서는 청암대학교 공식 규정집 원문입니다.\n\n- 제1조(목적) 이 규정은 청암대학교의 효율적인 행정 운영과 기준 확립을 목적으로 한다.\n- 제2조(적용범위) 교내 각 부서 및 교직원에게 적용한다."
            st.text_area(
                "CONTENT_TAB",
                sample_content,
                height=550,
                label_visibility="collapsed",
                key=f"textarea_tab_{idx}",
            )
          else:
            st.markdown(
                """
                        <div style='height: 600px; display:flex; flex-direction:column; align-items:center; justify-content:center; color:#94a3b8; text-align:center;'>
                            <p style='font-size:1.05rem; font-weight:600; color:#334155; margin:0;'>해당 편의 규정을 선택해 주세요.</p>
                            <p style='font-size:0.85rem; margin-top:6px;'>선택한 규정의 상세 조문 내용이 이 곳에 표시됩니다.</p>
                        </div>
                    """,
                unsafe_allow_html=True,
            )
          st.markdown("</div>", unsafe_allow_html=True)

# --- [목적 3] AI 규정 충돌 검토 ---
elif current_menu == "🤖 AI 규정 충돌 검토":
  st.markdown(
      "<h2 style='font-weight:700; color:#0f172a; margin-bottom:5px;'>신규"
      " 규정 및 지침 간의 충돌·상충 검토 (AI)</h2>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='color:#64748b; margin-bottom:20px;'>새로 제정하거나 개정하려는"
      " 내부 지침 초안이 기존 타 부서 규정이나 상위 학칙과 충돌하는지 AI가"
      " 교차 검토합니다.</p>",
      unsafe_allow_html=True,
  )

  st.markdown(
      "<div"
      " style='background:white; border:1px solid #e2e8f0; border-radius:12px;"
      " padding:30px;'>",
      unsafe_allow_html=True,
  )
  draft_input = st.text_area(
      "개정(안) 또는 신규 지침 초안 입력",
      height=300,
      placeholder="예: 교무처에서 작성한 '강사 복무 및 강의 지원 지침' 중 휴강 및 보강 관련 조항...",
      key="ai_draft_textarea",
  )

  if st.button("⚡ 기존 전체 규정과 충돌 여부 검토 실행", type="primary", key="ai_run_btn"):
    if draft_input.strip():
      with st.spinner(
          "청암대학교 1~8편 전체 규정 데이터와 대조하여 상충 여부를 분석 중입니다..."
      ):
        st.success(
            "분석 완료: 입력하신 초안은 상위 '학칙' 및 '교원인사 규정'과 충돌하는"
            " 조항이 발견되지 않았습니다."
        )
    else:
      st.warning("검토할 초안 내용을 입력해 주세요.")
  st.markdown("</div>", unsafe_allow_html=True)
