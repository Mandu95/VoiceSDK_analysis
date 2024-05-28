import streamlit as st
import pandas as pd
from Data_anal import contract_manage  # 데이터 로드
import streamlit_function as sf  # streamlit_function 모듈 임포트


def show_contract_management():

    st.subheader("계약서 관리")
    st.write("정식/데모 계약서를 확인할 수 있습니다.:sunglasses:")

    items_per_page = 10  # 페이지당 항목 수 설정

    # 세션 초기화
    sf.init_session_state(contract_manage, "전체")

    # 데이터 표시
    tab_label = st.session_state['select_tab_전체'] if 'select_tab_전체' in st.session_state else "전체"
    if tab_label == "전체":
        filtered_data = contract_manage
    else:
        filtered_data = contract_manage[contract_manage['제품'].apply(
            lambda x: tab_label in x if isinstance(x, list) else str(x) == tab_label)]

    filtered_data = filtered_data.reset_index(drop=True)
    filtered_data.index = filtered_data.index + 1
    filtered_data.index.name = 'No'

    sf.display_tab(contract_manage, filtered_data, tab_label, items_per_page)


if __name__ == "__main__":
    show_contract_management()
