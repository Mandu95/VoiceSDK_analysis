import streamlit as st
import streamlit.components.v1 as components
import component_sub as mandu_cs


# 데이터프레임 html table로 보여주는 함수
def display_dataframe(df, page_name=None):

    df = mandu_cs.URL_insert(df)

    if page_name is not None:

        mandu_cs.reset_filter_button(
            f"{page_name}_filter", f"{page_name}_search")

        # 상단에 검색창과 선택박스 삽입
        col1, col2 = st.columns([8, 2])

        with col1:
            search_query = mandu_cs.search_box(f"{page_name}_search")

        with col2:
            if page_name == "업무":
                filter_options = df['분류'].dropna().unique().tolist()
                filter_options.insert(0, '전체')
                selected_filter = mandu_cs.filter_selectbox(
                    f"{page_name}_filter", filter_options)
                df = mandu_cs.URL_insert(df)
            else:
                filter_options = ["전체", "VoiceEMR", "VoiceENR",
                                  "VoiceSDK", "VoiceMARK", "VoiceEMR+", "VoiceDOC"]
                selected_filter = mandu_cs.filter_selectbox(
                    f"{page_name}_filter", filter_options)

        # 검색 기능 적용: 첫 번째 열을 기준으로 검색
        if search_query:
            first_column = df.columns[0]
            df = df[df[first_column].astype(
                str).str.contains(search_query, na=False)]

        # 제품 열의 리스트를 텍스트로 변환
        if '제품' in df.columns:
            df['제품'] = df['제품'].apply(lambda x: ', '.join(
                x) if isinstance(x, list) else x)

        if selected_filter != "전체":

            if page_name != "업무":
                df = df[df['제품'] == selected_filter]
            else:
                df = df[df['분류'] == selected_filter]

        if df.empty:
            # 데이터가 없는 경우 메시지 표시
            st.markdown(
                """
                <style>
                    .empty-message {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 50vh;
                        font-size: 2em;
                        color: black;
                    }
                </style>
                <div class="empty-message">검색 결과가 없습니다.</div>
                """,
                unsafe_allow_html=True
            )
        else:
            # 좌측 테이블과 우측 페이징을 위한 컬럼 배치
            col1, col2 = st.columns([8, 2])
            with col2:
                # 페이징
                items_per_page = 10  # 한 페이지에 보여줄 행의 개수
                paged_df, total_pages, page_num = mandu_cs.paginate_dataframe(
                    df, items_per_page, key_prefix=page_name)

            if page_name != "업무":
                paged_df = paged_df.drop(
                    columns=['제품'])  # 필요한 열만 남기고 제거

            # 데이터프레임을 HTML로 변환
            df_html = paged_df.to_html(index=False, escape=False)

            # 테이블 높이 계산
            table_height = mandu_cs.calculate_table_height(paged_df)

            # 데이터프레임 표시
            components.html(mandu_cs.show_table(df_html),
                            height=table_height + 100, scrolling=True)

    else:
        # 데이터프레임을 HTML로 변환
        df_html = df.to_html(index=False, escape=False)

        if df.empty:
            # 데이터가 없는 경우 메시지 표시
            st.markdown(
                """
                <style>
                    .empty-message {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 50vh;
                        font-size: 2em;
                        color: black;
                    }
                </style>
                <div class="empty-message">검색 결과가 없습니다.</div>
                """,
                unsafe_allow_html=True
            )

        # 데이터프레임 표시
        components.html(mandu_cs.show_table(df_html),
                        height=400, scrolling=True)


