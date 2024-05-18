import streamlit as st
import data_process

st.set_page_config(layout="wide")

df = data_process.df
url_data = data_process.url_df

# 페이지 레이아웃 설정
col_header, col_buttons = st.columns([8, 2])
with col_header:
    st.subheader("PuzzleAI's 사업부 대시보드")

with col_buttons:
    st.markdown(
        """
        <style>
        .button-container {
            display: flex;
            justify-content: flex-end;
            align-items: center;
        }
        .button {
            padding: 10px 24px;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 12px;
            transition-duration: 0.4s;
            border: none;
            color: white;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            min-width: 150px; /* 모든 버튼의 최소 너비를 동일하게 설정 */
        }
        .notion-button {
            background-color: #00bfa6; /* Notion 시그니처 색상 */
        }
        .notion-button:hover {
            background-color: white;
            color: black;
            border: 2px solid #00bfa6;
        }
        .onedrive-button {
            background-color: #0078d4; /* OneDrive 시그니처 색상 */
        }
        .onedrive-button:hover {
            background-color: white;
            color: black;
            border: 2px solid #0078d4;
        }
        </style>
        <div class="button-container">
            <a href="https://www.notion.so/puzzleai/69aeff6ca32d4466ad4748dde3939e8b?v=3de75aac58cd42978178f02e0b3d7707" target="_blank">
                <button class="button notion-button">고객 관리</button>
            </a>
            <a href="https://puszleai-my.sharepoint.com/:f:/g/personal/mandu95_puzzle-ai_com/Egh0NiS6DdRPo8ej06sndswB7z9FOPB7OIAArnEenTObvw?e=igldVp" target="_blank">
                <button class="button onedrive-button">사업부 공유폴더</button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("Notion DB를 기준으로 분석한 자료입니다.:sunglasses:")

table_height = 400  # 테이블 높이 (픽셀 단위)
table_width = 2000  # 테이블 너비 (픽셀 단위)
items_per_page = 10  # 페이지당 항목 수 설정

def paginate_data(dataframe, page_number, items_per_page):
    """데이터프레임을 페이지별로 나누는 함수"""
    start_index = (page_number - 1) * items_per_page
    end_index = start_index + items_per_page
    return dataframe.iloc[start_index:end_index]

def init_session_state(tab_label):
    """세션 상태를 초기화하는 함수"""
    if f'{tab_label}_filtered_df' not in st.session_state:
        st.session_state[f'{tab_label}_filtered_df'] = None
    if f'{tab_label}_page_number' not in st.session_state:
        st.session_state[f'{tab_label}_page_number'] = 1

# 탭 메뉴 설정
tab1, tab2, tab3, tab4, tab5 = st.tabs(["VoiceEMR", "VoiceENR", "VoiceSDK", "VoiceMARK", "VoiceDOC"])

def display_tab(dataframe, tab_label, customers, contracts, demos, unknown):
    """각 탭을 표시하는 함수"""
    init_session_state(tab_label)

    col1, col2, col3, col4 = st.columns([3, 3, 3, 3])

    with col1:
        st.write("고객")
        if st.button(f"{customers}", key=f"{tab_label}_고객"):
            st.session_state[f'{tab_label}_filtered_df'] = dataframe
            st.session_state[f'{tab_label}_page_number'] = 1
            st.session_state[f'{tab_label}_start_index'] = 1

    with col2:
        st.write("정식계약")
        if st.button(f"{contracts}", key=f"{tab_label}_정식계약"):
            st.session_state[f'{tab_label}_filtered_df'] = dataframe[dataframe['계약관리'] == '정식']
            st.session_state[f'{tab_label}_page_number'] = 1
            st.session_state[f'{tab_label}_start_index'] = 1

    with col3:
        st.write("데모계약")
        if st.button(f"{demos}", key=f"{tab_label}_데모계약"):
            st.session_state[f'{tab_label}_filtered_df'] = dataframe[dataframe['계약관리'] == '데모']
            st.session_state[f'{tab_label}_page_number'] = 1
            st.session_state[f'{tab_label}_start_index'] = 1

    with col4:
        st.write("파악불가")
        if st.button(f"{unknown}", key=f"{tab_label}_파악불가"):
            st.session_state[f'{tab_label}_filtered_df'] = dataframe[dataframe['계약관리'].isnull()]
            st.session_state[f'{tab_label}_page_number'] = 1
            st.session_state[f'{tab_label}_start_index'] = 1

    if st.session_state[f'{tab_label}_filtered_df'] is not None:
        filtered_df = st.session_state[f'{tab_label}_filtered_df']

        if filtered_df.empty:
            st.markdown(
                """
                <style>
                .no-data {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 300px;
                    font-size: 36px;
                    color: red;
                }
                </style>
                <div class="no-data">데이터가 없습니다</div>
                """, unsafe_allow_html=True)
        else:
            total_items = len(filtered_df)
            total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)

            col5, col6 = st.columns([11, 1])
            with col5:
                st.write(f'Page number for {tab_label}')
            with col6:
                page_number = st.number_input(
                    '',
                    min_value=1,
                    max_value=total_pages,
                    step=1,
                    value=st.session_state[f'{tab_label}_page_number'],
                    key=f'page_{tab_label}'
                )
                st.session_state[f'{tab_label}_page_number'] = page_number

            paged_df = paginate_data(filtered_df, st.session_state[f'{tab_label}_page_number'], items_per_page)
            start_index = st.session_state.get(f'{tab_label}_start_index', 1)
            paged_df.index = range(start_index, start_index + len(paged_df))

            def highlight_remaining_days(val):
                """계약잔여일이 60일 이하인 경우 색상 강조"""
                try:
                    if int(val) < 60:
                        return 'background-color: yellow'
                except ValueError:
                    pass
                return ''

            styled_df = paged_df.style.applymap(highlight_remaining_days, subset=['계약잔여일'])
            
            st.dataframe(styled_df, height=table_height, width=table_width)
            st.write(f"Displaying rows {st.session_state[f'{tab_label}_page_number'] * items_per_page - (items_per_page - 1)} to {min(st.session_state[f'{tab_label}_page_number'] * items_per_page, total_items)} of {total_items}")

            st.session_state[f'{tab_label}_start_index'] = start_index + len(paged_df)

# 각 탭에 데이터프레임 및 페이징 기능 적용
with tab1:
    voiceemr_data = df[df['연관 제품'] == 'VoiceEMR'].reset_index(drop=True)
    voiceemr_data.index.name = 'No'
    count_voiceemr = len(voiceemr_data)

    temp1 = len(voiceemr_data[voiceemr_data['계약관리'].str.contains('정식', na=False)])
    temp2 = len(voiceemr_data[voiceemr_data['계약관리'].str.contains('데모', na=False)])
    temp3 = len(voiceemr_data[voiceemr_data['계약관리'].isnull()])

    display_tab(voiceemr_data, "VoiceEMR", count_voiceemr, temp1, temp2, temp3)

with tab2:
    voiceenr_data = df[df['연관 제품'] == 'VoiceENR'].reset_index(drop=True)
    voiceenr_data.index.name = 'No'
    count_voiceenr = len(voiceenr_data)

    temp1 = len(voiceenr_data[voiceenr_data['계약관리'].str.contains('정식', na=False)])
    temp2 = len(voiceenr_data[voiceenr_data['계약관리'].str.contains('데모', na=False)])
    temp3 = len(voiceenr_data[voiceenr_data['계약관리'].isnull()])

    display_tab(voiceenr_data, "VoiceENR", count_voiceenr, temp1, temp2, temp3)

with tab3:
    voicesdk_data = df[df['연관 제품'] == 'VoiceSDK'].reset_index(drop=True)
    voicesdk_data.index.name = 'No'
    count_voicesdk = len(voicesdk_data)

    temp1 = len(voicesdk_data[voicesdk_data['계약관리'].str.contains('정식', na=False)])
    temp2 = len(voicesdk_data[voicesdk_data['계약관리'].str.contains('데모', na=False)])
    temp3 = len(voicesdk_data[voicesdk_data['계약관리'].isnull()])

    display_tab(voicesdk_data, "VoiceSDK", count_voicesdk, temp1, temp2, temp3)

with tab4:
    voicemark_data = df[df['연관 제품'] == 'VoiceMARK'].reset_index(drop=True)
    voicemark_data.index.name = 'No'
    count_voicemark = len(voicemark_data)

    temp1 = len(voicemark_data[voicemark_data['계약관리'].str.contains('정식', na=False)])
    temp2 = len(voicemark_data[voicemark_data['계약관리'].str.contains('데모', na=False)])
    temp3 = len(voicemark_data[voicemark_data['계약관리'].isnull()])

    display_tab(voicemark_data, "VoiceMARK", count_voicemark, temp1, temp2, temp3)

with tab5:
    voicedoc_data = df[df['연관 제품'] == 'VoiceDOC'].reset_index(drop=True)
    voicedoc_data.index.name = 'No'
    count_voicedoc = len(voicedoc_data)

    temp1 = len(voicedoc_data[voicedoc_data['계약관리'].str.contains('정식', na=False)])
    temp2 = len(voicedoc_data[voicedoc_data['계약관리'].str.contains('데모', na=False)])
    temp3 = len(voicedoc_data[voicedoc_data['계약관리'].isnull()])

    display_tab(voicedoc_data, "VoiceDOC", count_voicedoc, temp1, temp2, temp3)
