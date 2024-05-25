import streamlit as st
from data_process import contract_management  # 데이터프레임을 data_process 모듈에서 불러옴

def show_contract_management():
    st.subheader("계약서 관리")
    st.write("정식/데모 계약서를 확인할 수 있습니다.:sunglasses:")

    # 표 높이와 너비 동적으로 설정하는 함수
    def get_table_dimensions():
        return 385, 2400  # 너비를 더 크게 설정

    table_height, table_width = get_table_dimensions()  # 표의 높이와 너비 설정
    items_per_page = 10  # 페이지당 항목 수 설정

    def paginate_data(dataframe, page_number, items_per_page):
        """
        데이터프레임을 페이지 번호에 따라 분할하여 반환하는 함수.
        """
        start_index = (page_number - 1) * items_per_page
        end_index = start_index + items_per_page
        paged_df = dataframe.iloc[start_index:end_index]
        paged_df.index = range(start_index + 1, start_index + 1 + len(paged_df))
        return paged_df

    # 세션 상태를 초기화하는 함수
    def init_session_state(tab_label):
        if f'{tab_label}_filtered_df' not in st.session_state:
            st.session_state[f'{tab_label}_filtered_df'] = contract_management
        if f'{tab_label}_page_number' not in st.session_state:
            st.session_state[f'{tab_label}_page_number'] = 1
        if f'search_query_{tab_label}' not in st.session_state:
            st.session_state[f'search_query_{tab_label}'] = ''

    # 데이터 프레임을 표시하고 페이징하는 함수
    def display_paginated_table(dataframe, tab_label):
        init_session_state(tab_label)
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
        st.dataframe(paged_df, height=table_height, width=table_width)
        st.write(f"Displaying rows {(page_number - 1) * items_per_page + 1} to {min(page_number * items_per_page, total_items)} of {total_items}")

    # 데이터 탭을 표시하고 검색 기능 추가
    def display_tab(dataframe, tab_label):
        init_session_state(tab_label)
        search_query = st.session_state[f'search_query_{tab_label}']
        
        col1, col2 = st.columns([8, 2])

        with col1:
            # 검색 기능 추가
            search_query = st.text_input("", search_query, placeholder="검색어를 입력하세요 (업체 또는 병원명):", key=f'search_input_{tab_label}')
            st.session_state[f'search_query_{tab_label}'] = search_query

        with col2:
            # 탭 메뉴를 selectbox로 대체
            tab_label = st.selectbox(
                "제품 구분",
                ["전체", "VoiceEMR", "VoiceENR", "VoiceSDK", "VoiceMARK", "VoiceDOC"],
                key=f'select_tab_{tab_label}'
            )

        if search_query:
            dataframe = dataframe[dataframe['계약명'].str.contains(search_query, case=False, na=False)]

        if dataframe.empty:
            st.markdown("<div class='no-data'>데이터가 없습니다</div>", unsafe_allow_html=True)
        else:
            display_paginated_table(dataframe, tab_label)

    # 세션 초기화
    init_session_state("전체")
    
    # 데이터 표시
    tab_label = st.session_state['select_tab_전체'] if 'select_tab_전체' in st.session_state else "전체"
    if tab_label == "전체":
        filtered_data = contract_management
    else:
        filtered_data = contract_management[contract_management['제품'].apply(lambda x: tab_label in x if isinstance(x, list) else str(x) == tab_label)]

    filtered_data = filtered_data.reset_index(drop=True)
    filtered_data.index = filtered_data.index + 1
    filtered_data.index.name = 'No'

    display_tab(filtered_data, tab_label)

if __name__ == "__main__":
    show_contract_management()
