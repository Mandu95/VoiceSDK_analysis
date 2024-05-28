import streamlit as st
import pandas as pd
from Data_anal import contract_manage  # 데이터 로드
import streamlit_function as sf  # streamlit_function 모듈 임포트


def show_contract_management():

    st.subheader("계약서 관리")
    st.write("정식/데모 계약서를 확인할 수 있습니다.:sunglasses:")

    # 표 높이와 너비 동적으로 설정하는 함수
    def get_table_dimensions():
        return 385, 2400  # 너비를 더 크게 설정

    table_height, table_width = get_table_dimensions()  # 표의 높이와 너비 설정
    items_per_page = 10  # 페이지당 항목 수 설정

    # 특정 열의 값을 금액 단위로 포맷팅하는 함수
    def format_currency(value):
        try:
            return f"{int(value):,}"
        except (ValueError, TypeError):
            return value

    # 데이터프레임을 페이지 번호에 따라 분할하여 반환하는 함수
    def paginate_data(dataframe, page_number, items_per_page):
        start_index = (page_number - 1) * items_per_page
        end_index = start_index + items_per_page
        paged_df = dataframe.iloc[start_index:end_index]
        paged_df.index = range(
            start_index + 1, start_index + 1 + len(paged_df))
        return paged_df

    # 세션 상태를 초기화하는 함수
    def init_session_state(tab_label):
        if f'{tab_label}_filtered_df' not in st.session_state:
            st.session_state[f'{tab_label}_filtered_df'] = contract_manage
        if f'{tab_label}_page_number' not in st.session_state:
            st.session_state[f'{tab_label}_page_number'] = 1
        if f'search_query_{tab_label}' not in st.session_state:
            st.session_state[f'search_query_{tab_label}'] = ''

    # 데이터 프레임을 HTML로 변환하여 표시하는 함수
    def display_html_table(dataframe, tab_label):
        if '페이지URL' in dataframe.columns:
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

        # 표의 높이와 너비 설정
        table_height, table_width = get_table_dimensions()

        # 데이터프레임을 HTML로 변환하여 스타일 추가 (열 이름만 가운데 정렬)
        styled_df = dataframe.style.set_table_styles(
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
            f"Displaying rows {(st.session_state[f'{tab_label}_page_number'] - 1) * items_per_page + 1} to {min(st.session_state[f'{tab_label}_page_number'] * items_per_page, len(dataframe))} of {len(dataframe)}")

    # 데이터 프레임을 표시하고 페이징하는 함수
    def display_paginated_table(dataframe, tab_label):
        init_session_state(tab_label)
        total_items = len(dataframe)
        total_pages = max(
            1, (total_items + items_per_page - 1) // items_per_page)

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

        if '계약잔여일' in paged_df.columns:
            styled_df = paged_df.style.applymap(
                sf.highlight_remaining_days, subset=['계약잔여일'])
        else:
            styled_df = paged_df

        display_html_table(styled_df, tab_label)

    # 데이터 탭을 표시하고 검색 기능 추가
    def display_tab(dataframe, tab_label):
        init_session_state(tab_label)
        search_query = st.session_state[f'search_query_{tab_label}']

        col1, col2 = st.columns([8, 2])

        with col1:
            # 검색 기능 추가
            search_query = st.text_input(
                "", search_query, placeholder="검색어를 입력하세요 (업체 또는 병원명):", key=f'search_input_{tab_label}')
            st.session_state[f'search_query_{tab_label}'] = search_query

        with col2:
            # 탭 메뉴를 selectbox로 대체
            tab_label = st.selectbox(
                "제품 구분",
                ["전체", "VoiceEMR", "VoiceENR", "VoiceSDK", "VoiceMARK", "VoiceDOC"],
                key=f'select_tab_{tab_label}'
            )

        if search_query:
            dataframe = dataframe[dataframe['계약명'].str.contains(
                search_query, case=False, na=False)]

        if dataframe.empty:
            st.markdown("<div class='no-data'>데이터가 없습니다</div>",
                        unsafe_allow_html=True)
        else:
            display_paginated_table(dataframe, tab_label)

    # 세션 초기화
    init_session_state("전체")

    # 데이터 표시
    tab_label = st.session_state['select_tab_전체'] if 'select_tab_전체' in st.session_state else "전체"
    if tab_label == "전체":
        filtered_data = contract_manage
    else:
        filtered_data = contract_manage[contract_manage['제품'].apply(
            lambda x: tab_label in x if isinstance(x, list) else str(x) == tab_label)]

    filtered_data = filtered_data.reset_index(drop=True)
    filtered_data.index = filtered_data.index + 1
    filtered_data.index.name = 'No'

    display_tab(filtered_data, tab_label)


if __name__ == "__main__":
    show_contract_management()
