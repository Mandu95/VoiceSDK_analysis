import streamlit as st
import data_process

# 페이지 레이아웃 설정
st.set_page_config(layout="wide")

# 데이터 로드
df = data_process.df
URL = data_process.url_df

def make_clickable(name, url):
    """하이퍼링크를 만드는 함수"""
    return f'<a href="{url}" target="_blank">{name}</a>'

# "업체이름" 열의 각 행에 해당하는 URL을 하이퍼링크로 변환
if '업체이름' in df.columns and 'URL' in URL.columns:
    df['업체이름'] = df.apply(lambda x: make_clickable(x['업체이름'], URL.loc[x.name, 'URL']), axis=1)

# 페이지 상단 영역
st.subheader("PuzzleAI's 사업부 대시보드")
st.subheader("Notion DB를 기준으로 분석한 자료입니다.:sunglasses:")

# 테이블 크기 설정
table_height = 400  # 테이블 높이 (픽셀 단위)
table_width = 2000  # 테이블 너비 (픽셀 단위)
items_per_page = 10  # 페이지당 항목 수 설정

def paginate_data(dataframe, page_number, items_per_page):
    """데이터프레임을 페이지 단위로 나누는 함수"""
    start_index = (page_number - 1) * items_per_page
    end_index = start_index + items_per_page
    return dataframe.iloc[start_index:end_index]

def init_session_state(tab_label):
    """세션 상태를 초기화하는 함수"""
    if f'{tab_label}_filtered_df' not in st.session_state:
        st.session_state[f'{tab_label}_filtered_df'] = None
    if f'{tab_label}_page_number' not in st.session_state:
        st.session_state[f'{tab_label}_page_number'] = 1

def display_tab(dataframe, tab_label, customers, contracts, demos, unknown):
    """탭 내용을 표시하는 함수"""
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
        
        if filtered_df.empty:
            st.markdown(
                """
                <style>
                .no-data {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 300px;
                    font-size: 24px;
                    color: black;
                }
                </style>
                <div class="no-data">데이터가 없습니다</div>
                """, unsafe_allow_html=True)
        else:
            total_items = len(filtered_df)
            total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)

            # 페이지 번호 입력 상자를 표 상단 맨 오른쪽에 배치
            col5, col6 = st.columns([10, 1])
            with col6:
                page_number = st.number_input(
                    f'Page number for {tab_label}', 
                    min_value=1, 
                    max_value=total_pages, 
                    step=1, 
                    value=st.session_state[f'{tab_label}_page_number'], 
                    key=f'page_{tab_label}'
                )
                st.session_state[f'{tab_label}_page_number'] = page_number

            paged_df = paginate_data(filtered_df, st.session_state[f'{tab_label}_page_number'], items_per_page)
            paged_df.index += 1

            # CSS 스타일 추가
            st.markdown(
                """
                <style>
                .dataframe td, .dataframe th {
                    font-size: 12px; /* 글자 크기 조정 */
                    text-align: center; /* 중앙 정렬 */
                }
                .dataframe td {
                    white-space: nowrap; /* 한 줄로 표시 */
                    overflow: hidden;
                    text-overflow: ellipsis;
                    max-width: 200px;
                }
                .dataframe {
                    table-layout: auto;
                    width: 100%;
                }
                </style>
                """, unsafe_allow_html=True)

            # HTML 허용하여 데이터프레임 표시
            st.markdown(paged_df.to_html(escape=False, index=True, index_names=True), unsafe_allow_html=True)
            st.write(f"Displaying rows {st.session_state[f'{tab_label}_page_number'] * items_per_page - (items_per_page - 1)} to {min(st.session_state[f'{tab_label}_page_number'] * items_per_page, total_items)} of {total_items}")

# 탭메뉴 영역
tab1, tab2, tab3, tab4, tab5 = st.tabs(["VoiceEMR", "VoiceENR", "VoiceSDK", "VoiceMARK", "VoiceDOC"])

