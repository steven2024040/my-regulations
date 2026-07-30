import streamlit as st
import pandas as pd

# 웹사이트 제목
st.set_page_config(page_title="청암대학교 규정 통합 관리 시스템", layout="wide")
st.title("🏛️ 청암대학교 규정/지침 통합 검색")

# 간단한 설명
st.markdown("""
이 시스템은 교내 모든 규정과 부서별 지침을 한눈에 확인하기 위한 프로토타입입니다.
좌측 메뉴에서 부서별/분류별 필터를 선택하세요.
""")

# 데이터 불러오기 (나중에 엑셀 파일과 연동)
# 지금은 테스트용 임시 데이터를 만듭니다.
data = {
    "분류": ["제3편 규정관리", "제6편 일반행정", "제6편 일반행정"],
    "규정명": ["규정관리 규정", "교직원 복무 규정", "교직원 포상 규정"],
    "관리부서": ["기획처", "총무처", "총무처"],
    "상태": ["현행", "현행", "개정예정"]
}
df = pd.DataFrame(data)

# 검색창
search = st.text_input("검색어를 입력하세요 (예: 복무, 포상, 기획처)")

# 필터링 로직
if search:
    df = df[df['규정명'].str.contains(search) | df['관리부서'].str.contains(search)]

# 화면에 표로 보여주기
st.dataframe(df, use_container_width=True)

# 규정 간 충돌 검토 (AI 기능 예시 버튼)
if st.button("AI 규정 충돌 검토 시작 (Beta)"):
    st.info("비교할 두 가지 규정을 선택하시면 AI가 상충 여부를 분석합니다.")
