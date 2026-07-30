import streamlit as st
import pandas as pd
import google.generativeai as genai
import os

# 1. AI 설정 (금고에서 키를 가져옴)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API 키가 설정되지 않았습니다. Streamlit Secrets를 확인해주세요.")

# 2. 페이지 설정
st.set_page_config(page_title="청암대 규정 통합 관리 시스템", layout="wide")
st.title("🏛️ 청암대학교 규정/지침 지능형 시스템")

# 데이터 로드
@st.cache_data
def load_data():
    return pd.read_excel("data.xlsx")

df = load_data()

# 사이드바 모드 선택
user_mode = st.sidebar.radio("접속 모드", ["일반 사용자(열람)", "실무자(AI 사전 검토)"])

# --- [A] 일반 사용자 모드 (생략 - 기존과 동일) ---
if user_mode == "일반 사용자(열람)":
    st.header("🔍 규정/지침 통합 검색")
    search = st.text_input("검색어 입력")
    st.dataframe(df[df['규정명'].str.contains(search, na=False)] if search else df, use_container_width=True)

# --- [B] 실무자 모드 (AI 상충 검토 핵심 기능) ---
elif user_mode == "실무자(AI 사전 검토)":
    st.header("🤖 AI 규정 상충 검토 워크스테이션")
    st.info("신규 지침이 기존 규정과 충돌하는지 AI가 법률 전문가처럼 분석합니다.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1️⃣ 신규 지침(안) 입력")
        new_doc_content = st.text_area("작성 중인 지침 본문을 입력하세요.", height=400)
        
    with col2:
        st.subheader("2️⃣ 비교 대상 규정 선택")
        target_reg_name = st.selectbox("충돌이 우려되는 기존 규정을 선택하세요", df["규정명"].tolist())
        
        # 선택된 기존 규정 파일 읽기
        target_file = df[df["규정명"] == target_reg_name]["파일명"].values[0]
        target_content = ""
        if pd.notna(target_file):
            try:
                with open(f"docs/{target_file}", "r", encoding="utf-8") as f:
                    target_content = f.read()
                st.success(f"'{target_reg_name}' 본문을 성공적으로 불러왔습니다.")
            except:
                st.error("기존 규정 파일을 읽을 수 없습니다.")

    if st.button("🚀 AI 교차 검토 실행"):
        if new_doc_content and target_content:
            with st.spinner("AI가 두 문서를 대조하여 상충 조항을 분석 중입니다..."):
                prompt = f"""
                당신은 대학의 규정 심의 전문가입니다. 
                다음 두 문서를 비교하여, '신규 지침(안)'이 '기존 규정'의 내용과 충돌하거나 위배되는 부분이 있는지 분석하세요.
                
                [기존 규정: {target_reg_name}]
                {target_content}
                
                [신규 지침(안)]
                {new_doc_content}
                
                분석 결과는 다음 형식을 지켜주세요:
                1. 상충 여부 (적합/주의/부적합)
                2. 충돌이 우려되는 구체적인 조항 번호와 내용
                3. 수정 제안 및 사유
                """
                
                response = model.generate_content(prompt)
                st.markdown("### 📋 AI 분석 결과 보고서")
                st.write(response.text)
        else:
            st.warning("신규 내용과 비교 대상 규정이 모두 준비되어야 합니다.")
