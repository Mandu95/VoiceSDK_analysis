import streamlit as st
import streamlit_function
import real_data_analysis
import threading
import schedule
from datetime import datetime
import logging
import time


# 페이지 설정
st.set_page_config(page_title="PuzzleAI's Dashboard", layout="wide")

# 로그 설정
logging.basicConfig(filename='data_sync.log',
                    level=logging.INFO, format='%(asctime)s - %(message)s')

# CSS 파일 로드 및 기본 제목과 메뉴 항목 숨기기


def load_css():
    with open("styles.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown("""
        <style>
        .css-1d391kg, .css-1y4p8pa {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

# 초기 페이지 설정


def set_initial_page():
    # 페이지 레이아웃 설정
    col_header, col_buttons = st.columns([8, 2])
    with col_header:
        st.header("Welcome to PuzzleAI's Dashboard")

    # styles.css 파일 로드
    with open("styles.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    with col_buttons:
        st.markdown(
            """
            <div class="button-container">
                <a href="https://www.notion.so/puzzleai/69aeff6ca32d4466ad4748dde3939e8b?v=3de75aac58cd42978178f02e0b3d7707" target="_blank">
                    <button class="button notion-button">고객 관리</button>
                </a>
                <a href="https://puszleai-my.sharepoint.com/:f:/g/personal/mandu95_puzzle-ai_com/Egh0NiS6DdRPo8ej06sndswB7z9FOPB7OIAArnEenTObvw?e=igldVp" target="_blank">
                    <button class="button onedrive-button">사업부 공유폴더</button>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

# 데이터 동기화를 위한 함수


def main():
    load_css()
    set_initial_page()

    # 탭 구성
    tab_titles = ["VoiceEMR", "VoiceENR",
                  "VoiceSDK", "VoiceMARK", "VoiceDOC"]
    tabs = st.tabs(tab_titles)

    with tabs[0]:
        # 여기 VoiceEMR 페이지에 보여줄 데이터를 추가하세요.
        notion_df, result = real_data_analysis.main("VoiceEMR")
        streamlit_function.dashboard_button_df(
            notion_df[0], "상태", result, "VoiceEMR")

    with tabs[1]:
        # 여기 VoiceEMR 페이지에 보여줄 데이터를 추가하세요.
        notion_df, result = real_data_analysis.main("VoiceENR")

        streamlit_function.dashboard_button_df(
            notion_df[0], "상태", result, "VoiceENR")

    with tabs[2]:
        # 여기 VoiceEMR 페이지에 보여줄 데이터를 추가하세요.
        notion_df, result = real_data_analysis.main("VoiceSDK")
        streamlit_function.dashboard_button_df(
            notion_df[0], "상태", result, "VoiceSDK")

    with tabs[3]:
        # 여기 VoiceEMR 페이지에 보여줄 데이터를 추가하세요.
        notion_df, result = real_data_analysis.main("VoiceMARK")

        streamlit_function.dashboard_button_df(
            notion_df[0], "상태", result, "VoiceMARK")

    with tabs[4]:
        st.markdown("제품 개발을 위한 협약 단계에 있습니다. 차후 데이터가 업로드 되면 표시됩니다.")

        # streamlit_function.dashboard_button_df(notion_df[0],"상태",result,"VoiceDOC")


if __name__ == "__main__":
    main()
