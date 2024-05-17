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

def display_tab(dataframe, tab_label, customers, contracts, demos,unknown):
    col1, col2, col3, col4 = st.columns([3, 3, 3, 3])

    with col1:
        st.metric(label="고객", value=customers)
    with col2:
        st.metric(label="정식계약", value=contracts)
    with col3:
        st.metric(label="데모계약", value=demos)
    with col4:
        st.metric(label="파악불가", value=unknown)

    total_items = len(dataframe)
    total_pages = (total_items + items_per_page - 1) // items_per_page

    # CSS를 사용하여 입력 상자의 크기 및 정렬 조절
    st.markdown(f"""
        <style>
        .number-input-wrapper-{tab_label} {{
            display: flex;
            justify-content: left; /* 왼쪽 정렬 */
            align-items: center;
            margin: 10px 0;
        }}
        .number-input-wrapper-{tab_label} input {{
            width: 10px; /* 여기서 크기를 조절할 수 있습니다 */
            height: 40px; /* 여기서 높이를 조절할 수 있습니다 */
            font-size: 20px; /* 여기서 글꼴 크기를 조절할 수 있습니다 */
        }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="number-input-wrapper-{tab_label}">', unsafe_allow_html=True)
    page_number = st.number_input(f'Page number for {tab_label}', min_value=1, max_value=total_pages, step=1, value=1, key=tab_label)
    st.markdown('</div>', unsafe_allow_html=True)

    paged_df = paginate_data(dataframe, page_number, items_per_page)
    paged_df.index += 1

    st.dataframe(paged_df, height=table_height, width=table_width)
    st.write(f"Displaying rows {page_number * items_per_page - (items_per_page - 1)} to {min(page_number * items_per_page, total_items)} of {total_items}")





# 각 탭에 데이터프레임 및 페이징 기능 적용
with tab1:
    voiceemr_data = df[df['연관 제품'] == 'VoiceEMR'].reset_index(drop=True)
    voiceemr_data.index.name='구분'
    count_voiceemr = len(voiceemr_data)
    df.index.name = '구분'

    temp1 = len(df[df['계약관리'] == '정식'])
    temp2 = len(df[df['계약관리'] == '데모'])
    temp3 = len(df[df['계약관리'] == None])

    display_tab(voiceemr_data, "VoiceEMR", count_voiceemr, temp1, temp2,temp3)
with tab2:
    voiceenr_data = df[df['연관 제품'] == 'VoiceENR'].reset_index(drop=True)
    voiceenr_data.index.name='구분'
    count_voiceenr = len(voiceenr_data)

    temp1 = len(df[df['계약관리'] == '정식'])
    temp2 = len(df[df['계약관리'] == '데모'])
    temp3 = len(df[df['계약관리'] == "None"])

    display_tab(voiceenr_data, "VoiceENR", count_voiceenr, temp1, temp2,temp3)


with tab3:
    voicesdk_data= df[df['연관 제품'] == 'VoiceSDK'].reset_index(drop=True)
    voicesdk_data.index.name='구분'
    count_voicesdk = len(voicesdk_data)

    temp1 = len(df[df['계약관리'] == '정식'])
    temp2 = len(df[df['계약관리'] == '데모'])
    temp3 = len(df[df['계약관리'] == ""])
    display_tab(voicesdk_data, "VoiceSDK", count_voicesdk, temp1, temp2,temp3)


with tab4:
    voicemark_data= df[df['연관 제품'] == 'VoiceMARK'].reset_index(drop=True)
    voicemark_data.index.name='구분'
    count_voicemark = len(voicemark_data)

    temp1 = len(df[df['계약관리'] == '정식'])
    temp2 = len(df[df['계약관리'] == '데모'])
    temp3 = len(df[df['계약관리'] == None])
    display_tab(voicemark_data, "VoiceMARK", count_voicemark, temp1, temp2,temp3)


with tab5:
    voicedoc_data= df[df['연관 제품'] == 'VoiceDOC'].reset_index(drop=True)
    voicedoc_data.index.name='구분'
    count_voicedoc = len(voicedoc_data)

    temp1 = len(df[df['계약관리'] == '정식'])
    temp2 = len(df[df['계약관리'] == '데모'])
    temp3 = len(df[df['계약관리'] == None])
    display_tab(voicedoc_data, "VoiceDOC", count_voicedoc, temp1, temp2,temp3)