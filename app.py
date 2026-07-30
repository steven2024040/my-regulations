import streamlit as st
import pandas as pd
import os

# 1. 페이지 기본 설정
st.set_page_config(page_title="청암대 규정/지침 통합 관리 시스템", layout="wide")

# 2. 사이드바 - 사용자 모드 선택
st.sidebar.title("🔐 접속 모드")
user_mode = st.sidebar.radio("모드를 선택하세요", ["일반 사용자(열람)", "실무자(검토/등록)", "관리자"])

# 3. 데이터 로드 (함수화)
@st.cache_data
def load_data():
    return pd.read_excel("data.xlsx")

df = load_data()

# --- [A] 일반 사용자 모드 ---
if user_mode == "일반 사용자(열람)":
    st.header("🏛️ 규정/지침 통합 검색실")
    search = st.text_input("찾으시는 규정/지침 키워드를 입력하세요")
    # (이전의 검색 및 목록 출력 코드 동일...)
    st.dataframe(df[df['규정명'].str.contains(search, na=False)] if search else df, use_container_width=True)

# --- [B] 실무자 모드 (AI 사전 검토) ---
elif user_mode == "실무자(검토/등록)":
    st.header("🔍 신규 지침 사전 검토실")
    st.info("새로운 지침을 등록하기 전, 기존 규정과 충돌하는 부분이 있는지 AI가 검토합니다.")
    
    password = st.text_input("부서 비밀번호를 입력하세요", type="password")
    
    if password == "1234": # 예시 비밀번호
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("1️⃣ 신규 지침 입력")
            new_doc = st.text_area("작성 중인 지침 내용을 붙여넣으세요.", height=300)
            
        with col2:
            st.subheader("2️⃣ 비교 대상 규정 선택")
            target_reg = st.selectbox("충돌 여부를 확인할 상위 규정을 선택하세요", df["규정명"].tolist())
            
        if st.button("🚀 AI 교차 검토 시작"):
            if new_doc:
                with st.spinner("AI가 두 규정을 정밀 대조 중입니다..."):
                    # 여기에 나중에 Gemini AI 연결 코드가 들어갑니다.
                    st.success("분석 완료!")
                    st.warning(f"⚠️ 검토 결과: 신규 내용 중 일부가 '{target_reg}'의 제5조와 충돌할 가능성이 있습니다.")
                    st.markdown("**[AI 권고안]** 지침의 문구를 '총장의 승인을 득한 후'에서 '위원회 심의를 거쳐'로 변경하는 것을 추천합니다.")
            else:
                st.error("신규 지침 내용을 입력해주세요.")

# --- [C] 관리자 모드 ---
elif user_mode == "관리자":
    st.header("⚙️ 시스템 관리자 페이지")
    admin_pw = st.text_input("관리자 암호", type="password")
    if admin_pw == "admin123":
        st.write("📊 데이터 업데이트 현황")
        st.write(df)
        st.button("전체 지침 현행화 점검")
