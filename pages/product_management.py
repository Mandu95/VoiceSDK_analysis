import streamlit as st
import pandas as pd
import data_process


def show_product_management():
    # 데이터 로드
    df = data_process.df

    st.subheader("제품 현황 관리")

    # 페이지 레이아웃 설정
    col_header, col_buttons = st.columns([8, 2])
    with col_header:
        st.subheader("PuzzleAI's 사업부 대시보드")

    with col_buttons:
        st.markdown(
            """
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
        start_index = (page_number - 1) * items_per_page
        end_index = start_index + items_per_page
        paged_df = dataframe.iloc[start_index:end_index]
        paged_df.index = range(
            start_index + 1, start_index + 1 + len(paged_df))
        return paged_df

    # 세션 상태를 초기화하는 함수
    def init_session_state(tab_label):
        if f'{tab_label}_filtered_df' not in st.session_state:
            st.session_state[f'{tab_label}_filtered_df'] = df
        if f'{tab_label}_page_number' not in st.session_state:
            st.session_state[f'{tab_label}_page_number'] = 1

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
        total_pages = max(
            1, (total_items + items_per_page - 1) // items_per_page)

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
        styled_df = paged_df.style.applymap(
            highlight_remaining_days, subset=['계약잔여일'])
        st.dataframe(styled_df, height=table_height, width=table_width)
        st.write(
            f"Displaying rows {(page_number - 1) * items_per_page + 1} to {min(page_number * items_per_page, total_items)} of {total_items}")

    # 데이터 탭을 표시하는 함수
    def display_tab(dataframe, tab_label, customers, contracts, demos, send_docu, unknown):
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
                <div class="no-data">데이터가 없습니다</div>
                """, unsafe_allow_html=True)
        else:
            display_paginated_table(filtered_df, tab_label)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["전체", "VoiceEMR", "VoiceENR", "VoiceSDK", "VoiceMARK", "VoiceDOC"])

    with tab1:
        all_data = df.reset_index(drop=True)
        all_data.index = all_data.index + 1
        all_data.index.name = 'No'
        display_paginated_table(all_data, "전체")

    def setup_tab(tab, product_name, tab_label):
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

    setup_tab(tab2, 'VoiceEMR', 'VoiceEMR')
    setup_tab(tab3, 'VoiceENR', 'VoiceENR')
    setup_tab(tab4, 'VoiceSDK', 'VoiceSDK')
    setup_tab(tab5, 'VoiceMARK', 'VoiceMARK')
    setup_tab(tab6, 'VoiceDOC', 'VoiceDOC')
