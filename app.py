import streamlit as st
import pandas as pd

# 웹사이트 설정
st.set_page_config(page_title="청암대학교 규정 통합 관리", layout="wide")

st.title("🏛️ 청암대학교 규정/지침 통합 검색")

# 엑셀 파일 읽기
try:
    df = pd.read_excel("data.xlsx")
    
    # 사이드바: 필터 기능
    st.sidebar.header("🔍 필터 설정")
    all_categories = ["전체"] + list(df["분류"].unique())
    selected_category = st.sidebar.selectbox("편별 분류", all_categories)
    
    all_depts = ["전체"] + list(df["관리부서"].unique())
    selected_dept = st.sidebar.selectbox("관리부서", all_depts)

    # 검색창
    search_query = st.text_input("찾으시는 규정명을 입력하세요", placeholder="예: 복무, 장학, 인사")

    # 데이터 필터링 로직
    filtered_df = df.copy()
    
    if selected_category != "전체":
        filtered_df = filtered_df[filtered_df["분류"] == selected_category]
        
    if selected_dept != "전체":
        filtered_df = filtered_df[filtered_df["관리부서"] == selected_dept]
        
    if search_query:
        filtered_df = filtered_df[filtered_df["규정명"].str.contains(search_query, na=False)]

    # 결과 출력
    st.subheader(f"📋 검색 결과 (총 {len(filtered_df)}건)")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"데이터 파일을 읽는 중 오류가 발생했습니다: {e}")
    st.info("GitHub에 'data.xlsx' 파일이 올바르게 업로드되었는지 확인해주세요.")
