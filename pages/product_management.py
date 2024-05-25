import streamlit as st
from data_process import product_management  # 데이터 로드

def show_product_management():
    df = product_management  # 데이터프레임 설정

    st.subheader("제품 현황 관리")
    st.write("Notion DB를 기준으로 분석한 자료이며, 오전 8시, 12시, 15시 하루 3회 동기화 됩니다.:sunglasses:")

    # 표 높이와 너비 동적으로 설정하는 함수
    def get_table_dimensions():
        return 385, 2400  # 너비를 더 크게 설정

    table_height, table_width = get_table_dimensions()  # 표의 높이와 너비 설정
    items_per_page = 10  # 페이지당 항목 수 설정

    # 데이터프레임을 페이징하는 함수
    def paginate_data(dataframe, page_number, items_per_page):
        start_index = (page_number - 1) * items_per_page
        end_index = start_index + items_per_page
        paged_df = dataframe.iloc[start_index:end_index]
        paged_df.index = range(start_index + 1, start_index + 1 + len(paged_df))
        return paged_df

    # 세션 상태를 초기화하는 함수
    def init_session_state(tab_label):
        if f'{tab_label}_filtered_df' not in st.session_state:
            st.session_state[f'{tab_label}_filtered_df'] = df
        if f'{tab_label}_page_number' not in st.session_state:
            st.session_state[f'{tab_label}_page_number'] = 1
        if 'search_query' not in st.session_state:
            st.session_state['search_query'] = ''

    # "계약잔여일"이 90일보다 작은 경우 노란색으로 강조하는 함수
    def highlight_remaining_days(val):
        try:
            if int(val) < 90:
                return 'background-color: yellow'
        except (ValueError, TypeError):
            return ''
        return ''

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

        if '계약잔여일' in paged_df.columns:
            styled_df = paged_df.style.applymap(
                highlight_remaining_days, subset=['계약잔여일'])
        else:
            styled_df = paged_df

        st.dataframe(styled_df, height=table_height, width=table_width)
        st.write(
            f"Displaying rows {(page_number - 1) * items_per_page + 1} to {min(page_number * items_per_page, total_items)} of {total_items}")

    # 데이터 탭을 표시하고 검색 기능 추가
    def display_tab(dataframe, tab_label):
        init_session_state(tab_label)
        search_query = st.session_state['search_query']
        
        col1, col2 = st.columns([8, 2])

        with col1:
            # 검색 기능 추가
            search_query = st.text_input("", search_query, placeholder="업체 이름 또는 병원 이름을 입력해주세요", key='search_input')
            st.session_state['search_query'] = search_query

        with col2:
            # 탭 메뉴를 selectbox로 대체
            tab_label = st.selectbox(
                "제품 구분",
                ["전체", "VoiceEMR", "VoiceENR", "VoiceSDK", "VoiceMARK", "VoiceDOC"],
                key='select_tab'
            )

        if tab_label == "전체":
            filtered_data = dataframe
        else:
            filtered_data = dataframe[dataframe['연관 제품'].apply(lambda x: tab_label in x if isinstance(x, list) else tab_label == x)]

        if search_query:
            filtered_data = filtered_data[filtered_data['업체 이름'].str.contains(search_query, case=False, na=False)]

        if filtered_data.empty:
            st.markdown("<div class='no-data'>데이터가 없습니다</div>", unsafe_allow_html=True)
        else:
            display_paginated_table(filtered_data, tab_label)

    # 세션 초기화
    init_session_state("전체")
    
    # 데이터 표시
    tab_label = st.session_state['select_tab'] if 'select_tab' in st.session_state else "전체"
    if tab_label == "전체":
        filtered_data = product_management
    else:
        filtered_data = product_management[product_management['연관 제품'].apply(lambda x: tab_label in x if isinstance(x, list) else tab_label == x)]

    filtered_data = filtered_data.reset_index(drop=True)
    filtered_data.index = filtered_data.index + 1
    filtered_data.index.name = 'No'

    display_tab(filtered_data, tab_label)

if __name__ == "__main__":
    show_product_management()
