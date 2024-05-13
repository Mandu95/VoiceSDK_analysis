import streamlit as st
st.set_page_config(layout="wide")


import data_process


##페이지 상단 영역
st.subheader("Puzzle-AI VoiceSDK 대시보드")

col9, col10 = st.columns([8, 2])
st.subheader("Notion DB를 기준으로 분석한 자료입니다.:sunglasses:")

# 탭메뉴 영역
tab1, tab2 = st.tabs(["VoiceSDK 업체 현황", "VoiceSDK 파일"])

with tab1:
    col1, col2 = st.columns([5, 5])
st.write("Streamlit is working without notion_API.")