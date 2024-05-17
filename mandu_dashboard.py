import streamlit as st
import data_process

st.set_page_config(layout="wide")

df = data_process.df
# 페이지 상단 영역
st.subheader("PuzzleAI's 사업부 대시보드")

col9, col10 = st.columns([8, 2])
st.subheader("Notion DB를 기준으로 분석한 자료입니다.:sunglasses:")
table_height = 400  # 테이블 높이 (픽셀 단위)
table_width = 2000  # 테이블 너비 (픽셀 단위)

# 페이지당 항목 수 설정
items_per_page = 10

def paginate_data(dataframe, page_number, items_per_page):
    start_index = (page_number - 1) * items_per_page
    end_index = start_index + items_per_page
    return dataframe.iloc[start_index:end_index]

# 탭메뉴 영역
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["VoiceEMR", "VoiceENR", "VoiceSDK", "VoiceMARK", "VoiceDOC"])

def display_tab(dataframe, tab_label, customers, contracts, demos):
    col1, col2, col3 = st.columns([4, 3, 3])

    with col1:
        st.metric(label="고객", value=customers)
    with col2:
        st.metric(label="정식계약", value=contracts)
    with col3:
        st.metric(label="데모계약", value=demos)

    total_items = len(dataframe)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    page_number = st.number_input(f'Page number for {tab_label}', min_value=1, max_value=total_pages, step=1, value=1)


    # CSS를 사용하여 입력 상자의 크기 조절
    st.markdown("""
        <style>
        .number-input-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 10px 0;
        }
        .number-input-wrapper input {
            width: 50px; /* 여기서 크기를 조절할 수 있습니다 */
            height: 40px; /* 여기서 높이를 조절할 수 있습니다 */
            font-size: 20px; /* 여기서 글꼴 크기를 조절할 수 있습니다 */
        }
        </style>
    """, unsafe_allow_html=True)

    paged_df = paginate_data(dataframe, page_number, items_per_page)
    paged_df.index += 1

    st.dataframe(paged_df, height=table_height, width=table_width)
    st.write(f"Displaying rows {page_number * items_per_page - (items_per_page - 1)} to {min(page_number * items_per_page, total_items)} of {total_items}")

# 각 탭에 데이터프레임 및 페이징 기능 적용
with tab1:
    display_tab(df[df['연관 제품'] == 'VoiceEMR'].reset_index(drop=True), "VoiceEMR", 55, 9, 30)
with tab2:
    display_tab(df[df['연관 제품'] == 'VoiceENR'].reset_index(drop=True), "VoiceENR", 4, 4, 0)
with tab3:
    display_tab(df[df['연관 제품'] == 'VoiceSDK'].reset_index(drop=True), "VoiceSDK", 9, 0, 2)
with tab4:
    display_tab(df[df['연관 제품'] == 'VoiceMARK'].reset_index(drop=True), "VoiceMARK", 1, 1, 0)
with tab5:
    display_tab(df[df['연관 제품'] == 'VoiceDOC'].reset_index(drop=True), "VoiceDOC", 1, 0, 0)