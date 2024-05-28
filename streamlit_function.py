import streamlit as st
import pandas as pd


def get_table_dimensions():
    """표 높이와 너비 동적으로 설정하는 함수"""
    return 800, 2400  # 더 큰 높이 설정


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


def display_html_table(dataframe, tab_label, page_number, table_height, table_width, items_per_page):
    """데이터 프레임을 HTML로 변환하여 표시하는 함수"""
    if '페이지URL' in dataframe.columns:
        if '업체 이름' in dataframe.columns:
            dataframe['업체 이름'] = dataframe.apply(
                lambda row: f'<a href="{row["페이지URL"]}" style="color: black;">{row["업체 이름"]}</a>', axis=1)
        if '계약명' in dataframe.columns:
            dataframe['계약명'] = dataframe.apply(
                lambda row: f'<a href="{row["페이지URL"]}" style="color: black;">{row["계약명"]}</a>', axis=1)
        dataframe = dataframe.drop(columns=['페이지URL'])

    if '사본링크' in dataframe.columns:
        dataframe['사본링크'] = dataframe.apply(
            lambda row: f'<a href="{row["사본링크"]}" style="color: black;">계약서 확인</a>', axis=1)

    dataframe = dataframe.drop(
        columns=["제품 현황 관리", "제품", "계약구분"], errors='ignore')

    # 특정 열의 값을 금액 단위로 포맷팅
    currency_columns = ['라이선스 총액', '계약단가', '계약총액']
    for col in currency_columns:
        if col in dataframe.columns:
            dataframe[col] = dataframe[col].apply(format_currency)

    paged_df = paginate_data(dataframe, page_number, items_per_page)
    styled_df = paged_df.style.set_table_styles(
        [{
            'selector': 'th',
            'props': [('text-align', 'center')]
        }]
    ).set_properties(**{'text-align': 'left'})

    table_html = styled_df.to_html(escape=False, index=False)
    table_html = f'''
    <div style="height: {table_height}px; width: {table_width}px; overflow: auto;">
        {table_html}
    </div>
    '''

    st.write(table_html, unsafe_allow_html=True)
    st.write(
        f"Displaying rows {(page_number - 1) * items_per_page + 1} to {min(page_number * items_per_page, len(dataframe))} of {len(dataframe)}")


def display_html_table_for_other_docs(dataframe, tab_label, items_per_page):
    """기타 문서 관리용 데이터 프레임을 HTML로 변환하여 표시하는 함수"""
    if f'{tab_label}_filtered_df' not in st.session_state:
        st.session_state[f'{tab_label}_filtered_df'] = dataframe
    if f'{tab_label}_page_number' not in st.session_state:
        st.session_state[f'{tab_label}_page_number'] = 1

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

    if '발송 대상' in paged_df.columns:
        paged_df = paged_df.drop(columns=['발송 대상'])
    if '사본링크' in paged_df.columns:
        paged_df['문서 확인하기'] = paged_df['사본링크'].apply(
            lambda x: f'<a href="{x}" target="_blank">문서 확인하기</a>')
        paged_df = paged_df.drop(columns=['사본링크'])

    if '페이지URL' in paged_df.columns:
        paged_df['문서이름'] = paged_df.apply(
            lambda row: f'<a href="{row["페이지URL"]}" style="color: black;">{row["문서이름"]}</a>', axis=1)
        paged_df = paged_df.drop(columns=['페이지URL'])

    if '제품' in paged_df.columns:
        paged_df = paged_df.drop(columns=['제품'])

    currency_columns = ['라이선스 총액', '계약단가', '계약총액']
    for col in currency_columns:
        if col in paged_df.columns:
            paged_df[col] = paged_df[col].apply(format_currency)

    if '라이선스 수' in paged_df.columns:
        paged_df['라이선스 수'] = paged_df['라이선스 수'].apply(format_license_count)

    if '제품' in paged_df.columns:
        paged_df['제품'] = paged_df['제품'].apply(format_product_list)

    paged_df = paged_df.applymap(str)

    table_height, table_width = get_table_dimensions()

    styled_df = paged_df.style.set_table_styles(
        [{
            'selector': 'th',
            'props': [('text-align', 'center')]
        }]
    ).set_properties(**{'text-align': 'left'})

    table_html = styled_df.to_html(escape=False, index=False)
    table_html = f'''
    <div style="height: {table_height}px; width: {table_width}px; overflow: auto;">
        {table_html}
    </div>
    '''

    st.write(table_html, unsafe_allow_html=True)
    st.write(
        f"Displaying rows {(page_number - 1) * items_per_page + 1} to {min(page_number * items_per_page, total_items)} of {total_items}"
    )


def display_tab(df, dataframe, tab_label, items_per_page):
    """데이터 탭을 표시하고 검색 기능 추가"""
    init_session_state(df, tab_label)
    search_query = st.session_state['search_query']

    col1, col2 = st.columns([8, 2])

    with col1:
        search_query = st.text_input(
            "", search_query, placeholder="업체 이름 또는 병원 이름을 입력해주세요", key='search_input')
        st.session_state['search_query'] = search_query

    with col2:
        tab_label = st.selectbox(
            "제품 구분",
            ["전체", "VoiceEMR", "VoiceENR", "VoiceSDK", "VoiceMARK", "VoiceDOC"],
            key='select_tab'
        )

    if tab_label == "전체":
        filtered_data = dataframe
    else:
        filtered_data = dataframe[dataframe['연관 제품'].apply(
            lambda x: tab_label in x if isinstance(x, list) else tab_label == x)]

    if search_query:
        filtered_data = filtered_data[filtered_data['업체 이름'].str.contains(
            search_query, case=False, na=False)]

    total_items = len(filtered_data)
    total_pages = max(
        1, (total_items + items_per_page - 1) // items_per_page)

    col3, col4 = st.columns([10, 1])
    with col4:
        page_number = st.number_input(
            f'Page number for {tab_label}',
            min_value=1,
            max_value=total_pages,
            step=1,
            value=st.session_state[f'{tab_label}_page_number'],
            key=f'page_{tab_label}'
        )
        st.session_state[f'{tab_label}_page_number'] = page_number

    if filtered_data.empty:
        st.markdown("<div class='no-data'>데이터가 없습니다</div>",
                    unsafe_allow_html=True)
    else:
        table_height, table_width = get_table_dimensions()
        display_html_table(filtered_data, tab_label, page_number,
                           table_height, table_width, items_per_page)
