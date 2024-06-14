import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
from bs4 import BeautifulSoup
import real_data_analysis


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


#######################################################################################################

def make_button(df, tab_name):  # 데이터프레임 특정 열의 행 고유 값을 가지고 버튼 항목 만드는 함수 ################
    # VoiceSDK 탭 처리
    if tab_name == "VoiceSDK":
        temp_values = ['최초컨택', '자료발송', '사업설명',
                       '실무자회의', '협약', '견적발송', 'POC', '계약완료']

    else:
        if tab_name in ["VoiceMARK", "VoiceDOC"]:
            temp_values = ['데모요청', '사업설명', '견적발송', '계약중', '계약완료']
        elif tab_name == "VoiceENR":
            temp_values = ['자료발송', '사업설명', '견적발송', '계약중', '계약완료']
        elif tab_name == "VoiceEMR":
            temp_values = ['데모요청', '사업설명', '견적발송', '계약완료', '데모']

    return temp_values


# Streamlit Home 화면 Tab 메뉴 값을 기준으로 필터링 된 데이터프림 만드는 함수
def make_filter_df(df, tab_name, col_name=None):

    if col_name is None:
        # tab_name에 따라 데이터프레임 필터링
        if tab_name in df['제품'].unique():
            df = df[df['제품'] == tab_name]
    else:
        # tab_name에 따라 데이터프레임 필터링
        if tab_name in df[col_name].unique():
            df = df[df[col_name] == tab_name]
    return df


def Sort_Col_df(df, tab_name):  # 데이터 프레임 열 삭제 및 정렬 ################
    # VoiceSDK 탭 처리
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

#######################################################################################################


#######################################################################################################
def View_button(temp_values):  # 상단 버튼 표시
    # 상태 버튼 생성
    col_count = len(temp_values)
    cols = st.columns(col_count)
    return cols


# 버튼 클릭됐을 때 session 상태 변화 return 및 테이블 표시
def View_Table_by_clicked_button(df, temp_values, cols, status_counts, tab_name):
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
        filtered_df = df[df['상태'].str.contains(
            st.session_state.clicked_item, na=False)]
        if len(filtered_df) == 0:
            st.markdown("데이터가 존재하지 않습니다. 데이터가 추가되면 표시됩니다.")
        else:
            filtered_df = filtered_df.reset_index(drop=True)
            display_dataframe(filtered_df)

    return st.session_state.clicked_item


