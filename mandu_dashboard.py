import streamlit as st
import pandas as pd
import data_process
import time
import threading
import schedule
from datetime import datetime
import logging

# 페이지 설정
st.set_page_config(page_title="PuzzleAI's Dashboard", layout="wide")

# 로그 설정
logging.basicConfig(filename='data_sync.log',
                    level=logging.INFO, format='%(asctime)s - %(message)s')

# 데이터 로드
df = data_process.df
url_data = data_process.url_df

# CSS 파일 로드
with open("styles.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# 메뉴 선택을 위한 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "제품 현황 관리"

# 선택 박스를 사용하여 메뉴 선택
menu = st.sidebar.selectbox("탭 메뉴", ["제품 현황 관리", "계약서 관리", "기타 문서 관리"], index=[
                            "제품 현황 관리", "계약서 관리", "기타 문서 관리"].index(st.session_state.page))

# 선택된 메뉴를 세션 상태에 저장
st.session_state.page = menu

# 선택된 메뉴에 따라 페이지 표시


def load_page(page_name):
    if page_name == "제품 현황 관리":
        from pages import product_management
        product_management.show_product_management()
    elif page_name == "계약서 관리":
        from pages import contract_management
        contract_management.show_contract_management()
    elif page_name == "기타 문서 관리":
        from pages import other_documents_management
        other_documents_management.show_other_documents_management()


# 페이지 로드
load_page(st.session_state.page)

# 데이터 동기화를 위한 함수


def update_data():
    global df, url_data
    df = data_process.df
    url_data = data_process.url_df
    logging.info("데이터 로드 성공")
    st.experimental_rerun()


# 매일 오전 9시와 오후 4시에 데이터를 동기화하도록 예약
schedule.every().day.at("09:00").do(update_data)
schedule.every().day.at("16:00").do(update_data)

# 백그라운드에서 스케줄러 실행


def run_scheduler():
    while True:
        now = datetime.now()
        if now.weekday() < 5:  # 월요일(0)부터 금요일(4)까지만 실행
            schedule.run_pending()
        time.sleep(1)


# 백그라운드에서 스케줄러 실행
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()
