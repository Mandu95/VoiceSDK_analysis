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

# 세션 상태를 초기화하는 함수
def init_session_state(tab_label):
    if f'{tab_label}_filtered_df' not in st.session_state:
        st.session_state[f'{tab_label}_filtered_df'] = None
    if f'{tab_label}_page_number' not in st.session_state:
        st.session_state[f'{tab_label}_page_number'] = 1

# 탭메뉴 영역
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["VoiceEMR", "VoiceENR", "VoiceSDK", "VoiceMARK", "VoiceDOC"])

def display_tab(dataframe, tab_label, customers, contracts, demos, unknown):
    # 세션 상태 초기화
    init_session_state(tab_label)

    col1, col2, col3, col4 = st.columns([3, 3, 3, 3])

    # 텍스트와 버튼을 분리하여 표시
    with col1:
        st.write("고객")
        if st.button(f"{customers}", key=f"{tab_label}_고객"):
            st.session_state[f'{tab_label}_filtered_df'] = dataframe
            st.session_state[f'{tab_label}_page_number'] = 1

    with col2:
        st.write("정식계약")
        if st.button(f"{contracts}", key=f"{tab_label}_정식계약"):
            st.session_state[f'{tab_label}_filtered_df'] = dataframe[dataframe['계약관리'] == '정식']
            st.session_state[f'{tab_label}_page_number'] = 1

    with col3:
        st.write("데모계약")
        if st.button(f"{demos}", key=f"{tab_label}_데모계약"):
            st.session_state[f'{tab_label}_filtered_df'] = dataframe[dataframe['계약관리'] == '데모']
            st.session_state[f'{tab_label}_page_number'] = 1

    with col4:
        st.write("파악불가")
        if st.button(f"{unknown}", key=f"{tab_label}_파악불가"):
            st.session_state[f'{tab_label}_filtered_df'] = dataframe[dataframe['계약관리'].isnull()]
            st.session_state[f'{tab_label}_page_number'] = 1

    # 필터링된 데이터프레임이 세션 상태에 저장되어 있을 때만 표시
    if st.session_state[f'{tab_label}_filtered_df'] is not None:
        filtered_df = st.session_state[f'{tab_label}_filtered_df']
        total_items = len(filtered_df)
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
        page_number = st.number_input(
            f'Page number for {tab_label}', 
            min_value=1, 
            max_value=total_pages, 
            step=1, 
            value=st.session_state[f'{tab_label}_page_number'], 
            key=f'page_{tab_label}',
            on_change=lambda: st.session_state.update({f'{tab_label}_page_number': st.session_state[f'page_{tab_label}']})
        )
        st.markdown('</div>', unsafe_allow_html=True)

        paged_df = paginate_data(filtered_df, page_number, items_per_page)
        paged_df.index += 1

        st.dataframe(paged_df, height=table_height, width=table_width)
        st.write(f"Displaying rows {page_number * items_per_page - (items_per_page - 1)} to {min(page_number * items_per_page, total_items)} of {total_items}")




# 각 탭에 데이터프레임 및 페이징 기능 적용
with tab1:
    voiceemr_data = df[df['연관 제품'] == 'VoiceEMR'].reset_index(drop=True)
    voiceemr_data.index.name='구분'
    count_voiceemr = len(voiceemr_data)
    df.index.name = '구분'

    # 계약 관리가 "정식"인 데이터만 카운트
    temp1 = len(voiceemr_data[voiceemr_data['계약관리'] == '정식'])
    # 계약 관리가 "데모"인 데이터만 카운트
    temp2 = len(voiceemr_data[voiceemr_data['계약관리'] == '데모'])
    # 계약 관리가 비어있는 데이터만 카운트
    temp3 = len(voiceemr_data[voiceemr_data['계약관리'].isnull()])

    display_tab(voiceemr_data, "VoiceEMR", count_voiceemr, temp1, temp2,temp3)
with tab2:
    voiceenr_data = df[df['연관 제품'] == 'VoiceENR'].reset_index(drop=True)
    voiceenr_data.index.name='구분'
    count_voiceenr = len(voiceenr_data)

    # 계약 관리가 "정식"인 데이터만 카운트
    temp1 = len(voiceenr_data[voiceenr_data['계약관리'] == '정식'])
    # 계약 관리가 "데모"인 데이터만 카운트
    temp2 = len(voiceenr_data[voiceenr_data['계약관리'] == '데모'])
    # 계약 관리가 비어있는 데이터만 카운트
    temp3 = len(voiceenr_data[voiceenr_data['계약관리'].isnull()])

    display_tab(voiceenr_data, "VoiceENR", count_voiceenr, temp1, temp2,temp3)


with tab3:
    voicesdk_data= df[df['연관 제품'] == 'VoiceSDK'].reset_index(drop=True)
    voicesdk_data.index.name='구분'
    count_voicesdk = len(voicesdk_data)

    # 계약 관리가 "정식"인 데이터만 카운트
    temp1 = len(voicesdk_data[voicesdk_data['계약관리'] == '정식'])
    # 계약 관리가 "데모"인 데이터만 카운트
    temp2 = len(voicesdk_data[voicesdk_data['계약관리'] == '데모'])
    # 계약 관리가 비어있는 데이터만 카운트
    temp3 = len(voicesdk_data[voicesdk_data['계약관리'].isnull()])
    display_tab(voicesdk_data, "VoiceSDK", count_voicesdk, temp1, temp2,temp3)


with tab4:
    voicemark_data= df[df['연관 제품'] == 'VoiceMARK'].reset_index(drop=True)
    voicemark_data.index.name='구분'
    count_voicemark = len(voicemark_data)

    # 계약 관리가 "정식"인 데이터만 카운트
    temp1 = len(voicemark_data[voicemark_data['계약관리'] == '정식'])
    # 계약 관리가 "데모"인 데이터만 카운트
    temp2 = len(voicemark_data[voicemark_data['계약관리'] == '데모'])
    # 계약 관리가 비어있는 데이터만 카운트
    temp3 = len(voicemark_data[voicemark_data['계약관리'].isnull()])
    display_tab(voicemark_data, "VoiceMARK", count_voicemark, temp1, temp2,temp3)


with tab5:
    voicedoc_data= df[df['연관 제품'] == 'VoiceDOC'].reset_index(drop=True)
    voicedoc_data.index.name='구분'
    count_voicedoc = len(voicedoc_data)

    # 계약 관리가 "정식"인 데이터만 카운트
    temp1 = len(voicedoc_data[voicedoc_data['계약관리'] == '정식'])
    # 계약 관리가 "데모"인 데이터만 카운트
    temp2 = len(voicedoc_data[voicedoc_data['계약관리'] == '데모'])
    # 계약 관리가 비어있는 데이터만 카운트
    temp3 = len(voicedoc_data[voicedoc_data['계약관리'].isnull()])
    display_tab(voicedoc_data, "VoiceDOC", count_voicedoc, temp1, temp2,temp3)