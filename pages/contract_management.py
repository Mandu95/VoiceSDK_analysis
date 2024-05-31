import streamlit as st
from ready_data import contract_manage  # 데이터 로드
import streamlit_function as sf  # streamlit_function 모듈 임포트


def show_contract_management():
    st.set_page_config(page_title="계약서 조회", layout="wide")
    st.subheader("계약서 조회")
    st.write("정식/데모 계약서를 확인할 수 있습니다.:sunglasses:")

    # 필요 없는 열을 제거
    df = contract_manage.drop(columns=['제품', '제품 현황 관리', '계약경로', '매입/매출'])

    columns_order = ['계약명', '계약구분', '계약시작일', '라이선스 수', '계약단가',
                     '라이선스 총액', '계약총액', '문서확인', '사본링크', '페이지URL']
    df_reordered = df.reindex(columns=columns_order)

    sf.display_tab(df_reordered, "계약서 관리", 10)


if __name__ == "__main__":
    show_contract_management()
