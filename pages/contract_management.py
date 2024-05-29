import streamlit as st
from Data_anal import contract_manage  # 데이터 로드
import streamlit_function as sf  # streamlit_function 모듈 임포트


def show_contract_management():
    st.subheader("계약서 관리")
    st.write("정식/데모 계약서를 확인할 수 있습니다.:sunglasses:")

    # 필요 없는 열을 제거
    df = contract_manage.drop(columns=['제품 현황 관리', '계약경로', '매입/매출'])

    sf.display_tab(df, "계약서 관리", 10)


if __name__ == "__main__":
    show_contract_management()
