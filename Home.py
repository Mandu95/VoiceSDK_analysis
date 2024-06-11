import streamlit as st
import logging
import streamlit_function as sf
import login_function as lf

# 메인 콘텐츠 표시


def main_content():
    sf.load_css()
    sf.set_initial_page()

    import real_data_analysis, ready_data

    company_df = ready_data.product_manage
    # contract_df = ready_data.contract_manage
    # etc_df = ready_data.etc_manage
    # task_df = ready_data.Task

    # 로그아웃 버튼 추가
    lf.add_logout_button()

    # 탭 구성
    tab_titles = ["VoiceEMR", "VoiceENR", "VoiceSDK", "VoiceMARK", "VoiceDOC"]
    tabs = st.tabs(tab_titles)

    with tabs[0]:
        sf.dashboard_button_df(
            company_df, "상태", "VoiceEMR")

    with tabs[1]:
        sf.dashboard_button_df(
            company_df, "상태", "VoiceENR")

    with tabs[2]:
        sf.dashboard_button_df(
            company_df, "상태", "VoiceSDK")

    with tabs[3]:
        sf.dashboard_button_df(
            company_df, "상태", "VoiceMARK")

    with tabs[4]:
        st.markdown("제품 개발을 위한 협약 단계에 있습니다. 차후 데이터가 업로드 되면 표시됩니다.")

# 메인 함수


def main():
    st.set_page_config(page_title="PuzzleAI's Dashboard",
                       layout="wide")

    logging.basicConfig(filename='data_sync.log',
                        level=logging.INFO, format='%(asctime)s - %(message)s')

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['signup'] = False

    if st.session_state['logged_in']:
        main_content()
    else:
        if st.session_state['signup']:
            lf.signup_screen()
        else:
            lf.login_screen()


if __name__ == "__main__":
    main()
