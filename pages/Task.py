import streamlit as st
from Data_anal import Task  # 데이터 로드
import streamlit_function as sf  # streamlit_function 모듈 임포트

st.set_page_config(page_title="업체 조회", layout="wide")


def show_product_management():
    df = Task.drop(
        columns=['요청자', '담당부서', '파일과 미디어', '관련 문서', '사업부 달력 (관련 일정)'])  # 필요한 열만 남기고 제거

    # 열 순서 변경
    columns_order = ['업무', '상태', '담당자',
                     '업무기간', '요청자', '우선순위']
    df = df.reindex(columns=columns_order)

    st.subheader("업체 별 업무 진행상황 관리")
    st.write("Notion DB를 기준으로 분석한 자료입니다.:sunglasses:")

    sf.display_tab(df, "업무 관리", 10)


if __name__ == "__main__":
    show_product_management()
