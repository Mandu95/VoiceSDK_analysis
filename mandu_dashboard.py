import streamlit as st
import data_process

st.set_page_config(layout="wide")

df = data_process.df
# 페이지 상단 영역
st.subheader("PuzzleAI's 사업부 대시보드")

col9, col10 = st.columns([8, 2])
st.subheader("Notion DB를 기준으로 분석한 자료입니다.:sunglasses:")
table_height = 400  # 테이블 높이 (픽셀 단위)
table_width = 800   # 테이블 너비 (픽셀 단위)

# 탭메뉴 영역
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["VoiceEMR", "VoiceENR", "VoiceSDK", "VoiceMARK", "VoiceDOC"])
# VoiceEMR
with tab1:

    col1, col2, col3 = st.columns([4, 3, 3])

    with col1:
        st.metric(label="고객", value=55)
    with col2:
        st.metric(label="정식계약", value=9)
    with col3:
        st.metric(label="데모계약", value=30)

    active_df = df[df['연관 제품'] == 'VoiceEMR'].reset_index(drop=True)
    active_df.index += 1
    st.dataframe(active_df,height=table_height, width=table_width)

# VoiceENR
with tab2:

    col4, col5, col6 = st.columns([4, 3, 3])

    with col4:
        st.metric(label="고객", value=4)
    with col5:
        st.metric(label="정식계약", value=4)
    with col6:
        st.metric(label="데모계약", value=0)

    active_df = df[df['연관 제품'] == 'VoiceENR'].reset_index(drop=True)
    active_df.index += 1
    st.dataframe(active_df,height=table_height, width=table_width)

# VoiceSDK
with tab3:

    col7, col8, col9 = st.columns([4, 3, 3])

    with col7:
        st.metric(label="고객", value=9)
    with col8:
        st.metric(label="정식계약", value=0)
    with col9:
        st.metric(label="협업 중", value=2)
    active_df = df[df['연관 제품'] == 'VoiceSDK'].reset_index(drop=True)
    active_df.index += 1
    st.dataframe(active_df,height=table_height, width=table_width)

# VoiceMARK
with tab4:

    col10, col11, col12 = st.columns([4, 3, 3])

    with col10:
        st.metric(label="고객", value=1)
    with col11:
        st.metric(label="정식계약", value=1)
    with col12:
        st.metric(label="데모계약", value=0)

    active_df = df[df['연관 제품'] == 'VoiceMARK'].reset_index(drop=True)
    active_df.index += 1
    st.dataframe(active_df,height=table_height, width=table_width)

# VoiceDOC
with tab5:
    col13, col14, col15 = st.columns([4, 3, 3])

    with col13:
        st.metric(label="고객", value=1)
    with col14:
        st.metric(label="정식계약", value=0)
    with col15:
        st.metric(label="데모계약", value=0)

    active_df = df[df['연관 제품'] == 'VoiceDOC'].reset_index(drop=True)
    active_df.index += 1
    st.dataframe(active_df,height=table_height, width=table_width)
