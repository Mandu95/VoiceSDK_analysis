import streamlit as st
from Data_anal import contract_manage  # 데이터 로드
import streamlit_function as sf  # streamlit_function 모듈 임포트


def show_contract_management():
    st.subheader("계약서 관리")
    st.write("정식/데모 계약서를 확인할 수 있습니다.:sunglasses:")

    sf.display_tab(contract_manage, "계약서 관리", 10)


if __name__ == "__main__":
    show_contract_management()
