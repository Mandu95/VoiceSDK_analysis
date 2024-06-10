import streamlit as st
import logging
import streamlit_function as sf
import login_function as lf

# 메인 콘텐츠 표시


def main_content():
    sf.load_css()
    sf.set_initial_page()

    import real_data_analysis

    # 로그아웃 버튼 추가
    lf.add_logout_button()

    # 탭 구성
    tab_titles = ["VoiceEMR", "VoiceENR", "VoiceSDK", "VoiceMARK", "VoiceDOC"]
    tabs = st.tabs(tab_titles)

    with tabs[0]:
        notion_df, result = real_data_analysis.main("VoiceEMR")
        sf.dashboard_button_df(
            notion_df[0], "상태", result, "VoiceEMR")

    with tabs[1]:
        notion_df, result = real_data_analysis.main("VoiceENR")
        sf.dashboard_button_df(
            notion_df[0], "상태", result, "VoiceENR")

    with tabs[2]:
        notion_df, result = real_data_analysis.main("VoiceSDK")
        sf.dashboard_button_df(
            notion_df[0], "상태", result, "VoiceSDK")

    with tabs[3]:
        notion_df, result = real_data_analysis.main("VoiceMARK")
        sf.dashboard_button_df(
            notion_df[0], "상태", result, "VoiceMARK")

    with tabs[4]:
        st.markdown("제품 개발을 위한 협약 단계에 있습니다. 차후 데이터가 업로드 되면 표시됩니다.")

# 메인 함수


def main():
    st.set_page_config(page_title="PuzzleAI's Dashboard", layout="wide")

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
