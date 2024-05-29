import streamlit as st
import pandas as pd


def get_table_dimensions():
    """표 높이와 너비 동적으로 설정하는 함수"""
    return '100%', '100%'  # 너비와 높이를 100%로 설정하여 웹 페이지 크기에 맞춤


def paginate_data(dataframe, page_number, items_per_page):
    """
    데이터프레임을 페이지 번호에 따라 분할하여 반환하는 함수.
    """
    start_index = (page_number - 1) * items_per_page
    end_index = start_index + items_per_page
    paged_df = dataframe.iloc[start_index:end_index]
    paged_df.index = range(
        start_index + 1, start_index + 1 + len(paged_df))
    return paged_df


def init_session_state(df, tab_label):
    """세션 상태를 초기화하는 함수"""
    if f'{tab_label}_filtered_df' not in st.session_state:
        st.session_state[f'{tab_label}_filtered_df'] = df
    if f'{tab_label}_page_number' not in st.session_state:
        st.session_state[f'{tab_label}_page_number'] = 1
    if 'search_query' not in st.session_state:
        st.session_state['search_query'] = ''


def highlight_remaining_days(val):
    """계약잔여일이 90일보다 작은 경우 노란색으로 강조하는 함수"""
    try:
        if int(val) < 90:
            return 'background-color: yellow'
    except (ValueError, TypeError):
        return ''
    return ''


def format_currency(value):
    """특정 열의 값을 금액 단위로 포맷팅하는 함수"""
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return value


def format_license_count(value):
    """'라이선스 수' 열의 값을 일반 숫자 텍스트로 포맷팅하는 함수 (소숫점 제거)"""
    try:
        return f"{int(value)}"
    except (ValueError, TypeError):
        return value


def format_product_list(value):
    """'제품' 열의 리스트 형태 값을 텍스트로 나열"""
    if isinstance(value, list):
        return ", ".join(value)
    return value


def ensure_required_columns(dataframe):
    """필요한 열이 존재하지 않을 경우 기본값을 추가하는 함수"""
    required_columns = {
        '페이지URL': '',
        '사본링크': '',
        '발송 대상': '',
        '라이선스 총액': 0,
        '계약단가': 0,
        '계약총액': 0,
        '라이선스 수': 0
    }
    for column, default_value in required_columns.items():
        if column not in dataframe.columns:
            dataframe[column] = default_value
    return dataframe


def display_html_table(dataframe, tab_label, items_per_page, search_query="", selected_product="전체"):
    """데이터 프레임을 HTML로 변환하여 표시하는 함수"""

    # Ensure required columns
    dataframe = ensure_required_columns(dataframe)

    # Initialize session state
    if f'{tab_label}_filtered_df' not in st.session_state:
        st.session_state[f'{tab_label}_filtered_df'] = dataframe
    if f'{tab_label}_page_number' not in st.session_state:
        st.session_state[f'{tab_label}_page_number'] = 1

    # Filter based on search query
    if search_query:
        dataframe = dataframe[dataframe['업체 이름'].str.contains(
            search_query, case=False, na=False)]

    # Filter based on selected product
    if selected_product != "전체":
        dataframe = dataframe[dataframe['연관 제품'].apply(
            lambda x: selected_product in x if isinstance(x, list) else selected_product == x)]

    total_items = len(dataframe)
    total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)

    col1, col2 = st.columns([10, 1])
    with col2:
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

    # Drop specific columns and add links based on tab_label
    if '발송 대상' in paged_df.columns:
        paged_df = paged_df.drop(columns=['발송 대상'])
    if '사본링크' in paged_df.columns:
        paged_df['문서확인'] = paged_df['사본링크'].apply(
            lambda x: f'<a href="{x}" target="_blank" style="color: black;">문서 확인하기</a>')
        paged_df = paged_df.drop(columns=['사본링크'])
    if '페이지URL' in paged_df.columns:
        if tab_label == "계약서 관리":
            paged_df['계약명'] = paged_df.apply(
                lambda row: f'<a href="{row["페이지URL"]}" style="color: black;">{row["계약명"]}</a>', axis=1)
        elif tab_label == "제품 현황 관리":
            paged_df['업체 이름'] = paged_df.apply(
                lambda row: f'<a href="{row["페이지URL"]}" style="color: black;">{row["업체 이름"]}</a>', axis=1)
        paged_df = paged_df.drop(columns=['페이지URL'])
    if '제품' in paged_df.columns:
        paged_df = paged_df.drop(columns=['제품'])

    # Format currency and license count
    currency_columns = ['라이선스 총액', '계약단가', '계약총액']
    for col in currency_columns:
        if col in paged_df.columns:
            paged_df[col] = paged_df[col].apply(format_currency)
    if '라이선스 수' in paged_df.columns:
        paged_df['라이선스 수'] = paged_df['라이선스 수'].apply(format_license_count)

    # Apply HTML table styles and convert to HTML
    paged_df = paged_df.applymap(str)
    table_height, table_width = get_table_dimensions()
    styled_df = paged_df.style.set_table_styles(
        [{'selector': 'th', 'props': [('text-align', 'center')]}]
    ).set_properties(**{'text-align': 'left'})

    table_html = styled_df.to_html(escape=False, index=False)
    table_html = f'''
    <div style="height: {table_height}; width: {table_width}; overflow: auto;">
        <style>
            table {{
                width: 100%;
                table-layout: auto;
            }}
            th, td {{
                text-align: left;
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            td {{
                word-wrap: break-word;
                white-space: normal;
            }}
        </style>
        {table_html}
    </div>
    '''

    st.write(table_html, unsafe_allow_html=True)
    st.write(
        f"Displaying rows {(page_number - 1) * items_per_page + 1} to {min(page_number * items_per_page, total_items)} of {total_items}"
    )


def display_tab(dataframe, tab_label, items_per_page):
    """데이터 탭을 표시하고 검색 기능 추가"""
    init_session_state(dataframe, tab_label)
    search_query = st.session_state.get('search_query', "")

    col1, col2 = st.columns([8, 2])

    with col1:
        search_query = st.text_input(
            "", search_query, placeholder="업체 이름 또는 병원 이름을 입력해주세요", key='search_input')
        st.session_state['search_query'] = search_query

    with col2:
        selected_product = st.selectbox("제품 구분", [
                                        "전체", "VoiceEMR", "VoiceENR", "VoiceSDK", "VoiceMARK", "VoiceDOC"], key='select_tab')

    display_html_table(dataframe, tab_label, items_per_page,
                       search_query, selected_product)
