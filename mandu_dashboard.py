import streamlit as st
import data_process

st.set_page_config(layout="wide")



##페이지 상단 영역
st.subheader("PuzzleAI's 사업부 대시보드")

col9, col10 = st.columns([8, 2])
st.subheader("Notion DB를 기준으로 분석한 자료입니다.:sunglasses:")

# 탭메뉴 영역
tab1, tab2, tab3, tab4 = st.tabs(["VoiceENR", "VoiceSDK", "VoiceMARK","VoicDOC"])

with tab1:
    col1, col2 = st.columns([5, 5])
    st.write ("컨텐츠 삽입 예정")
