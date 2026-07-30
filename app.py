import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="청암대학교 규정 통합 관리", layout="wide")
st.title("🏛️ 청암대학교 규정/지침 통합 검색")

try:
    df = pd.read_excel("data.xlsx")
    
    # 레이아웃 나누기 (왼쪽: 목록, 오른쪽: 본문)
    col1, col2 = st.columns([0.4, 0.6])

    with col1:
        st.subheader("🔍 규정 목록")
        search_query = st.text_input("검색어 입력")
        
        filtered_df = df.copy()
        if search_query:
            filtered_df = filtered_df[filtered_df["규정명"].str.contains(search_query, na=False)]
        
        # 목록을 라디오 버튼 형태로 보여주기 (클릭 시 선택되게 함)
        selected_reg = st.radio("상세 내용을 보려면 규정을 선택하세요", 
                                filtered_df["규정명"].tolist(),
                                label_visibility="collapsed")

    with col2:
        st.subheader("📄 규정 본문")
        if selected_reg:
            # 선택된 규정의 파일명 찾기
            file_name = df[df["규정명"] == selected_reg]["파일명"].values[0]
            
            if pd.isna(file_name):
                st.warning("이 규정은 아직 본문 파일이 등록되지 않았습니다.")
            else:
                try:
                    # GitHub의 docs 폴더에서 텍스트 파일 읽기
                    file_path = f"docs/{file_name}"
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    st.text_area("본문 내용", content, height=500)
                    
                    # AI 분석 버튼 (미래의 충돌 검토 기능 자리)
                    if st.button("🤖 AI에게 이 규정 요약 시키기"):
                        st.write("AI 기능이 곧 업데이트될 예정입니다!")
                        
                except FileNotFoundError:
                    st.error(f"파일을 찾을 수 없습니다: {file_path}")

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
