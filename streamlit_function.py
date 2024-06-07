import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
from bs4 import BeautifulSoup


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


def filter_dataframe(dataframe, search_query, selected_product):
    """검색어와 선택된 제품에 따라 데이터프레임을 필터링하는 함수"""

    # 두 번째 열의 이름 가져오기
    second_column = dataframe.columns[0]

    # 검색어에 따라 필터링
    if search_query:
        dataframe = dataframe[dataframe.apply(lambda row: row.astype(
            str).str.contains(search_query, case=False, na=False).any(), axis=1)]

    # 선택된 제품에 따라 필터링 (두 번째 열의 값이 선택된 제품을 포함하는지 확인)
    if selected_product != "전체":
        dataframe = dataframe[dataframe[second_column].str.contains(
            selected_product, case=False, na=False)]

    return dataframe


def display_html_table(dataframe, tab_label, items_per_page, search_query="", selected_product="전체"):
    """데이터프레임을 HTML로 변환하여 스트림릿에 표시하는 함수"""
    if f'{tab_label}_filtered_df' not in st.session_state:
        st.session_state[f'{tab_label}_filtered_df'] = dataframe
    if f'{tab_label}_page_number' not in st.session_state:
        st.session_state[f'{tab_label}_page_number'] = 1

    dataframe = filter_dataframe(dataframe, search_query, selected_product)

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

    paged_df = URL_insert(paged_df)

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
            th, td {{
                padding: 8px;
                border: 1px solid #ddd;
                word-wrap: break-word;
            }}
            table {{
                width: 100%;
                table-layout: auto; /* 첫 번째 열을 제외한 나머지 열의 너비를 고정 */
                border-collapse: collapse;
            }}
            th {{
                background-color: #f2f2f2;
                text-align: center; /* 기본적으로 모든 헤더 값 가운데 정렬 */
            }}
            td {{
                text-align: center; /* 기본적으로 모든 행 값 가운데 정렬 */
            }}
            td:first-child {{
                width: auto; /* 첫 번째 열은 자동 너비 */
                text-align: left; 
            }}

            a {{
                color: inherit;
                text-decoration: none;
            }}
        </style>
        {table_html}
    </div>
    '''

    # 데이터프레임 표시
    components.html(table_html, height=400, scrolling=True)


def display_tab(dataframe, tab_label, items_per_page):
    """탭을 표시하고 검색 및 필터 기능을 추가하는 함수"""
    init_session_state(dataframe, tab_label)

    if st.button("필터 초기화", key=f"{tab_label}_reset_button"):
        reset_session_state(tab_label)

    search_query = st.session_state.get('search_query', "")
    selected_product = st.session_state.get(
        f'{tab_label}_selected_product', "전체")

    col1, col2 = st.columns([8, 2])

    with col1:
        search_query = st.text_input(
            "", search_query, placeholder="검색어를 입력해주세요", key=f"{tab_label}_search_input")
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
            "제품 구분", product_options, key=f"{tab_label}_select_tab")
        st.session_state[f'{tab_label}_selected_product'] = selected_product

    display_html_table(dataframe, tab_label, items_per_page,
                       search_query, selected_product)


def dashboard_button_df(df, column_name, status_list_counts, tab_name):

    URL_insert(df)
    if tab_name == "VoiceSDK":

        # 필요한 열만 남기고 제거
        df = df.drop(columns=['연관 제품', '기타문서 (견적서, NDA 등)',
                              "페이지URL", "📦 업무 일정", "계약 횟수", "계약관리"])

        # 데이터프레임 열 순서 변경
        columns_order = ["업체 이름", "상태", "개발언어", "담당자 이메일",
                         "컨택 업체 담당자", "계약종료일", "계약잔여일", "라이선스 수", "납품병원", "정보 최신화 날짜"]
        df = df.reindex(columns=columns_order)
        # ArrowInvalid 오류 해결을 위해 리스트 형태를 텍스트 값으로 변환
        df['납품병원'] = df['납품병원'].apply(
            lambda x: ', '.join(x) if isinstance(x, list) else x)
        # ArrowInvalid 오류 해결을 위해 리스트 형태를 텍스트 값으로 변환
        df['개발언어'] = df['개발언어'].apply(
            lambda x: ', '.join(x) if isinstance(x, list) else x)

    else:
        # 필요한 열만 남기고 제거
        df = df.drop(columns=['연관 제품', '기타문서 (견적서, NDA 등)',
                              "페이지URL", "📦 업무 일정", "계약 횟수", "개발언어", "계약관리"])

        # 데이터프레임 열 순서 변경
        columns_order = ["업체 이름", "상태", "담당자 이메일",
                         "컨택 업체 담당자", "계약종료일", "계약잔여일", "라이선스 수", "납품병원", "정보 최신화 날짜"]
        df = df.reindex(columns=columns_order)

        # ArrowInvalid 오류 해결을 위해 리스트 형태를 텍스트 값으로 변환
        df['납품병원'] = df['납품병원'].apply(
            lambda x: ', '.join(x) if isinstance(x, list) else x)

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
            filtered_df = df[df['상태'].str.contains(
                st.session_state.clicked_item, na=False)]

            if len(filtered_df) == 0:
                st.markdown("데이터가 존재하지 않습니다. 데이터가 추가되면 표시됩니다.")
            else:
                filtered_df = filtered_df.reset_index(drop=True)  # 인덱스 열 제거
                display_dataframe(filtered_df)


def display_dataframe(df):

    # '납품병원' 열 숨기기
    if '납품병원' in df.columns:
        df = df.drop('납품병원', axis=1)

    # 데이터프레임을 HTML로 변환
    df_html = df.to_html(index=False, escape=False)

   # 사용자 정의 CSS 및 HTML 삽입
    table_html = f'''
    <div style="height: 400px; width: 100vw; overflow: auto; margin: auto;">
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
            th, td {{
                padding: 8px;
                border: 1px solid #ddd;
                word-wrap: break-word;
            }}
            table {{
                width: 100%;
                table-layout: auto; /* 첫 번째 열을 제외한 나머지 열의 너비를 고정 */
                border-collapse: collapse;
            }}
            th {{
                background-color: #f2f2f2;
                text-align: center; /* 기본적으로 모든 헤더 값 가운데 정렬 */
            }}
            td {{
                text-align: center; /* 기본적으로 모든 행 값 가운데 정렬 */
            }}
            td:first-child {{
                width: auto; /* 첫 번째 열은 자동 너비 */
                text-align: left; 
            }}

            a {{
                color: inherit;
                text-decoration: none;
            }}
        </style>
        {df_html}
    </div>
    '''

    # 데이터프레임 표시
    components.html(table_html, height=400, scrolling=True)


def Crawling_page_text(url):
    try:
        # 페이지 가져오기
        response = requests.get(url)
        response.raise_for_status()  # 요청이 성공했는지 확인

        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 모든 텍스트 추출 (태그 사이의 텍스트)
        text = soup.get_text(separator=' ', strip=True)

        return text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# CSS 파일 로드 및 기본 제목과 메뉴 항목 숨기기


def load_css():
    with open("styles.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown("""
        <style>
        .css-1d391kg, .css-1y4p8pa {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

# 초기 페이지 설정


def set_initial_page():
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


def URL_insert(df):

    # '페이지URL' 열이 있는지 확인
    if '페이지URL' in df.columns:
        # 첫 번째 열에 하이퍼링크 직접 적용
        df.iloc[:, 0] = df.apply(
            lambda x: f'<a href="{x["페이지URL"]}" target="_blank">{x.iloc[0]}</a>', axis=1)

    df = df.drop(columns=["페이지URL"])

    return df
