import streamlit as st
from ready_data import etc_manage  # 데이터프레임을 data_process 모듈에서 불러옴
import streamlit_function as sf  # streamlit_function 모듈 임포트

st.set_page_config(page_title="기타 서류 조회", layout="wide")


def show_other_documents_management():
    st.subheader("기타 문서 관리")
    st.write("업체로 발송 된 견적서, MOU 및 NDA 체결 문서를 볼 수 있습니다:sunglasses:")

    df = etc_manage.drop(
        columns=['발송 대상', '제품'])  # 필요한 열만 남기고 제거

    # 데이터프레임 열 순서 변경
    columns_order = ['문서이름', '라이선스 수', '계약단가',
                     '라이선스 총액', '계약총액', '견적 유효 마감일', '문서확인', '사본링크', '페이지URL']
    etc_manage_reordered = etc_manage.reindex(columns=columns_order)

    # sf.display_tab 함수 호출
    sf.display_tab(etc_manage_reordered, "기타 문서 관리", 10)


# 호출 예제
if __name__ == "__main__":
    show_other_documents_management()
