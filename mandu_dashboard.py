import streamlit as st
import data_process
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
    st.title("Welcome to PuzzleAI's Dashboard")
    st.write("Use the sidebar to navigate to different sections.")

# 데이터 동기화를 위한 함수


def update_data():
    global df, url_data
    df = data_process.df
    url_data = data_process.url_df
    logging.info("데이터 로드 성공")
    st.experimental_rerun()

# 스케줄 설정


def setup_schedule():
    schedule.every().day.at("09:00").do(update_data)
    schedule.every().day.at("16:00").do(update_data)

# 백그라운드에서 스케줄러 실행


def run_scheduler():
    while True:
        if datetime.now().weekday() < 5:
            schedule.run_pending()
        time.sleep(1)

# 메인 함수


def main():
    load_css()
    set_initial_page()
    setup_schedule()

    # 스케줄러를 백그라운드에서 실행
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()


if __name__ == "__main__":
    main()
