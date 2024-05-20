import streamlit as st
from data_process import etc_document  # 데이터프레임을 data_process 모듈에서 불러옴

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

# 데이터 프레임을 표시하고 페이징하는 함수
def display_paginated_table(dataframe, tab_label):
    """
    데이터프레임을 페이지 단위로 나누어 표시하는 함수.
    """
    if f'{tab_label}_filtered_df' not in st.session_state:
        st.session_state[f'{tab_label}_filtered_df'] = dataframe  # 기본값은 전체 데이터프레임
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
    
    # 표의 높이와 너비 설정
    table_height, table_width = get_table_dimensions()

    # 데이터프레임을 지정된 크기로 표시
    st.dataframe(paged_df, height=table_height, width=table_width)
    st.write(
        f"Displaying rows {(page_number - 1) * items_per_page + 1} to {min(page_number * items_per_page, total_items)} of {total_items}")

def show_other_documents_management():
    st.subheader("기타 문서 관리")
    # 기타 문서 관리에 대한 내용을 여기에 추가합니다.
    st.write("업체로 발송 된 견적서, MOU 및 NDA 체결 문서를 볼 수 있습니다:sunglasses:")

    # etc_document 데이터프레임 복사 및 인덱스 재설정
    etc_document_copy = etc_document.reset_index(drop=True)
    etc_document_copy.index = etc_document_copy.index + 1
    etc_document_copy.index.name = 'No'
    
    # etc_document 데이터프레임을 페이징하여 표시
    display_paginated_table(etc_document_copy, "기타 문서 관리")

# 호출 예제
if __name__ == "__main__":
    show_other_documents_management()
