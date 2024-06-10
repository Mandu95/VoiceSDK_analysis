import streamlit as st
import pandas as pd
import streamlit_function as sf  # streamlit_function 모듈 임포트
import login_function as lf  # 로그인 모듈 임포트

st.set_page_config(page_title="데이터 조회", layout="wide")

# 로그인 상태 확인
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("로그인 후 접속해주세요")
    st.stop()

else:
    from ready_data import product_manage, etc_manage, contract_manage  # 데이터 로드

    # 로그아웃 버튼 추가
    lf.add_logout_button()

    # 계약서 관리 페이지 함수
    st.subheader("데이터 조회")
    st.write("업체 상태, 계약서, 견적서 등 데이터를 직접 조회합니다.:sunglasses:")

    def show_contract_management():
        st.write("정식/데모 계약서를 확인할 수 있습니다.:sunglasses:")

        # 필요 없는 열을 제거
        df = contract_manage.drop(columns=['제품', '제품 현황 관리', '계약경로', '매입/매출'])

        columns_order = ['계약명', '계약구분', '계약시작일', '라이선스 수', '계약단가',
                         '라이선스 총액', '계약총액', '문서확인', '사본링크', '페이지URL']
        df_reordered = df.reindex(columns=columns_order)

        sf.display_tab(df_reordered, "계약서 관리", 10)

    # 기타 문서 관리 페이지 함수
    def show_other_documents_management():
        st.write("업체로 발송 된 견적서, MOU 및 NDA 체결 문서를 볼 수 있습니다:sunglasses:")

        df = etc_manage.drop(
            columns=['발송 대상', '제품'])  # 필요한 열만 남기고 제거

        # 데이터프레임 열 순서 변경
        columns_order = ['문서이름', '라이선스 수', '계약단가',
                         '라이선스 총액', '계약총액', '견적 유효 마감일', '문서확인', '사본링크', '페이지URL']
        etc_manage_reordered = df.reindex(columns=columns_order)

        # sf.display_tab 함수 호출
        sf.display_tab(etc_manage_reordered, "기타 문서 관리", 10)

    # 제품 현황 관리 페이지 함수
    def show_product_management():
        df = product_manage.drop(
            columns=['개발언어', '납품병원', '연관 제품', '계약구분', '계약 횟수', '계약관리', '라이선스 수', '기타문서 (견적서, NDA 등)'])  # 필요한 열만 남기고 제거

        # 열 순서 변경
        columns_order = ['업체 이름', '상태', '담당자 이메일',
                         '컨택 업체 담당자', '계약시작일', '계약종료일', '계약잔여일', '정보 최신화 날짜', '페이지URL']
        df = df.reindex(columns=columns_order)

        st.write("Notion DB를 기준으로 분석한 자료이며, 오전 7시, 12시 하루 2회 동기화 됩니다.:sunglasses:")

        sf.display_tab(df, "제품 현황 관리", 10)

    # 탭 구성
    tab1, tab2, tab3 = st.tabs(["업체추적", "계약서", "기타서류"])

    with tab1:
        show_product_management()

    with tab2:
        show_contract_management()

    with tab3:

        show_other_documents_management()
