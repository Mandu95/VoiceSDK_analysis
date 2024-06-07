import streamlit as st
import yaml
import os
import hashlib

# 사용자 데이터를 저장할 파일 경로
USER_DATA_FILE = 'user_data.yaml'

# 사용자 데이터를 로드하거나 파일이 없으면 초기화


def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            return yaml.safe_load(file)
    else:
        return {"users": {}}

# 사용자 데이터를 저장


def save_user_data(user_data):
    with open(USER_DATA_FILE, 'w') as file:
        yaml.dump(user_data, file)

# 비밀번호를 해싱하는 함수


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 로그인 화면 표시


def login_screen():
    st.title("Login")

    login_form = st.form("login_form")
    email = login_form.text_input("Email")
    password = login_form.text_input("Password", type="password")
    login_button = login_form.form_submit_button("Login")

    if login_button:
        user_data = load_user_data()
        hashed_password = hash_password(password)

        if email in user_data["users"] and user_data["users"][email]["password"] == hashed_password:
            st.session_state["logged_in"] = True
            st.session_state["email"] = email
            st.experimental_rerun()
        else:
            st.error("Invalid email or password")

    st.button("Sign Up", on_click=lambda: st.session_state.update(
        {"signup": True}))

# 회원가입 화면 표시


def signup_screen():
    st.title("Sign Up")

    signup_form = st.form("signup_form")
    email = signup_form.text_input("Email")
    username = signup_form.text_input("Username")
    password = signup_form.text_input("Password", type="password")
    signup_button = signup_form.form_submit_button("Sign Up")

    if signup_button:
        if "@puzzle-ai.com" not in email:
            st.error("Email must contain @puzzle-ai.com")
        else:
            user_data = load_user_data()
            if email in user_data["users"]:
                st.error("Email already exists")
            else:
                user_data["users"][email] = {
                    "username": username,
                    "password": hash_password(password)
                }
                save_user_data(user_data)
                st.success("Sign up successful! Please log in.")
                st.session_state["signup"] = False
                st.experimental_rerun()

    st.button("Back to Login",
              on_click=lambda: st.session_state.update({"signup": False}))

# 로그아웃 버튼 추가


def add_logout_button():
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["signup"] = False
        st.session_state["email"] = ""
        st.experimental_rerun()