# 초기 페이지 설정
def set_initial_page():

    mandu_cs.load_css()
    col_header, col_buttons = st.columns([8, 2])
    with col_header:
        st.header("Welcome to PuzzleAI's Dashboard")

    with open("styles.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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


def table_columns_select(df, tab_name):
    if tab_name == "VoiceSDK":
        # 필요한 열만 남기고 제거
        df = df.drop(columns=['기타문서 (견적서, NDA 등)', "페이지URL",
                              "📦 업무 일정", "계약 횟수", "계약관리", "납품병원", "제품"])
        # 데이터프레임 열 순서 변경
        columns_order = ["업체 이름", "상태", "개발언어", "담당자 이메일",
                         "컨택 업체 담당자", "계약종료일", "계약잔여일", "라이선스 수", "정보 최신화 날짜"]
        df = df.reindex(columns=columns_order)
        # ArrowInvalid 오류 해결을 위해 리스트 형태를 텍스트 값으로 변환
        df['개발언어'] = df['개발언어'].apply(
            lambda x: ', '.join(x) if isinstance(x, list) else x)

    else:
        # 필요한 열만 남기고 제거
        df = df.drop(columns=['기타문서 (견적서, NDA 등)', "페이지URL",
                              "📦 업무 일정", "계약 횟수", "개발언어", "계약관리", "납품병원"])
        # 데이터프레임 열 순서 변경
        columns_order = ["업체 이름", "상태", "담당자 이메일",
                         "컨택 업체 담당자", "계약종료일", "계약잔여일", "라이선스 수", "정보 최신화 날짜"]
        df = df.reindex(columns=columns_order)

    return df


def component_top_button(df, tab_name):

    df, temp_values = mandu_cs.preprocess_df(df, tab_name)
    # 상태별 카운트 계산
    status_counts = df['상태'].value_counts().to_dict()

    # 상태 버튼 생성
    col_count = len(temp_values)
    cols = st.columns(col_count)

    if 'clicked_item' not in st.session_state:
        st.session_state.clicked_item = None

    for idx, item in enumerate(temp_values):
        with cols[idx]:
            count = status_counts.get(item, 0)
            if st.button(f"{item} : {count}", key=f"{tab_name}_{item}_{idx}_first"):
                if st.session_state.clicked_item == item:
                    st.session_state.clicked_item = None
                else:
                    st.session_state.clicked_item = item

    # 클릭된 항목과 연관된 데이터프레임 표시 (df에서 필터링)
    if st.session_state.clicked_item:
        df = df[df['상태'] == st.session_state.clicked_item]
        if len(df) == 0:
            st.markdown("데이터가 존재하지 않습니다. 데이터가 추가되면 표시됩니다.")
        else:
            df = df.reset_index(drop=True)
            display_dataframe(df)

            # 계약완료 버튼이 클릭됐을 때 아래 선택박스/테이블 표시를 위한 코드
            if st.session_state.clicked_item == "계약완료":
                Data_all_df = st.session_state['매입/매출 전체 데이터']
                Data_all_df = Data_all_df[Data_all_df['제품'] == tab_name]

                Data_buy_df = st.session_state['매입/매출 매출 데이터']
                Data_buy_df = Data_buy_df[Data_buy_df['제품'] == tab_name]

                Data_sell_df = st.session_state['매입/매출 매입 데이터']
                Data_sell_df = Data_sell_df[Data_sell_df['제품'] == tab_name]

                Data_no_info_df = st.session_state['매입/매출 정보없음 데이터']
                Data_no_info_df = Data_no_info_df[Data_no_info_df['제품'] == tab_name]

                # Tab 메뉴 항목들
                tab_titles = ["전체", "매출/매입", "정보없음"]
                tabs = st.tabs(tab_titles)

                with tabs[0]:

                    all_select_values = mandu_cs.extract_column_unique_value(
                        Data_all_df, "제품 현황 관리")
                    col1, col2 = st.columns([8, 2])
                    with col1:
                        st.write(f"문서개수 : {len(Data_all_df)}")
                    with col2:
                        selected_filter = mandu_cs.filter_selectbox(
                            f"{tabs}_all_filter", all_select_values)

                    result = mandu_cs.View_table(
                        selected_filter, Data_all_df, "계약완료 버튼클릭")
                    if result:
                        display_dataframe(Data_all_df)

                with tabs[1]:
                    buy_select_values = mandu_cs.extract_column_unique_value(
                        Data_buy_df, "제품 현황 관리")
                    sell_select_values = mandu_cs.extract_column_unique_value(
                        Data_sell_df, "제품 현황 관리")

                    col10, col11 = st.columns([5, 5])

                    with col10:
                        col20, col21 = st.columns([8, 2])
                        with col20:
                            st.write(f"문서개수 : {len(Data_buy_df)}")
                        with col21:
                            selected_filter = mandu_cs.filter_selectbox(
                                f"{tabs}_buy_filter", buy_select_values)

                        result = mandu_cs.View_table(
                            selected_filter, Data_buy_df, "계약완료 버튼클릭")
                        if result:
                            display_dataframe(Data_buy_df)
                    with col11:
                        col22, col23 = st.columns([8, 2])
                        with col22:
                            st.write(f"문서개수 : {len(Data_sell_df)}")
                        with col23:
                            selected_filter = mandu_cs.filter_selectbox(
                                f"{tabs}_sell_filter", sell_select_values)
                        mandu_cs.View_table(
                            selected_filter, Data_sell_df, "계약완료 버튼클릭")
                        if result:
                            display_dataframe(Data_sell_df)
                with tabs[2]:
                    no_info_select_values = mandu_cs.extract_column_unique_value(
                        Data_no_info_df, "제품 현황 관리")
                    col1, col2 = st.columns([8, 2])
                    with col1:
                        st.write(f"문서개수 : {len(Data_no_info_df)}")
                    with col2:
                        selected_filter = mandu_cs.filter_selectbox(
                            f"{tabs}_no_info_filter", no_info_select_values)

                    result = mandu_cs.View_table(
                        selected_filter, no_info_select_values, "계약완료 버튼클릭")
                    if result:
                        display_dataframe(Data_no_info_df)


def second_layer(DF_update_one_Week_cop, DF_New_cop, tab_name):
    col1, col2 = st.columns([5, 5])

    with col1:
        st.subheader("최근 1주 내 이력변경")
        # 데이터프레임이 비었는지 확인
        if DF_update_one_Week_cop.empty:
            mandu_cs.display_empty_message(f"{tab_name}의 업데이트된 데이터가 없습니다.")
        else:

            # HTML/CSS 스타일 설정
            st.markdown("""
                    <style>
                    .stButton button {
                        display: inline-block;
                        padding: auto;
                        margin: auto;
                        font-size: 14px;
                    }
                    </style>
                """, unsafe_allow_html=True)

            cols = st.columns(len(DF_update_one_Week_cop))
            for col, (index, row) in zip(cols, DF_update_one_Week_cop.iterrows()):
                # 고유한 키를 사용하여 같은 이름이 중복되는 경우 문제를 방지
                button_key = f"{row['업체 이름']}_{index}"
                if col.button(row['업체 이름'], key=button_key):
                    st.write(f"{row['업체 이름']} 버튼이 클릭되었습니다!")
                    # 클릭 시 세부 정보를 표시하는 expander
                    with st.expander("세부 정보 보기"):
                        st.write(f"업체 이름: {row['업체 이름']}")
                        st.write(f"정보 최신화 날짜: {row['정보 최신화 날짜']}")

    with col2:

        st.subheader(f"당월 신규 업체")

        if DF_New_cop.empty:
            mandu_cs.display_empty_message(f"{tab_name}의 신규 데이터가 없습니다.")
        else:
            DF_New_cop = mandu_cs.URL_insert(DF_New_cop)
            DF_New_cop = mandu_cs.table_columns_select(
                DF_New_cop, tab_name, "두번째레이어")

            display_dataframe(DF_New_cop)


def third_layer(demo_cop, Demo_to_contract_cop,  tab_name):

    # 스타일 적용
    st.markdown("""
    <style>
    .divider {
        border-left: 2px solid #ccc;
        height: 100px;
    }
    </style>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([5, 5, 5])

    with col1:

        st.subheader("계약전환률")
        st.write("데모 또는 MOU 체결 등 협력 진행 이후 정식계약으로 전환 된 비율입니다.")

        if Demo_to_contract_cop.empty:
            mandu_cs.display_empty_message(f"{tab_name}의 계약 전환 된 사례가 없습니다.")
        else:
            # mandu_cs.URL_insert(Demo_to_contract_cop)
            Demo_total_len = len(demo_cop)
            Demo_to_contract_len = len(Demo_to_contract_cop)
            result = (Demo_to_contract_len/Demo_total_len) * 100
            result = round(result, 2)
            # st.write(Demo_total_len, Demo_to_contract_len)
            st.header(f"{result}%")
            # # 초기화
            # if 'selected_item' not in st.session_state:
            #     st.session_state.selected_item = None

            # # 각 항목에 대한 버튼 생성
            # for item in DA_result:
            #     if st.button(item):
            #         st.session_state.selected_item = item  # 클릭된 아이템 저장

            # # 선택된 아이템이 있을 경우 표시
            # if st.session_state.selected_item:
            #     st.write(f"You clicked: {st.session_state.selected_item}")

    with col2:

        st.subheader("계약전환률")
        st.write("데모 또는 MOU 체결 등 협력 진행 이후 정식계약으로 전환 된 비율입니다.")
