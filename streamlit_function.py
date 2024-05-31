import streamlit as st
import pandas as pd


def get_table_dimensions():
    """표 높이와 너비 동적으로 설정하는 함수"""
    return '100%', '100%'  # 너비와 높이를 100%로 설정하여 웹 페이지 크기에 맞춤


def paginate_data(dataframe, page_number, items_per_page):
    """데이터프레임을 페이지 번호에 따라 분할하여 반환하는 함수"""
    start_index = (page_number - 1) * items_per_page
    end_index = start_index + items_per_page
    paged_df = dataframe.iloc[start_index:end_index]
    paged_df.index = range(start_index + 1, start_index + 1 + len(paged_df))
    return paged_df


def init_session_state(df, tab_label):
    """세션 상태를 초기화하는 함수"""
    if f'{tab_label}_filtered_df' not in st.session_state:
        st.session_state[f'{tab_label}_filtered_df'] = df
    if f'{tab_label}_page_number' not in st.session_state:
        st.session_state[f'{tab_label}_page_number'] = 1
    if 'search_query' not in st.session_state:
        st.session_state['search_query'] = ''
    if f'{tab_label}_selected_product' not in st.session_state:
        st.session_state[f'{tab_label}_selected_product'] = '전체'


def reset_session_state(tab_label):
    """세션 상태를 초기화하는 함수"""
    st.session_state['search_query'] = ''
    st.session_state[f'{tab_label}_selected_product'] = '전체'


def filter_dataframe(dataframe, tab_label, search_query, selected_product):
    """검색어와 선택된 제품에 따라 데이터프레임을 필터링하는 함수"""
    if tab_label == "계약서 관리":
        filter_column = '계약명'
    elif tab_label == "제품 현황 관리":
        filter_column = '업체 이름'
    elif tab_label == "기타 문서 관리":
        filter_column = '문서이름'
    elif tab_label == "업무 관리":
        filter_column = '분류'
    else:
        filter_column = None

    if search_query and filter_column:
        dataframe = dataframe[dataframe[filter_column].str.contains(
            search_query, case=False, na=False)]

    if selected_product != "전체" and filter_column:
        # Debug print to see what's being filtered
        print(f"Filtering {filter_column} for {selected_product}")
        # Changed from 'str.contains' to direct equality
        dataframe = dataframe[dataframe[filter_column] == selected_product]

    return dataframe


