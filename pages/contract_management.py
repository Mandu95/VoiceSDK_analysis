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
        paged_df.index = range(
            start_index + 1, start_index + 1 + len(paged_df))
        return paged_df

    # 세션 상태를 초기화하는 함수
    def init_session_state(tab_label):
        if f'{tab_label}_filtered_df' not in st.session_state:
            st.session_state[f'{tab_label}_filtered_df'] = contract_management
        if f'{tab_label}_page_number' not in st.session_state:
            st.session_state[f'{tab_label}_page_number'] = 1

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
        st.dataframe(paged_df, height=table_height, width=table_width)
        st.write(
            f"Displaying rows {(page_number - 1) * items_per_page + 1} to {min(page_number * items_per_page, total_items)} of {total_items}")

    # 데이터 탭을 표시하는 함수
    def display_tab(dataframe, tab_label):
        init_session_state(tab_label)
        col1, col2, col3 = st.columns([3, 3, 3])

        total_count = len(dataframe)
        sell_count = len(dataframe[dataframe['매입/매출'] == '매출'])
        buy_count = len(dataframe[dataframe['매입/매출'] == '매입'])

        def create_button(column, label, data_filter, count):
            with column:
                st.write(label)
                if st.button(f"{count}", key=f"{tab_label}_{label}"):
                    st.session_state[f'{tab_label}_filtered_df'] = data_filter
                    st.session_state[f'{tab_label}_page_number'] = 1

        create_button(col1, "전체", dataframe, total_count)
        create_button(
            col2, "매출", dataframe[dataframe['매입/매출'] == '매출'], sell_count)
        create_button(
            col3, "매입", dataframe[dataframe['매입/매출'] == '매입'], buy_count)

        filtered_df = st.session_state[f'{tab_label}_filtered_df']
        if filtered_df.empty:
            st.markdown("<div class='no-data'>데이터가 없습니다</div>",
                        unsafe_allow_html=True)
        else:
            display_paginated_table(filtered_df, tab_label)

    tabs = ["전체", "VoiceEMR", "VoiceENR", "VoiceSDK", "VoiceMARK", "VoiceDOC"]
    selected_tab = st.tabs(tabs)

    for i, tab in enumerate(tabs):
        with selected_tab[i]:
            if tab == "전체":
                filtered_data = contract_management
            else:
                # 필터링 결과를 디버그 출력으로 확인
                filtered_data = contract_management[contract_management['제품'] == tab]
                st.write(f"Filtered data for tab {tab}:")
                st.write(filtered_data)

            filtered_data = filtered_data.reset_index(drop=True)
            filtered_data.index = filtered_data.index + 1
            filtered_data.index.name = 'No'

            if filtered_data.empty:
                st.markdown("<div class='no-data'>데이터가 없습니다</div>",
                            unsafe_allow_html=True)
            else:
                display_tab(filtered_data, tab)


if __name__ == "__main__":
    show_contract_management()
