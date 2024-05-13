import streamlit as st

import notion_API

nc = notion_API.notion_API()  ##notion api 호출해서 DB 연결
all_key = ["8f0bbf0eae504cd29a45080803aa74cf", "2301ef1117d14da1a495e36a65fb1e74"] ##내가 조회하고자 하는 DB 키 정적입력 type = list
data = nc.notion_readDatabase(all_key)  ## DB 데이터 추출
database_properties = nc.extract_properties(data) ## dic 형태에서 properties 속성 값만 추출

st.set_page_config(layout="wide")


##페이지 상단 영역
st.subheader("Puzzle-AI VoiceSDK 대시보드")


col9, col10 = st.columns([8, 2])
st.subheader("Notion DB를 기준으로 분석한 자료입니다.:sunglasses:")

# 탭메뉴 영역
tab1, tab2 = st.tabs(["VoiceSDK 업체 현황", "VoiceSDK 파일"])


with tab1:
    # 시스템 작업 DB 탭 누르면 표시될 내용
    col1, col2 = st.columns([5, 5])

with tab2:
    # 시스템 작업 DB 탭 누르면 표시될 내용

    st.dataframe(
        database_properties[0],
        use_container_width=False,
        hide_index=None,
        column_order=None,
        column_config=None,
    )
