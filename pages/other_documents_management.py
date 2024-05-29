import streamlit as st
from Data_anal import etc_manage  # 데이터프레임을 data_process 모듈에서 불러옴
import streamlit_function as sf  # streamlit_function 모듈 임포트


def show_other_documents_management():
    st.subheader("기타 문서 관리")
    st.write("업체로 발송 된 견적서, MOU 및 NDA 체결 문서를 볼 수 있습니다:sunglasses:")

    sf.display_tab(etc_manage, "기타 문서 관리", 10)


# 호출 예제
if __name__ == "__main__":
    show_other_documents_management()
