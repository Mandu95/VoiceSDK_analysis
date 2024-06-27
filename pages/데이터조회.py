import streamlit as st
import login_function as lf  # 로그인 모듈 임포트
import Mandu_component
import component_sub

st.set_page_config(page_title="데이터 조회", layout="wide")

# 로그인 상태 확인
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("로그인 후 접속해주세요")
    st.stop()

else:

    # 로그아웃 버튼 추가
    lf.add_logout_button()

    # 계약서 관리 페이지 함수
    st.subheader("데이터 조회")
    st.write("업체 상태, 계약서, 견적서 등 데이터를 직접 조회합니다.:sunglasses:")

    def show_contract_management():
        # 세션 상태에 로딩된 데이터를 저장
        contract_manage = st.session_state['contract_manage']

        st.write("정식/데모 계약서를 확인할 수 있습니다.:sunglasses:")

        # 필요 없는 열을 제거
        contract_manage = contract_manage.drop(
            columns=['제품 현황 관리', '계약경로', '매입/매출'])

        columns_order = ['계약명', '계약구분', '계약시작일', '라이선스 수', '계약단가', '제품',
                         '라이선스 총액', '계약총액', '페이지URL']
        contract_manage = contract_manage.reindex(
            columns=columns_order)
        Mandu_component.display_dataframe(
            contract_manage, tab_name=None, page_name="계약서 관리", purpose=None)

    # 기타 문서 관리 페이지 함수
    def show_other_documents_management():
        # 세션 상태에 로딩된 데이터를 저장
        etc_manage = st.session_state['etc_manage']
        st.write("업체로 발송 된 견적서, MOU 및 NDA 체결 문서를 볼 수 있습니다:sunglasses:")

        etc_manage = etc_manage.drop(
            columns=['발송 대상'])  # 필요한 열만 남기고 제거

        # 데이터프레임 열 순서 변경
        columns_order = ['문서이름', '제품', '라이선스 수', '계약단가',
                         '라이선스 총액', '계약총액', '견적 유효 마감일', '페이지URL']
        etc_manage = etc_manage.reindex(columns=columns_order)

        Mandu_component.display_dataframe(
            etc_manage, tab_name=None, page_name="기타 문서 관리", purpose=None)

    # 제품 현황 관리 페이지 함수
    def show_product_management():
        # 세션 상태에 로딩된 데이터를 저장
        cop_manage = st.session_state['cop_manage_df']

        # 열 순서 변경
        columns_order = ['업체 이름', '상태', '제품', '담당자', '정보 최신화 날짜', '페이지URL']
        cop_manage = cop_manage.reindex(
            columns=columns_order)

        st.write("Notion DB를 기준으로 분석한 자료이며, 오전 7시, 12시 하루 2회 동기화 됩니다.:sunglasses:")

        Mandu_component.display_dataframe(
            cop_manage, tab_name=None, page_name="제품 현황 관리", purpose=None)

    # 제품 현황 관리 페이지 함수
    def show_customer_management():
        # 세션 상태에 로딩된 데이터를 저장
        customer_df = st.session_state['customer_df']
        # 열 순서 변경
        columns_order = ['고객 컨택 담당자', '프로젝트', '담당자 직급', '담당자 전화번호',
                         '담당자 이메일', '최초 컨택 날짜', '인/아웃바운드', '제품', '페이지URL']
        customer_df = customer_df.reindex(columns=columns_order)

        st.write("프로젝트 진행 중인 업체 별 담당자 정보 조회 입니다.")

        Mandu_component.display_dataframe(
            customer_df, tab_name=None, page_name="고객 관리", purpose=None)

    # 탭 구성
    tab1, tab2, tab3, tab4 = st.tabs(["업체추적", "계약서", "기타서류", "고객 담당자"])

    with tab1:
        show_product_management()

    with tab2:
        show_contract_management()

    with tab3:

        show_other_documents_management()

    with tab4:

        show_customer_management()
