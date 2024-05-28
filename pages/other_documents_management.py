import streamlit as st
from Data_anal import etc_manage  # 데이터프레임을 data_process 모듈에서 불러옴

# 표 높이와 너비 동적으로 설정하는 함수


def get_table_dimensions():
    return 385, 2400  # 표의 높이와 너비를 설정

# 데이터프레임을 페이징하는 함수


def paginate_data(dataframe, page_number, items_per_page):
    """
    데이터프레임을 페이지 번호에 따라 분할하여 반환하는 함수.
    """
    start_index = (page_number - 1) * items_per_page
    end_index = start_index + items_per_page
    paged_df = dataframe.iloc[start_index:end_index]

    # 인덱스를 1부터 시작하도록 설정 (범위를 데이터프레임의 길이에 맞추어 조정)
    paged_df.index = range(start_index + 1, start_index + 1 + len(paged_df))
    return paged_df

# 특정 열의 값을 금액 단위로 포맷팅


def format_currency(value):
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return value

# "라이선스 수" 열의 값을 일반 숫자 텍스트로 포맷팅 (소숫점 제거)


def format_license_count(value):
    try:
        return f"{int(value)}"
    except (ValueError, TypeError):
        return value

# "제품" 열의 리스트 형태 값을 텍스트로 나열


def format_product_list(value):
    if isinstance(value, list):
        return ", ".join(value)
    return value

# 데이터 프레임을 HTML로 변환하여 표시하는 함수


def display_html_table(dataframe, tab_label):
    """
    데이터프레임을 HTML 형태의 표로 변환하여 페이지 단위로 나누어 표시하는 함수.
    """
    if f'{tab_label}_filtered_df' not in st.session_state:
        # 기본값은 전체 데이터프레임
        st.session_state[f'{tab_label}_filtered_df'] = dataframe
    if f'{tab_label}_page_number' not in st.session_state:
        st.session_state[f'{tab_label}_page_number'] = 1  # 기본 페이지 번호는 1

    total_items = len(dataframe)
    items_per_page = 10  # 페이지당 항목 수 설정
    total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)

    # 페이지 번호 입력 상자를 표 상단 맨 오른쪽에 배치
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

    # "발송대상"과 "사본링크" 열을 숨기고 "문서 확인하기" 열 추가
    if '발송 대상' in paged_df.columns:
        paged_df = paged_df.drop(columns=['발송 대상'])
    if '사본링크' in paged_df.columns:
        paged_df['문서 확인하기'] = paged_df['사본링크'].apply(
            lambda x: f'<a href="{x}" target="_blank">문서 확인하기</a>')
        paged_df = paged_df.drop(columns=['사본링크'])

    # "페이지URL"을 "문서이름"에 하이퍼링크로 추가
    if '페이지URL' in paged_df.columns:
        paged_df['문서이름'] = paged_df.apply(
            lambda row: f'<a href="{row["페이지URL"]}" style="color: black;">{row["문서이름"]}</a>', axis=1)
        paged_df = paged_df.drop(columns=['페이지URL'])

    # '제품' 열 제거
    if '제품' in paged_df.columns:
        paged_df = paged_df.drop(columns=['제품'])

    # 적용할 열에 대한 포맷팅 함수 적용
    currency_columns = ['라이선스 총액', '계약단가', '계약총액']
    for col in currency_columns:
        if col in paged_df.columns:
            paged_df[col] = paged_df[col].apply(format_currency)

    if '라이선스 수' in paged_df.columns:
        paged_df['라이선스 수'] = paged_df['라이선스 수'].apply(format_license_count)

    if '제품' in paged_df.columns:
        paged_df['제품'] = paged_df['제품'].apply(format_product_list)

    # 모든 값을 문자열 형태로 변환
    paged_df = paged_df.applymap(str)

    # 표의 높이와 너비 설정
    table_height, table_width = get_table_dimensions()

    # 데이터프레임을 HTML로 변환하여 스타일 추가 (열 이름만 가운데 정렬)
    styled_df = paged_df.style.set_table_styles(
        [{
            'selector': 'th',
            'props': [('text-align', 'center')]
        }]
    ).set_properties(**{'text-align': 'left'})

    table_html = styled_df.to_html(escape=False, index=False)
    table_html = f'''
    <div style="height: {table_height}px; width: {table_width}px; overflow: auto;">
        {table_html}
    </div>
    '''

    # 데이터프레임을 지정된 크기로 표시 (HTML로 스타일링 포함)
    st.write(
        table_html,
        unsafe_allow_html=True
    )
    st.write(
        f"Displaying rows {(page_number - 1) * items_per_page + 1} to {min(page_number * items_per_page, total_items)} of {total_items}"
    )

# 문서 관리 페이지를 표시하는 함수


def show_other_documents_management():
    st.subheader("기타 문서 관리")
    st.write("업체로 발송 된 견적서, MOU 및 NDA 체결 문서를 볼 수 있습니다:sunglasses:")

    col1, col2 = st.columns([8, 2])

    with col1:
        search_query = st.text_input(
            "",
            value=st.session_state.get('search_query', ''),
            placeholder="문서와 관련 된 업체 또는 병원 이름을 검색해주세요.",
            key='search_input'
        )
        st.session_state['search_query'] = search_query

    with col2:
        # 탭 메뉴를 selectbox로 대체
        tab_label = st.selectbox(
            "문서 구분",
            ["전체", "VoiceEMR", "VoiceENR", "VoiceSDK", "VoiceMARK", "VoiceDOC"],
            key='select_tab'
        )

    # 탭 메뉴와 검색어에 따른 데이터 필터링
    if tab_label == "전체":
        filtered_data = etc_manage
    else:
        filtered_data = etc_manage[etc_manage['문서이름'].str.contains(
            tab_label, case=False, na=False)]

    if search_query:
        filtered_data = filtered_data[filtered_data['문서이름'].str.contains(
            search_query, case=False, na=False)]

    filtered_data = filtered_data.reset_index(drop=True)
    filtered_data.index = filtered_data.index + 1
    filtered_data.index.name = 'No'

    if filtered_data.empty:
        st.markdown(
            """
            <div class="no-data">데이터가 없습니다</div>
            """, unsafe_allow_html=True)
    else:
        display_html_table(filtered_data, tab_label)


# 호출 예제
if __name__ == "__main__":
    show_other_documents_management()
