import streamlit as st
import streamlit.components.v1 as components
import component_sub as mandu_cs
import streamlit as st
from datetime import datetime
import plotly.express as px
import pandas as pd


# 데이터프레임 html table로 보여주는 함수
def display_dataframe(df, tab_name=None, page_name=None, purpose=None):

    df = mandu_cs.URL_insert(df)

    if df is not None and not df.empty:
        if page_name is not None:

            mandu_cs.reset_filter_button(
                f"{page_name}_filter", f"{page_name}_search")

            # 상단에 검색창과 선택박스 삽입
            col1, col2 = st.columns([8, 2])

            with col1:
                search_query = mandu_cs.search_box(f"{page_name}_search")

            with col2:
                if page_name == "업무":
                    filter_options = df['프로젝트 (제품)'].dropna().unique().tolist()
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
                    df = df[df['프로젝트 (제품)'] == selected_filter]

            if df.empty:
                mandu_cs.display_empty_message(f"조회되는 데이터가 없습니다.")
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


def component_top_button(df, demo_cop=None, Demo_to_contract_cop=None, tab_name=None):
    df = mandu_cs.URL_insert(df)
    df, temp_values = mandu_cs.preprocess_df(df, tab_name)
    temp_values = ["전체"] + temp_values  # 상태별 유니크 값 추출 및 '전체' 추가
    status_counts = df['상태'].value_counts().to_dict()
    status_counts['전체'] = len(df)  # 전체 데이터 수를 추가

    cols = st.columns(len(temp_values))  # 각 상태에 대한 버튼을 배치할 열 생성

    if 'clicked_item' not in st.session_state:
        st.session_state.clicked_item = '전체'  # 세션 상태에 'clicked_item' 초기화

    if 'show_tables' not in st.session_state:
        st.session_state.show_tables = False  # 세션 상태에 'show_tables' 초기화

    if 'buy_filter' not in st.session_state:
        st.session_state.buy_filter = '전체'
    if 'sell_filter' not in st.session_state:
        st.session_state.sell_filter = '전체'
    if 'no_info_filter' not in st.session_state:
        st.session_state.no_info_filter = '전체'

    for idx, item in enumerate(temp_values):
        with cols[idx]:  # 생성된 열에 각 버튼 배치
            count = status_counts.get(item, 0)
            button_label = f"{item} : {count}"
            if st.button(button_label, key=f"{tab_name}_{item}_{idx}_first"):
                # 클릭된 아이템이 다시 클릭되면 전체 데이터프레임 표시
                if st.session_state.clicked_item == item:
                    st.session_state.clicked_item = '전체'
                    st.session_state.show_tables = False
                else:
                    st.session_state.clicked_item = item
                    st.session_state.show_tables = True
                st.session_state.selected_filter = '전체'  # 버튼 클릭 시 필터 초기화

    # 클릭된 항목에 따라 데이터프레임 필터링
    if st.session_state.clicked_item == '전체' or not st.session_state.clicked_item:
        display_dataframe(df, tab_name)  # 전체 데이터프레임 표시
    else:
        filtered_df = df[df['상태'] == st.session_state.clicked_item]
        if filtered_df.empty:
            st.write("데이터가 존재하지 않습니다. 데이터가 추가되면 표시됩니다.")
        else:
            display_dataframe(filtered_df.reset_index(drop=True), tab_name)

        # 계약완료 버튼이 클릭됐을 때 아래 선택박스/테이블 표시를 위한 코드
        if st.session_state.clicked_item == "계약완료" and st.session_state.show_tables:
            Data_all_df = st.session_state['매입/매출 전체 데이터']
            Data_all_df = Data_all_df[Data_all_df['제품'] == tab_name]
            all_select_values = ['전체'] + \
                [str(year) for year in range(2018, 2025)]
            Data_all_df = mandu_cs.columns_select(
                Data_all_df, tab_name, "계약완료 버튼클릭")

            Data_buy_df = st.session_state['매입/매출 매출 데이터']
            Data_buy_df = Data_buy_df[Data_buy_df['제품'] == tab_name]
            buy_select_values = ['전체'] + \
                [str(year) for year in range(2018, 2025)]
            Data_buy_df = mandu_cs.columns_select(
                Data_buy_df, tab_name, "계약완료 버튼클릭")

            Data_sell_df = st.session_state['매입/매출 매입 데이터']
            Data_sell_df = Data_sell_df[Data_sell_df['제품'] == tab_name]
            sell_select_values = ['전체'] + \
                [str(year) for year in range(2018, 2025)]
            Data_sell_df = mandu_cs.columns_select(
                Data_sell_df, tab_name, "계약완료 버튼클릭")

            Data_no_info_df = st.session_state['매입/매출 정보없음 데이터']
            Data_no_info_df = Data_no_info_df[Data_no_info_df['제품'] == tab_name]
            no_info_select_values = ['전체'] + \
                [str(year) for year in range(2018, 2025)]
            Data_no_info_df = mandu_cs.columns_select(
                Data_no_info_df, tab_name, "계약완료 버튼클릭")

            # Tab 메뉴 항목들
            tab_titles = ["매출/매입", "정보없음"]
            tabs = st.tabs(tab_titles)

            with tabs[0]:
                if demo_cop is None and Demo_to_contract_cop is None:

                    if len(Data_all_df) != 0:
                        col11, col12 = st.columns([5, 5])
                        with col11:
                            col20, col21 = st.columns([8, 2])

                            with col20:
                                st.subheader("매출 계약서")
                                st.write(f"문서개수 : {len(Data_buy_df)}")
                            with col21:
                                selected_buy_filter = st.selectbox(
                                    "기간 선택:", buy_select_values, key=f"{tab_name}_buy_filter")

                                if selected_buy_filter != st.session_state.buy_filter:
                                    st.session_state.buy_filter = selected_buy_filter

                            if st.session_state.buy_filter != "전체":
                                Data_buy_df = Data_buy_df[Data_buy_df['계약명'].str.contains(
                                    st.session_state.buy_filter)]

                            if Data_buy_df.empty:
                                st.write("검색 결과가 없습니다.")
                            else:
                                display_dataframe(Data_buy_df, tab_name)

                        with col12:
                            col22, col23 = st.columns([8, 2])
                            with col22:
                                st.subheader("매입 계약서")
                                st.write(f"문서개수 : {len(Data_sell_df)}")
                            with col23:
                                selected_sell_filter = st.selectbox(
                                    "기간 선택:", sell_select_values, key=f"{tab_name}_sell_filter")

                                if selected_sell_filter != st.session_state.sell_filter:
                                    st.session_state.sell_filter = selected_sell_filter

                            if st.session_state.sell_filter != "전체":
                                Data_sell_df = Data_sell_df[Data_sell_df['계약명'].str.contains(
                                    st.session_state.sell_filter)]

                            if Data_sell_df.empty:
                                st.write("검색 결과가 없습니다.")
                            else:
                                display_dataframe(Data_sell_df, tab_name)
                else:
                    col10, col11, col12 = st.columns([3, 5, 5])

                    with col10:  # Use col11 as the first column
                        st.subheader("계약전환률")
                        st.write("데모 계약 이후 정식계약으로 전환 된 비율입니다.")

                        if Demo_to_contract_cop.empty:
                            mandu_cs.display_empty_message(
                                f"{tab_name}의 계약 전환 된 사례가 없습니다.")
                        else:
                            Demo_total_len = len(demo_cop)
                            Demo_to_contract_len = len(Demo_to_contract_cop)
                            result = (Demo_to_contract_len /
                                      Demo_total_len) * 100
                            result = round(result, 2)
                            st.header(f"{result}%")
                    with col11:
                        col20, col21 = st.columns([8, 2])

                        with col20:
                            st.subheader("매출 계약서")
                            st.write(f"문서개수 : {len(Data_buy_df)}")
                        with col21:
                            selected_buy_filter = st.selectbox(
                                "기간 선택:", buy_select_values, key=f"{tab_name}_buy_filter")

                            if selected_buy_filter != st.session_state.buy_filter:
                                st.session_state.buy_filter = selected_buy_filter

                        if st.session_state.buy_filter != "전체":
                            Data_buy_df = Data_buy_df[Data_buy_df['계약명'].str.contains(
                                st.session_state.buy_filter)]

                        if Data_buy_df.empty:
                            st.write("검색 결과가 없습니다.")
                        else:
                            display_dataframe(Data_buy_df, tab_name)

                    with col12:
                        col22, col23 = st.columns([8, 2])
                        with col22:
                            st.subheader("매입 계약서")
                            st.write(f"문서개수 : {len(Data_sell_df)}")
                        with col23:
                            selected_sell_filter = st.selectbox(
                                "기간 선택:", sell_select_values, key=f"{tab_name}_sell_filter")

                            if selected_sell_filter != st.session_state.sell_filter:
                                st.session_state.sell_filter = selected_sell_filter

                        if st.session_state.sell_filter != "전체":
                            Data_sell_df = Data_sell_df[Data_sell_df['계약명'].str.contains(
                                st.session_state.sell_filter)]

                        if Data_sell_df.empty:
                            st.write("검색 결과가 없습니다.")
                        else:
                            display_dataframe(Data_sell_df, tab_name)

            with tabs[1]:
                col1, col2 = st.columns([8, 2])
                with col1:
                    st.write(f"문서개수 : {len(Data_no_info_df)}")
                with col2:
                    selected_no_info_filter = st.selectbox(
                        "기간 선택:", no_info_select_values, key=f"{tab_name}_no_info_filter")

                    if selected_no_info_filter != st.session_state.no_info_filter:
                        st.session_state.no_info_filter = selected_no_info_filter

                if st.session_state.no_info_filter != "전체":
                    Data_no_info_df = Data_no_info_df[Data_no_info_df['계약명'].str.contains(
                        st.session_state.no_info_filter)]

                if Data_no_info_df.empty:
                    st.write("검색 결과가 없습니다.")
                else:
                    display_dataframe(Data_no_info_df, tab_name)