def View_table_Clicked_contract_complete(tab_name):
    import Mandu_DA
    all_contract_df, sell_df, buy_df, no_info_df = Mandu_DA.mandu_contract_main(
        tab_name)

    # Tab 메뉴 항목들
    tab_titles = ["전체", "매출/매입", "정보없음"]
    tabs = st.tabs(tab_titles)

    with tabs[0]:

        all_df = all_contract_df[0]

        # 상단에 선택박스 삽입
        col1, col2 = st.columns([8, 2])
        with col1:

            st.write(f"문서개수 : {len(all_df)}")
        with col2:
            selected_filter = filter_selectbox(
                f"{tabs}_filter", all_contract_df[1])

        if selected_filter != "전체":
            all_df = all_df[all_df['계약명'].str.contains(
                selected_filter, na=False)]

        if all_df.empty:
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
            display_dataframe(all_df)

    with tabs[1]:
        col10, col11 = st.columns([5, 5])
        with col10:
            contract_sell_df = sell_df[0]
            col1, col2 = st.columns([8, 2])
            with col1:
                st.write(f"문서개수 : {len(contract_sell_df)}")

            with col2:
                selected_filter = filter_selectbox(
                    f"{tabs}_filter_매출", sell_df[1])
                sell_sum = real_data_analysis.calculate_total_amount(
                    contract_sell_df, "계약총액")
            if selected_filter != "전체":
                contract_sell_df = contract_sell_df[contract_sell_df['계약명'].str.contains(
                    selected_filter, na=False)]
                sell_sum = real_data_analysis.calculate_total_amount(
                    contract_sell_df, "계약총액")
            if contract_sell_df.empty:
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
                display_dataframe(contract_sell_df)
                st.write(f"총 매출액 : {sell_sum}")
        with col11:

            # 상단에 선택박스 삽입
            contract_buy_df = buy_df[0]
            col1, col2 = st.columns([8, 2])
            with col1:

                st.write(f"문서개수 : {len(contract_buy_df)}")
            with col2:
                selected_filter = filter_selectbox(
                    f"{tabs}_filter_매입", buy_df[1])
            buy_sum = real_data_analysis.calculate_total_amount(
                contract_buy_df, "계약총액")
            if selected_filter != "전체":
                contract_buy_df = contract_buy_df[contract_buy_df['계약명'].str.contains(
                    selected_filter, na=False)]
                buy_sum = real_data_analysis.calculate_total_amount(
                    contract_buy_df, "계약총액")
            if contract_buy_df.empty:
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
                display_dataframe(contract_buy_df)
                st.write(f"총 매입액 : {buy_sum}")
    with tabs[2]:
        contract_noinfo_df = no_info_df[0]
        # 상단에 선택박스 삽입
        col1, col2 = st.columns([8, 2])
        with col1:
            st.write(f"문서개수 : {len(contract_noinfo_df)}")
        with col2:
            selected_filter = filter_selectbox(
                f"{tabs}_filter", no_info_df[1])
        if selected_filter != "전체":
            contract_noinfo_df = contract_noinfo_df[contract_noinfo_df['계약명'].str.contains(
                selected_filter, na=False)]
        if contract_noinfo_df.empty:
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
            display_dataframe(contract_noinfo_df)

#######################################################################################################


def dashboard_button_df(df, column_name, tab_name):

    # URL 삽입 함수 호출
    URL_insert(df)

    df = make_filter_df(df, tab_name)  # 데이터프레임 Tab 선택 항목에 맞춰 필터링
    df = Sort_Col_df(df, tab_name)  # 데이터프레임 Tab 선택 항목에 맞춰 열 삭제 및 정렬
    temp_values = make_button(df, tab_name)  # Tab 메뉴 별 상단 버튼 항목
    status_counts = df[column_name].value_counts().to_dict()     # 버튼 별 카운트 계산

    # streamlit web 화면 상에 버튼 개수에 맞춰 영역 할당 및 view
    cols = View_button(temp_values)
    session_status = View_Table_by_clicked_button(
        df, temp_values, cols, status_counts, tab_name)

    # 계약완료 버튼이 클릭됐을 때 아래 선택박스/테이블 표시를 위한 코드
    if session_status == "계약완료":
        View_table_Clicked_contract_complete(tab_name)

    recent_df = real_data_analysis.recent_data(df)
    # 데이터프레임의 "업체 이름" 열 값에서 HTML 태그 제거 및 텍스트만 추출하여 업데이트
    recent_df['업체 이름'] = recent_df['업체 이름'].apply(
        real_data_analysis.extract_text_from_html)

    # 상단에 검색창과 선택박스 삽입
    col20, col21 = st.columns([5, 5])
    with col20:
        # Streamlit 페이지 구성
        st.subheader("최근 2주간 업데이트")
        if recent_df.empty:
            st.write("데이터가 없습니다.")
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

            cols = st.columns(len(recent_df))
            for col, (index, row) in zip(cols, recent_df.iterrows()):
                # 고유한 키를 사용하여 같은 이름이 중복되는 경우 문제를 방지
                button_key = f"{row['업체 이름']}_{index}"
                if col.button(row['업체 이름'], key=button_key):
                    st.write(f"{row['업체 이름']} 버튼이 클릭되었습니다!")
                    # 클릭 시 세부 정보를 표시하는 expander
                    with st.expander("세부 정보 보기"):
                        st.write(f"업체 이름: {row['업체 이름']}")
                        st.write(f"정보 최신화 날짜: {row['정보 최신화 날짜']}")

    with col21:
        st.subheader("테스트")


