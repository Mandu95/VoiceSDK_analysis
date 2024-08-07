import streamlit as st
import pandas as pd
import re


# display dataframe 할 때 css 값
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

# 검색창 생성하는 함수


def search_box(search_key, default=""):
    return st.text_input("검색어를 입력하세요", default, key=search_key)

# 필터 선택박스 생성하는 함수


def filter_selectbox(filter_key, options, default="전체"):
    """필터 선택박스를 생성하는 함수"""
    return st.selectbox("필터 선택", options, index=options.index(default), key=filter_key)


# 필터 초기화 버튼 생성하는 함수
def reset_filter_button(filter_key, search_key):
    """필터 초기화 버튼을 생성하는 함수"""
    if st.button("필터 초기화", key=f"{filter_key}_reset_button"):
        st.session_state[filter_key] = "전체"
        st.session_state[search_key] = ""


# 페이징 기능 삽입
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


# 테이블 높이 계산하는 함수
def calculate_table_height(df, row_height=30):
    """데이터프레임의 행 개수에 맞춰 테이블 높이를 계산하는 함수"""
    num_rows = len(df)
    table_height = num_rows * row_height
    return table_height


# '페이지URL' 열이 있는지 확인하고 하이퍼링크 적용
def URL_insert(df):

    if df is None:
        display_empty_message(f"검색 결과가 없습니다.")

    else:
        if '페이지URL' in df.columns:
            df.iloc[:, 0] = df.apply(
                lambda x: f'<a href="{x["페이지URL"]}" target="_blank">{x.iloc[0]}</a>' if pd.notna(x['페이지URL']) else x.iloc[0], axis=1)
            df = df.drop(columns=["페이지URL"])

        link_columns = {
            '사본링크': '문서 확인하기',
            '관련 문서': '문서 확인하기',
            '기타문서 (견적서, NDA 등)': '문서 확인하기'
        }

        for col, link_text in link_columns.items():
            if col in df.columns:
                df[col] = df[col].apply(
                    lambda x: f'<a href="{x}{link_text}</a>' if pd.notna(x) else '')
                if col == '기타문서 (견적서, NDA 등)':
                    df.rename(columns={col: '문서확인'}, inplace=True)

        return df


def load_css():
    with open("styles.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown("""
        <style>
        .css-1d391kg, .css-1y4p8pa {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)


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


def columns_select(df, tab_name, page_name=None):

    if page_name is not None:
        if page_name == "두번째레이어 오른쪽":
            # 데이터프레임 열 순서 변경
            columns_order = ["업체 이름", "상태", "개발언어", "정보 최신화 날짜"]
            df = df.reindex(columns=columns_order)

            return df

        elif page_name == "두번째레이어 왼쪽":
            # 데이터프레임 열 순서 변경
            columns_order = ["업체 이름", "정보 최신화 날짜"]
            df = df.reindex(columns=columns_order)

            return df

        elif page_name == "계약완료 버튼클릭":
            # 데이터프레임 열 순서 변경
            columns_order = ["계약명", "계약총액", "페이지URL"]

            df = df.reindex(columns=columns_order)
            df = URL_insert(df)

            return df

        elif page_name == "세번째레이어":
            # 데이터프레임 열 순서 변경
            columns_order = ["업체 이름", "상태", "개발언어",
                             "컨택 업체 담당자", "정보 최신화 날짜"]
            df = df.reindex(columns=columns_order)

            return df
        elif page_name == "업체 조회_데이터조회탭":
            # 데이터프레임 열 순서 변경
            columns_order = ["업체 이름", "상태", "컨택 업체 담당자"]
            df = df.reindex(columns=columns_order)

            return df

    else:
        if tab_name == "VoiceSDK":
            # 필요한 열만 남기고 제거
            df = df.drop(columns=['기타문서 (견적서, NDA 등)', "페이지URL",
                                  "📦 업무 일정", "계약 횟수", "계약관리", "납품병원", "제품"])
            # 데이터프레임 열 순서 변경
            columns_order = ["업체 이름", "상태", "개발언어",
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
            columns_order = ["업체 이름", "상태",
                             "컨택 업체 담당자", "계약종료일", "계약잔여일", "라이선스 수", "정보 최신화 날짜"]
            df = df.reindex(columns=columns_order)

        return df


def preprocess_df(df, tab_name):

    # VoiceSDK 탭 처리
    if tab_name == "VoiceSDK":
        temp_values = ['자료발송', '사업설명', '협약', 'POC', '계약완료', "협업취소"]
        # # 필요한 열만 남기고 제거
        # df = df.drop(columns=["📦 업무 일정", "계약관리", "납품병원", "제품"])
        # 데이터프레임 열 순서 변경
        columns_order = ["업체 이름", "상태", "개발언어",
                         "담당자", "주소", "정보 최신화 날짜"]
        df = df.reindex(columns=columns_order)

    elif tab_name == "VUNO":
        temp_values = ['협약', '계약완료', '계약종료']
        # # 필요한 열만 남기고 제거
        # df = df.drop(columns=["📦 업무 일정", "계약관리", "납품병원", "제품"])
        # 데이터프레임 열 순서 변경
        columns_order = ["업체 이름", "상태"]
        df = df.reindex(columns=columns_order)

    else:
        if tab_name in ["VoiceENR", "VoiceMARK", "VoiceDOC", "VUNO"]:
            temp_values = ['데모요청', '사업설명', '견적발송', '계약중', '계약완료']
        elif tab_name == "VoiceEMR":
            temp_values = ['데모요청', '사업설명', '견적발송', '계약완료', '데모']

        # # 필요한 열만 남기고 제거
        # df = df.drop(columns=["📦 업무 일정", "개발언어", "계약관리", "납품병원"])
        # 데이터프레임 열 순서 변경
        columns_order = ["업체 이름", "상태", "담당자", "주소", "정보 최신화 날짜"]
        df = df.reindex(columns=columns_order)

    return df, temp_values


def View_table(selected_filter, df, purpose=None):
    # df가 DataFrame인지 확인
    if isinstance(df, pd.DataFrame):
        if purpose is not None:
            if purpose == "계약완료 버튼클릭":
                if selected_filter != "전체":
                    df = df[df['계약명'].str.contains(selected_filter, na=False)]

                # DataFrame이 비어 있는지 확인
                if df.empty:
                    # df가 DataFrame이 아닐 때 오류 메시지 출력
                    display_empty_message(f"검색 결과가 없습니다.")
                else:

                    return df
    else:
        # df가 DataFrame이 아닐 때 오류 메시지 출력
        display_empty_message(f"해당되는 데이터가 없습니다.")


def display_empty_message(message):
    """데이터가 없을 때 메시지를 표시하는 함수"""
    st.markdown(
        f"""
        <style>
            .empty-message {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 10vh;
                font-size: 1em;
                color: black;
            }}
        </style>
        <div class="empty-message">{message}</div>
        """,
        unsafe_allow_html=True
    )


def display_bar_chart(df):
    print("아")
