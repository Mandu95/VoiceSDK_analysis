import streamlit as st
import pandas as pd
import data_process

st.set_page_config(layout="wide")

# 데이터 로드
df = data_process.df
url_data = data_process.url_df

# 모든 텍스트에 'AppleSDGothicNeoR00' 글꼴을 적용하는 CSS
st.markdown(
    """
    <style>
    @font-face {
        font-family: 'AppleSDGothicNeoR00';
        src: url('https://example.com/path/to/AppleSDGothicNeoR00.ttf') format('truetype'); /* 글꼴 파일 경로를 업데이트해야 합니다 */
    }
    html, body, [class*="css"] {
        font-family: 'AppleSDGothicNeoR00';
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

# 표 높이와 너비 동적으로 설정하는 함수


def get_table_dimensions():
    return 385, 2400  # 너비를 더 크게 설정


# 표의 높이와 너비 설정
table_height, table_width = get_table_dimensions()

# 페이지당 항목 수 설정
items_per_page = 10

# 데이터프레임을 페이징하는 함수


def paginate_data(dataframe, page_number, items_per_page):
    """
    데이터프레임을 페이지 번호에 따라 분할하여 반환하는 함수.
    """
    start_index = (page_number - 1) * items_per_page
    end_index = start_index + items_per_page
    paged_df = dataframe.iloc[start_index:end_index]

    # 인덱스를 1부터 시작하도록 설정 (범위를 데이터프레임의 길이에 맞추어 조정)
    paged_df.index = range(start_index + 1, start_index + 1 + len(paged_df))
    return paged_df

# 세션 상태를 초기화하는 함수


def init_session_state(tab_label):
    """
    각 탭에 대해 세션 상태를 초기화하는 함수.
    """
    if f'{tab_label}_filtered_df' not in st.session_state:
        st.session_state[f'{tab_label}_filtered_df'] = df  # 기본값은 전체 데이터프레임
    if f'{tab_label}_page_number' not in st.session_state:
        st.session_state[f'{tab_label}_page_number'] = 1  # 기본 페이지 번호는 1

# "계약잔여일"이 90일보다 작은 경우 노란색으로 강조하는 함수


def highlight_remaining_days(val):
    """
    '계약잔여일' 값이 90일보다 작은 경우 셀 배경색을 노란색으로 설정하는 함수.
    """
    try:
        if int(val) < 90:
            return 'background-color: yellow'
    except (ValueError, TypeError):
        return ''
    return ''

# 데이터 프레임을 표시하고 페이징하는 함수


def display_paginated_table(dataframe, tab_label):
    """
    데이터프레임을 페이지 단위로 나누어 표시하는 함수.
    """
    init_session_state(tab_label)

    total_items = len(dataframe)
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

    paged_df = paginate_data(dataframe, page_number, items_per_page)

    # "계약잔여일" 강조 표시 적용
    styled_df = paged_df.style.applymap(
        highlight_remaining_days, subset=['계약잔여일'])
    st.dataframe(styled_df, height=table_height, width=table_width)
    st.write(
        f"Displaying rows {(page_number - 1) * items_per_page + 1} to {min(page_number * items_per_page, total_items)} of {total_items}")

# 데이터 탭을 표시하는 함수


def display_tab(dataframe, tab_label, customers, contracts, demos, send_docu, unknown):
    """
    각 탭에 대한 데이터를 필터링하고 표시하는 함수.
    """
    init_session_state(tab_label)

    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])

    with col1:
        st.write("전체")
        if st.button(f"{customers}", key=f"{tab_label}_전체"):
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
        st.write("견적서 발송")
        if st.button(f"{send_docu}", key=f"{tab_label}_견적발송"):
            st.session_state[f'{tab_label}_filtered_df'] = dataframe[dataframe['상태'] == '견적발송']
            st.session_state[f'{tab_label}_page_number'] = 1

    with col5:
        st.write("파악불가")
        if st.button(f"{unknown}", key=f"{tab_label}_파악불가"):
            st.session_state[f'{tab_label}_filtered_df'] = dataframe[dataframe['계약관리'].isnull(
            ) & (dataframe['상태'] != '견적발송')]
            st.session_state[f'{tab_label}_page_number'] = 1

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
        display_paginated_table(filtered_df, tab_label)


# 전체 데이터에 페이징 적용
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["전체", "VoiceEMR", "VoiceENR", "VoiceSDK", "VoiceMARK", "VoiceDOC"])

with tab1:
    all_data = df.reset_index(drop=True)
    all_data.index = all_data.index + 1
    all_data.index.name = 'No'
    display_paginated_table(all_data, "전체")

# 각 탭에 데이터프레임 및 페이징 기능 적용


def setup_tab(tab, product_name, tab_label):
    """
    각 탭에 데이터를 설정하고 표시하는 함수.
    """
    product_data = df[df['연관 제품'] == product_name].reset_index(drop=True)
    product_data.index = product_data.index + 1
    product_data.index.name = 'No'

    count_total = len(product_data)
    count_contracts = len(
        product_data[product_data['계약관리'].str.contains('정식', na=False)])
    count_demos = len(
        product_data[product_data['계약관리'].str.contains('데모', na=False)])
    send_docu = len(
        product_data[product_data['상태'].str.contains('견적발송', na=False)])
    count_unknown = len(
        product_data[product_data['계약관리'].isnull() & (product_data['상태'] != '견적발송')])

    with tab:
        display_tab(product_data, tab_label, count_total,
                    count_contracts, count_demos, send_docu, count_unknown)


# 각 탭에 대해 setup_tab 함수 호출
setup_tab(tab2, 'VoiceEMR', 'VoiceEMR')
setup_tab(tab3, 'VoiceENR', 'VoiceENR')
setup_tab(tab4, 'VoiceSDK', 'VoiceSDK')
setup_tab(tab5, 'VoiceMARK', 'VoiceMARK')
setup_tab(tab6, 'VoiceDOC', 'VoiceDOC')