def search_box(search_key, default=""):
    """검색창을 생성하는 함수"""
    return st.text_input("검색어를 입력하세요", default, key=search_key)


def filter_selectbox(filter_key, options, default="전체"):
    """필터 선택박스를 생성하는 함수"""
    return st.selectbox("필터 선택", options, index=options.index(default), key=filter_key)


def reset_filter_button(filter_key, search_key):
    """필터 초기화 버튼을 생성하는 함수"""
    if st.button("필터 초기화", key=f"{filter_key}_reset_button"):
        st.session_state[filter_key] = "전체"
        st.session_state[search_key] = ""


def display_dataframe(df, page_name=None):
    if page_name is not None:

        reset_filter_button(f"{page_name}_filter", f"{page_name}_search")

        # 상단에 검색창과 선택박스 삽입
        col1, col2 = st.columns([8, 2])

        with col1:
            search_query = search_box(f"{page_name}_search")

        with col2:
            if page_name == "업무":
                filter_options = df['분류'].dropna().unique().tolist()
                filter_options.insert(0, '전체')
                selected_filter = filter_selectbox(
                    f"{page_name}_filter", filter_options)
                df = URL_insert(df)
            else:
                filter_options = ["전체", "VoiceEMR", "VoiceENR",
                                  "VoiceSDK", "VoiceMARK", "VoiceEMR+", "VoiceDOC"]
                selected_filter = filter_selectbox(
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
                paged_df, total_pages, page_num = paginate_dataframe(
                    df, items_per_page, key_prefix=page_name)

            if page_name != "업무":
                paged_df = paged_df.drop(
                    columns=['제품'])  # 필요한 열만 남기고 제거

            # 데이터프레임을 HTML로 변환
            df_html = paged_df.to_html(index=False, escape=False)

            # 테이블 높이 계산
            table_height = calculate_table_height(paged_df)

            # 데이터프레임 표시
            components.html(show_table(df_html),
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
        components.html(show_table(df_html), height=400, scrolling=True)


def show_table(df_html):
    table_html = f'''
            <div style="height: 100%; width: 100%; overflow: auto; margin: auto;">
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
    return table_html


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

    # Drop specific columns and add links based on tab_label
    if '사본링크' in df.columns:
        df['사본링크'] = df['사본링크'].apply(
            lambda x: f'<a href="{x}" target="_blank" style="color: inherit;">문서 확인하기</a>')

    # Drop specific columns and add links based on tab_label
    if '관련 문서' in df.columns:
        df['관련 문서'] = df['관련 문서'].apply(
            lambda x: f'<a href="{x}" target="_blank" style="color: inherit;">문서 확인하기</a>')

    if '기타문서 (견적서, NDA 등)' in df.columns:
        df['문서확인'] = df['기타문서 (견적서, NDA 등)'].apply(
            lambda x: f'<a href="{x}" target="_blank" style="color: inherit;">문서 확인하기</a>')
        df = df.drop(columns=['기타문서 (견적서, NDA 등)'])

    return df


def paginate_dataframe(df, page_size, key_prefix=""):
    """데이터프레임을 페이지 단위로 나누고 페이지 번호를 선택할 수 있는 기능을 제공하는 함수"""
    total_items = len(df)
    total_pages = (total_items + page_size - 1) // page_size

    if total_pages > 0:
        # 페이지 번호 선택
        page_num = st.number_input(
            f"Page number ({key_prefix})",
            min_value=1,
            max_value=total_pages,
            step=1,
            value=1,
            key=f"{key_prefix}_page_num"
        )
    else:
        page_num = 1

    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size
    paged_df = df.iloc[start_index:end_index]

    return paged_df, total_pages, page_num


def calculate_table_height(df, row_height=30):
    """데이터프레임의 행 개수에 맞춰 테이블 높이를 계산하는 함수"""
    num_rows = len(df)
    table_height = num_rows * row_height
    return table_height