def display_html_table(dataframe, tab_label, items_per_page, search_query="", selected_product="전체"):
    """데이터프레임을 HTML로 변환하여 스트림릿에 표시하는 함수"""
    if f'{tab_label}_filtered_df' not in st.session_state:
        st.session_state[f'{tab_label}_filtered_df'] = dataframe
    if f'{tab_label}_page_number' not in st.session_state:
        st.session_state[f'{tab_label}_page_number'] = 1

    dataframe = filter_dataframe(
        dataframe, tab_label, search_query, selected_product)

    if dataframe.empty:
        st.markdown(
            """
            <style>
                body[data-theme="light"] .empty-message {
                    color: black;
                }
                body[data-theme="dark"] .empty-message {
                    color: white;
                }
            </style>
            <div class="empty-message" style='display: flex; justify-content: center; align-items: center; height: 50vh;'>
                <h2 style='font-weight: bold;'>데이터가 존재하지 않습니다. 신규 데이터가 등록되면 표시됩니다.</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

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
    if '사본링크' in paged_df.columns:
        paged_df['문서확인'] = paged_df['사본링크'].apply(
            lambda x: f'<a href="{x}" target="_blank" style="color: inherit;">문서 확인하기</a>')
        paged_df = paged_df.drop(columns=['사본링크'])

    if '기타문서 (견적서, NDA 등)' in paged_df.columns:
        paged_df['문서확인'] = paged_df['기타문서 (견적서, NDA 등)'].apply(
            lambda x: f'<a href="{x}" target="_blank" style="color: inherit;">문서 확인하기</a>')
        paged_df = paged_df.drop(columns=['기타문서 (견적서, NDA 등)'])

    if '페이지URL' in paged_df.columns:
        if tab_label == "계약서 관리" and '계약명' in paged_df.columns:
            paged_df['계약명'] = paged_df.apply(
                lambda row: f'<a href="{row["페이지URL"]}" target="_blank" style="color: inherit;">{row["계약명"]}</a>', axis=1)
        elif tab_label == "제품 현황 관리" and '업체 이름' in paged_df.columns:
            paged_df['업체 이름'] = paged_df.apply(
                lambda row: f'<a href="{row["페이지URL"]}" target="_blank" style="color: inherit;">{row["업체 이름"]}</a>', axis=1)
        elif tab_label == "기타 문서 관리" and '문서이름' in paged_df.columns:
            paged_df['문서이름'] = paged_df.apply(
                lambda row: f'<a href="{row["페이지URL"]}" target="_blank" style="color: inherit;">{row["문서이름"]}</a>', axis=1)

        elif tab_label == "업무 관리" and '업무' in paged_df.columns:
            paged_df['업무'] = paged_df.apply(
                lambda row: f'<a href="{row["페이지URL"]}" target="_blank" style="color: inherit;">{row["업무"]}</a>', axis=1)
        paged_df = paged_df.drop(columns=['페이지URL'])

    # NaN 또는 None 값을 빈 문자열로 대체
    paged_df = paged_df.fillna('')

    paged_df = paged_df.applymap(str)
    table_height, table_width = get_table_dimensions()

    # 실제로 존재하는 열만 고려하여 스타일 적용
    right_align_columns = []
    left_align_columns = [col for col in [
        '업체 이름', '계약명', '문서이름', '업무'] if col in paged_df.columns]

    # 스타일 설정
    column_styles = [{'selector': 'th', 'props': [('text-align', 'center')]}]

    for col in right_align_columns:
        column_styles.append({'selector': f'td.col{paged_df.columns.get_loc(col)}', 'props': [
                             ('text-align', 'right')]})

    for col in left_align_columns:
        column_styles.append({'selector': f'td.col{paged_df.columns.get_loc(col)}', 'props': [
                             ('text-align', 'left')]})

    styled_df = paged_df.style.set_table_styles(
        column_styles
    ).set_properties(
        **{'text-align': 'center'},
        subset=pd.IndexSlice[:, [
            col for col in paged_df.columns if col not in right_align_columns + left_align_columns]]
    )

    table_html = styled_df.to_html(escape=False)
    table_html = f'''
    <div style="height: {table_height}; width: {table_width}; overflow: auto;">
        <style>
            body[data-theme="light"] th {{
                color: black;
            }}
            body[data-theme="dark"] th {{
                color: white;
            }}
            body[data-theme="light"] td {{
                color: black;
            }}
            body[data-theme="dark"] td {{
                color: white;
            }}
            table {{
                width: 100%;
                table-layout: auto;
            }}
            th, td {{
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            td {{
                word-wrap: break-word;
                white-space: normal;
            }}
            a {{
                color: inherit;
                text-decoration: none;
            }}
        </style>
        {table_html}
    '''

    st.write(table_html, unsafe_allow_html=True)
    st.write(
        f"Displaying rows {(page_number - 1) * items_per_page + 1} to {min(page_number * items_per_page, total_items)} of {total_items}"
    )


def display_tab(dataframe, tab_label, items_per_page):
    """탭을 표시하고 검색 및 필터 기능을 추가하는 함수"""
    init_session_state(dataframe, tab_label)

    if st.button("필터 초기화"):
        reset_session_state(tab_label)

    search_query = st.session_state.get('search_query', "")
    selected_product = st.session_state.get(
        f'{tab_label}_selected_product', "전체")

    col1, col2 = st.columns([8, 2])

    with col1:
        search_query = st.text_input(
            "", search_query, placeholder="검색어를 입력해주세요", key='search_input')
        st.session_state['search_query'] = search_query

    with col2:
        if tab_label == "업무 관리":
            product_options = ["전체"] + \
                dataframe['분류'].dropna().unique().tolist()
            product_options = [
                option for option in product_options if option.strip()]
        else:
            product_options = ["전체", "VoiceEMR", "VoiceENR",
                               "VoiceSDK", "VoiceMARK", "VoiceDOC"]

        selected_product = st.selectbox(
            "제품 구분", product_options, key='select_tab')
        st.session_state[f'{tab_label}_selected_product'] = selected_product

    display_html_table(dataframe, tab_label, items_per_page,
                       search_query, selected_product)




def dashboard_button_df(df,column_name,status_list_counts,tab_name):
        
        # ArrowInvalid 오류 해결을 위해 리스트 형태를 텍스트 값으로 변환
        df['납품병원'] = df['납품병원'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

        # status_list는 제품 현황관리의 "상태" 리스트, isinstance는 변수의 타입이 무엇인지 확인하는 것
        if isinstance(status_list_counts[0], list):
            col_count = len(status_list_counts[0])
            cols = st.columns(col_count)

            # 클릭된 항목을 저장할 세션 상태 추가
            if 'clicked_item' not in st.session_state:
                st.session_state.clicked_item = None
           # enumerate는 리스트 값과 인덱스 추출하는 것
            for idx, item in enumerate(status_list_counts[0]):
                with cols[idx]:
                    # 진행 상태 값에 대한 수치 표현을 버튼으로 생성
                    if st.button(f"{item} : {status_list_counts[1][item]}", key=f"{tab_name}_{item}_{idx}"):
                        if st.session_state.clicked_item == item:
                            st.session_state.clicked_item = None
                        else:
                            st.session_state.clicked_item = item

            # 클릭된 항목과 연관된 데이터프레임 표시 (notion_df[0]에서만 필터링)
            if st.session_state.clicked_item:
                filtered_df = df[df['상태'].str.contains(st.session_state.clicked_item, na=False)]
                
                if len(filtered_df) == 0:
                    st.markdown("데이터가 존재하지 않습니다. 데이터가 추가되면 표시됩니다.")
                else:
                    filtered_df = filtered_df.reset_index(drop=True)  # 인덱스 열 제거
                    filtered_df.index += 1  # 인덱스를 1부터 시작
                    filtered_df.index.name = "No" 


                
                st.dataframe(filtered_df)