def third_layer(DF_update_one_Week_cop, DF_New_cop, tab_name):
    col1, col2 = st.columns([5, 5])

    with col1:
        st.subheader("최근 1주 내 이력변경")
        # 데이터프레임이 비었는지 확인
        if DF_update_one_Week_cop.empty:
            mandu_cs.display_empty_message(f"{tab_name}의 업데이트된 데이터가 없습니다.")
        else:
            DF_update_one_Week_cop = mandu_cs.URL_insert(
                DF_update_one_Week_cop)
            DF_update_one_Week_cop = mandu_cs.columns_select(
                DF_update_one_Week_cop, tab_name, "두번째레이어 왼쪽")

            display_dataframe(DF_update_one_Week_cop, tab_name)

            # # HTML/CSS 스타일 설정
            # st.markdown("""
            #         <style>
            #         .stButton button {
            #             display: inline-block;
            #             padding: auto;
            #             margin: auto;
            #             font-size: 14px;
            #         }
            #         </style>
            #     """, unsafe_allow_html=True)

            # cols = st.columns(len(DF_update_one_Week_cop))
            # for col, (index, row) in zip(cols, DF_update_one_Week_cop.iterrows()):
            #     # 고유한 키를 사용하여 같은 이름이 중복되는 경우 문제를 방지
            #     button_key = f"{row['업체 이름']}_{index}"
            #     if col.button(row['업체 이름'], key=button_key):
            #         st.write(f"{row['업체 이름']} 버튼이 클릭되었습니다!")
            #         # 클릭 시 세부 정보를 표시하는 expander
            #         with st.expander("세부 정보 보기"):
            #             st.write(f"업체 이름: {row['업체 이름']}")
            #             st.write(f"정보 최신화 날짜: {row['정보 최신화 날짜']}")

    with col2:

        st.subheader(f"당월 신규 업체")

        if DF_New_cop.empty:
            mandu_cs.display_empty_message(f"{tab_name}의 신규 데이터가 없습니다.")
        else:
            DF_New_cop = mandu_cs.URL_insert(DF_New_cop)
            DF_New_cop = mandu_cs.columns_select(
                DF_New_cop, tab_name, "두번째레이어 오른쪽")

            display_dataframe(DF_New_cop, tab_name)