# 각 탭에 데이터프레임 및 페이징 기능 적용
with tab1:
    voiceemr_data = df[df['연관 제품'] == 'VoiceEMR'].reset_index(drop=True)
    voiceemr_data.index.name = 'No'
    count_voiceemr = len(voiceemr_data)

    # 계약 관리가 "정식"인 데이터만 카운트
    temp1 = len(voiceemr_data[voiceemr_data['계약관리'] == '정식'])
    # 계약 관리가 "데모"인 데이터만 카운트
    temp2 = len(voiceemr_data[voiceemr_data['계약관리'] == '데모'])
    # 계약 관리가 비어있는 데이터만 카운트
    temp3 = len(voiceemr_data[voiceemr_data['계약관리'].isnull()])

    display_tab(voiceemr_data, "VoiceEMR", count_voiceemr, temp1, temp2, temp3)

with tab2:
    voiceenr_data = df[df['연관 제품'] == 'VoiceENR'].reset_index(drop=True)
    voiceenr_data.index.name = 'No'
    count_voiceenr = len(voiceenr_data)

    # 계약 관리가 "정식"인 데이터만 카운트
    temp1 = len(voiceenr_data[voiceenr_data['계약관리'] == '정식'])
    # 계약 관리가 "데모"인 데이터만 카운트
    temp2 = len(voiceenr_data[voiceenr_data['계약관리'] == '데모'])
    # 계약 관리가 비어있는 데이터만 카운트
    temp3 = len(voiceenr_data[voiceenr_data['계약관리'].isnull()])

    display_tab(voiceenr_data, "VoiceENR", count_voiceenr, temp1, temp2, temp3)

with tab3:
    voicesdk_data = df[df['연관 제품'] == 'VoiceSDK'].reset_index(drop=True)
    voicesdk_data.index.name = 'No'
    count_voicesdk = len(voicesdk_data)

    # 계약 관리가 "정식"인 데이터만 카운트
    temp1 = len(voicesdk_data[voicesdk_data['계약관리'] == '정식'])
    # 계약 관리가 "데모"인 데이터만 카운트
    temp2 = len(voicesdk_data[voicesdk_data['계약관리'] == '데모'])
    # 계약 관리가 비어있는 데이터만 카운트
    temp3 = len(voicesdk_data[voicesdk_data['계약관리'].isnull()])

    display_tab(voicesdk_data, "VoiceSDK", count_voicesdk, temp1, temp2, temp3)

with tab4:
    voicemark_data = df[df['연관 제품'] == 'VoiceMARK'].reset_index(drop=True)
    voicemark_data.index.name = 'No'
    count_voicemark = len(voicemark_data)

    # 계약 관리가 "정식"인 데이터만 카운트
    temp1 = len(voicemark_data[voicemark_data['계약관리'] == '정식'])
    # 계약 관리가 "데모"인 데이터만 카운트
    temp2 = len(voicemark_data[voicemark_data['계약관리'] == '데모'])
    # 계약 관리가 비어있는 데이터만 카운트
    temp3 = len(voicemark_data[voicemark_data['계약관리'].isnull()])

    display_tab(voicemark_data, "VoiceMARK", count_voicemark, temp1, temp2, temp3)

with tab5:
    voicedoc_data = df[df['연관 제품'] == 'VoiceDOC'].reset_index(drop=True)
    voicedoc_data.index.name = 'No'
    count_voicedoc = len(voicedoc_data)

    # 계약 관리가 "정식"인 데이터만 카운트
    temp1 = len(voicedoc_data[voicedoc_data['계약관리'] == '정식'])
    # 계약 관리가 "데모"인 데이터만 카운트
    temp2 = len(voicedoc_data[voicedoc_data['계약관리'] == '데모'])
    # 계약 관리가 비어있는 데이터만 카운트
    temp3 = len(voicedoc_data[voicedoc_data['계약관리'].isnull()])

    display_tab(voicedoc_data, "VoiceDOC", count_voicedoc, temp1, temp2, temp3)
