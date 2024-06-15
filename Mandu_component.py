import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import re



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

# '페이지URL' 열이 있는지 확인하고 하이퍼링크 적용
def URL_insert(df):
    # '페이지URL' 열이 있는지 확인하고 하이퍼링크 적용
    if '페이지URL' in df.columns:
        df.iloc[:, 0] = df.apply(
            lambda x: f'<a href="{x["페이지URL"]}" target="_blank">{x.iloc[0]}</a>' if pd.notna(x['페이지URL']) else x.iloc[0], axis=1)
        df = df.drop(columns=["페이지URL"])

    # '사본링크' 열이 있으면 하이퍼링크 적용
    if '사본링크' in df.columns:
        df['사본링크'] = df['사본링크'].apply(
            lambda x: f'<a href="{x}" target="_blank" style="color: inherit;">문서 확인하기</a>' if pd.notna(x) else '')

    # '관련 문서' 열이 있으면 하이퍼링크 적용
    if '관련 문서' in df.columns:
        df['관련 문서'] = df['관련 문서'].apply(
            lambda x: f'<a href="{x}" target="_blank" style="color: inherit;">문서 확인하기</a>' if pd.notna(x) else '')

    # '기타문서 (견적서, NDA 등)' 열이 있으면 하이퍼링크 적용하고 열 이름을 '문서확인'으로 변경
    if '기타문서 (견적서, NDA 등)' in df.columns:
        df['문서확인'] = df['기타문서 (견적서, NDA 등)'].apply(
            lambda x: f'<a href="{x}" target="_blank" style="color: inherit;">문서 확인하기</a>' if pd.notna(x) else '')
        df = df.drop(columns=['기타문서 (견적서, NDA 등)'])

    return df


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




## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# 데이터프레임의 특정 열의 고유 행 값을 추출하기 위한 함수, 고유 값 추출 된 행은 삭제되도록 설계해둠.
def extract_column_unique_value(df, col_name=None): 

    if col_name is not None:

        unique_value = df[col_name].unique()
        df = df.drop(
            columns=[col_name])
        unique_value = unique_value.tolist()
        unique_value.insert(0, '전체')
        unique_value = [re.sub(r'\[.*?\]\s*', '', item)
                        for item in unique_value]

        return unique_value

def table_columns_select(df,tab_name):
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
            
    else :
            # 필요한 열만 남기고 제거
            df = df.drop(columns=['기타문서 (견적서, NDA 등)', "페이지URL",
                        "📦 업무 일정", "계약 횟수", "개발언어", "계약관리", "납품병원"])
            # 데이터프레임 열 순서 변경
            columns_order = ["업체 이름", "상태", "담당자 이메일",
                            "컨택 업체 담당자", "계약종료일", "계약잔여일", "라이선스 수", "정보 최신화 날짜"]
            df = df.reindex(columns=columns_order)
    
    return df


def preprocess_df(df,tab_name) : 
    
    df = URL_insert(df)
    # VoiceSDK 탭 처리
    if tab_name == "VoiceSDK":
        temp_values = ['최초컨택', '자료발송', '사업설명',
                       '실무자회의', '협약', '견적발송', 'POC', '계약완료']
        # 필요한 열만 남기고 제거
        df = df.drop(columns=["📦 업무 일정", "계약 횟수", "계약관리", "납품병원", "제품"])
        # 데이터프레임 열 순서 변경
        columns_order = ["업체 이름", "상태", "개발언어", "담당자 이메일",
                         "컨택 업체 담당자", "계약종료일", "계약잔여일", "라이선스 수", "정보 최신화 날짜"]
        df = df.reindex(columns=columns_order)

    else:
        if tab_name in ["VoiceENR", "VoiceMARK", "VoiceDOC"]:
            temp_values = ['데모요청', '사업설명', '견적발송', '계약중', '계약완료']
        elif tab_name == "VoiceEMR":
            temp_values = ['데모요청', '사업설명', '견적발송', '계약완료', '데모']

        # 필요한 열만 남기고 제거
        df = df.drop(columns=["📦 업무 일정", "계약 횟수", "개발언어", "계약관리", "납품병원"])
        # 데이터프레임 열 순서 변경
        columns_order = ["업체 이름", "상태", "담당자 이메일",
                         "컨택 업체 담당자", "계약종료일", "계약잔여일", "라이선스 수", "정보 최신화 날짜"]
        df = df.reindex(columns=columns_order)
    
    return df, temp_values

def component_top_button(df,tab_name):

    df, temp_values = preprocess_df(df,tab_name)
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
        df = df[df['상태']==st.session_state.clicked_item]
        if len(df) == 0:
            st.markdown("데이터가 존재하지 않습니다. 데이터가 추가되면 표시됩니다.")
        else:
            df = df.reset_index(drop=True)
            display_dataframe(df)

            # 계약완료 버튼이 클릭됐을 때 아래 선택박스/테이블 표시를 위한 코드
            if st.session_state.clicked_item == "계약완료":

                # Tab 메뉴 항목들
                tab_titles = ["전체", "매출/매입", "정보없음"]
                tabs = st.tabs(tab_titles)

                with tabs[0]:
                    Data_all_df = st.session_state['매입/매출 전체 데이터']
                    all_select_values = extract_column_unique_value(Data_all_df,"제품 현황 관리")
                    col1, col2 = st.columns([8, 2])
                    with col1:

                        st.write(f"문서개수 : {len(Data_all_df)}")
                    with col2:
                        selected_filter = filter_selectbox(
                            f"{tabs}_filter", all_select_values)
                with tabs[1]:
                    Data_buy_df  = st.session_state['매입/매출 매출 데이터']
                    buy_select_values = extract_column_unique_value(Data_buy_df,"제품 현황 관리")
                    Data_sell_df = st.session_state['매입/매출 매입 데이터']
                    sell_select_values = extract_column_unique_value(Data_sell_df,"제품 현황 관리")                    
                    
                    
                    col10, col11 = st.columns([5, 5])

                    with col10:
                        col1, col2 = st.columns([8, 2])
                        with col1:
                            st.write(f"문서개수 : {len(Data_buy_df)}")
                        with col2:
                            selected_filter = filter_selectbox(
                                f"{tabs}_filter", buy_select_values)
                            
                    with col11:
                        with col1:
                            st.write(f"문서개수 : {len(Data_sell_df)}")
                        with col2:
                            selected_filter = filter_selectbox(
                                f"{tabs}_filter", sell_select_values) 
                with tabs[2]:
                    Data_no_info_df = st.session_state['매입/매출 정보없음 데이터']
                    no_info_select_values = extract_column_unique_value(Data_no_info_df,"제품 현황 관리")
                    col1, col2 = st.columns([8, 2])
                    with col1:

                        st.write(f"문서개수 : {len(Data_no_info_df)}")
                    with col2:
                        selected_filter = filter_selectbox(
                            f"{tabs}_filter", no_info_select_values)