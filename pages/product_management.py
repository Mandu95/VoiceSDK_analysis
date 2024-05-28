import streamlit as st
import pandas as pd
from Data_anal import product_manage  # 데이터 로드
import streamlit_function as sf  # streamlit_function 모듈 임포트


def show_product_management():
    df = product_manage.drop(
        columns=['개발언어', '계약관리', '납품병원', '기타문서 (견적서, NDA 등)'])  # 필요한 열만 남기고 제거

    st.subheader("제품 현황 관리")
    st.write("Notion DB를 기준으로 분석한 자료이며, 오전 8시, 12시, 15시 하루 3회 동기화 됩니다.:sunglasses:")
    items_per_page = 10  # 페이지당 항목 수 설정

    # 세션 초기화
    sf.init_session_state(df, "전체")

    # 데이터 표시
    tab_label = st.session_state['select_tab'] if 'select_tab' in st.session_state else "전체"
    if tab_label == "전체":
        filtered_data = df
    else:
        filtered_data = product_manage[product_manage['연관 제품'].apply(
            lambda x: tab_label in x if isinstance(x, list) else tab_label == x)]
        filtered_data = filtered_data.drop(
            columns=['개발언어', '계약관리', '납품병원', '기타문서 (견적서, NDA 등)'])

    filtered_data = filtered_data.reset_index(drop=True)
    filtered_data.index = filtered_data.index + 1
    filtered_data.index.name = 'No'

    sf.display_tab(df, filtered_data, tab_label, items_per_page)


if __name__ == "__main__":
    show_product_management()
