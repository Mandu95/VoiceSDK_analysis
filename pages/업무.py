import streamlit as st
import streamlit_function as sf  # streamlit_function 모듈 임포트
import login_function as lf  # 로그인 모듈 임포트

st.set_page_config(page_title="업체 조회", layout="wide")


# 로그인 상태 확인
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.warning("로그인 후 접속해주세요.")
    st.stop()

else:

    from Ready_notion_DB import Task  # 데이터 로드

    # 로그아웃 버튼 추가
    lf.add_logout_button()

    def show_product_management():

        # 'age' 열을 기준으로 내림차순 정렬
        df = Task.sort_values(by='최종 편집 일시', ascending=False)
        df = Task.drop(
            columns=['요청자', '담당부서', '사업부 달력 (관련 일정)'])  # 필요한 열만 남기고 제거

        # 열 순서 변경
        columns_order = ['분류', '업무', '상태', '담당자',
                         '업무기간', '우선순위', '페이지URL', '관련 문서']
        df = df.reindex(columns=columns_order)

        st.subheader("업체 별 업무 진행상황 관리")
        st.write("Notion DB를 기준으로 분석한 자료입니다.:sunglasses:")

        sf.display_dataframe(df, "업무")

    if __name__ == "__main__":
        show_product_management()
