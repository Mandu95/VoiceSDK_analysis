import streamlit as st
from Data_anal import product_manage  # 데이터 로드
import streamlit_function as sf  # streamlit_function 모듈 임포트


def show_product_management():
    df = product_manage.drop(
        columns=['개발언어', '계약관리', '납품병원', '기타문서 (견적서, NDA 등)', '연관 제품', '계약구분', '계약 횟수'])  # 필요한 열만 남기고 제거

    st.subheader("제품 현황 관리")
    st.write("Notion DB를 기준으로 분석한 자료이며, 오전 8시, 12시, 15시 하루 3회 동기화 됩니다.:sunglasses:")

    sf.display_tab(df, "제품 현황 관리", 10)


if __name__ == "__main__":
    show_product_management()