def second_layer(moeny_df_list, quarter_list, tab_name):

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
        st.subheader("누적 영업매출")
        st.write("창립 이후 누적 매출입니다.")
        # 년도별 '계약총액' 합계 계산
        years = list(range(2022, 2025))
        yearly_sum = []
        for year in years:
            yearly_sum.append(
                moeny_df_list[0][(moeny_df_list[0]['매입/매출'] == '매출') &
                                 (moeny_df_list[0]['계약명'].str.contains(str(year)))]['계약총액'].sum()
            )

        # 현재 년도
        current_year = datetime.now().year

        # 데이터프레임 생성
        df = pd.DataFrame({
            '년도': years,
            '계약총액': yearly_sum
        })

        # 금액 단위로 변환 (천만원 단위)
        df['계약총액(천 만원)'] = df['계약총액'] / 10000000

        # 색상 설정
        df['색상'] = df['년도'].apply(
            lambda x: '당해년도' if x == current_year else '이전년도')

        # 0인 값 제외
        df = df[df['계약총액'] > 0]

        # 누적 매출액 계산
        total_revenue = moeny_df_list[0]['계약총액'].sum()

        # Plotly 파이 차트 생성
        fig = px.pie(
            df, names='년도', values='계약총액', color='색상',
            color_discrete_map={'당해년도': '#018E92', '이전년도': 'gray'},
            title=f"전체: {total_revenue:,.0f}원",
            hole=0.4  # 도넛형 차트로 만들기 위해 중간에 구멍 추가
        )

        # 마우스 커서에 표시되는 금액 포맷
        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>계약총액: %{value:,.0f}원<br>'
        )

        # 범례를 "당해년도"와 "이전년도"로 변경
        fig.update_layout(
            legend_title_text='년도 구분',
            legend=dict(
                itemsizing='constant',
                traceorder='reversed'
            )
        )

        # Streamlit에 그래프 표시
        st.plotly_chart(fig)
    with col2:
        st.subheader("올해 영업매출")
        st.write("계약날짜 기준으로 산출 된 계약총액 합계입니다.")
        # 금액 데이터 (예시 데이터 사용)

        # '계약명' 열에 '2024'가 포함된 항목만 필터링하여 합산
        total_this_year__money_amount = moeny_df_list[0][moeny_df_list[0]['계약명'].str.contains(
            '2024')]['계약총액'].sum()
        # 내가 구해 둔 항목의 합산
        total_this_months_money_amount = moeny_df_list[1]['계약총액'].sum()
        total_last_3_months_money_amount = moeny_df_list[2]['계약총액'].sum()
        total_last_6_months_money_amount = moeny_df_list[3]['계약총액'].sum()

        # 금액 단위로 표시
        total_this_year__money_amount_formatted = total_this_year__money_amount / \
            10000000  # 천 만원 단위로 변환
        total_this_months_money_amount_formatted = total_this_months_money_amount / \
            10000000  # 천 만원 단위로 변환
        total_last_3_months_money_amount_formatted = total_last_3_months_money_amount / \
            10000000  # 천 만원 단위로 변환
        total_last_6_months_money_amount_formatted = total_last_6_months_money_amount / \
            10000000  # 천 만원 단위로 변환

        # 데이터프레임 생성
        df = pd.DataFrame({
            '기간': ['24년', '당월', '3개월', '6개월'],
            '금액(천 만원)': [total_this_year__money_amount_formatted, total_this_months_money_amount_formatted, total_last_3_months_money_amount_formatted, total_last_6_months_money_amount_formatted],
            '원래 금액': [total_this_year__money_amount, total_this_months_money_amount, total_last_3_months_money_amount, total_last_6_months_money_amount]
        })

        # Plotly 막대 그래프 생성
        fig = px.bar(df, x='기간', y='금액(천 만원)', text_auto=False, color='기간',
                     color_discrete_map={
                         '24년 누적': '#018E92', '당월': '#636EFA', '3개월': 'gray', '6개월': 'gray'},
                     hover_data={'기간': False, '금액(천 만원)': False, '원래 금액': True})

        # 마우스 커서에 표시되는 금액 포맷
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>금액: %{customdata[0]:,.0f}원<br>')

        # Streamlit에 그래프 표시
        st.plotly_chart(fig)

        # total_this_months_money_amount = moeny_df_list[0]['계약총액'].sum()
        # total_last_3_months_money_amount = moeny_df_list[1]['계약총액'].sum()
        # total_last_6_months_money_amount = moeny_df_list[2]['계약총액'].sum()

        # # 금액 단위로 표시
        # formatted_this_month = f"{total_this_months_money_amount:,}원"
        # formatted_last_3_months = f"{total_last_3_months_money_amount:,}원"
        # formatted_last_6_months = f"{total_last_6_months_money_amount:,}원"

        # col10, col11 = st.columns([8, 2])
        # with col10:
        #     st.subheader("영업매출")
        #     st.write("계약서의 계약날짜 기준으로 산출 된 계약총액 합계입니다.")

        # with col11:
        #     # 선택박스 구성

        #     period_options = {
        #         "당월": formatted_this_month,
        #         "3개월": formatted_last_3_months,
        #         "6개월": formatted_last_6_months
        #     }

        #     # 각 선택박스에 고유한 키를 할당하기 위해 tab_name 변수와 고유의 접미사를 사용
        #     monthly_sales_key = f"{tab_name}_monthly_sales_selectbox"
        #     selected_period1 = st.selectbox("기간 선택:", list(
        #         period_options.keys()), key=monthly_sales_key)

        # st.subheader(f"{period_options[selected_period1]}")

    with col3:
        # 분기별 매출액 계산
        quarter_1_money = quarter_list[0]['계약총액'].sum()
        quarter_2_money = quarter_list[1]['계약총액'].sum()
        quarter_3_money = quarter_list[2]['계약총액'].sum()
        quarter_4_money = quarter_list[3]['계약총액'].sum()

        # 금액 단위로 표시
        formatted_money = {
            "1/4분기": f"{quarter_1_money:,}원",
            "2/4분기": f"{quarter_2_money:,}원",
            "3/4분기": f"{quarter_3_money:,}원",
            "4/4분기": f"{quarter_4_money:,}원"
        }

        current_quarter = (datetime.now().month - 1) // 3 + 1

        col10, col11 = st.columns([7, 3])
        with col10:
            st.subheader("분기별 매출")
            st.write("당해 년도 분기 별 매출 데이터입니다.")

        with col11:
            # 선택박스 구성
            quarter_sales_key = f"{tab_name}_quarter_sales_selectbox"
            selected_quarter_text = st.selectbox("기간 선택:", list(
                formatted_money.keys()), key=quarter_sales_key)

            selected_quarter_index = int(selected_quarter_text.split('/')[0])

        if selected_quarter_index > current_quarter:
            st.write("분기가 시작되면 데이터가 표시됩니다!")
        else:
            st.subheader(formatted_money[selected_quarter_text])
