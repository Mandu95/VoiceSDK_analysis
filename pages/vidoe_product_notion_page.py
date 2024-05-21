import streamlit as st


def show_embedded_page(url, width=1200, height=800):
    """
    주어진 URL을 iframe으로 임베드하여 표시하는 함수.
    :param url: 표시할 웹 페이지의 URL
    :param width: iframe의 너비 (기본값: 1200)
    :param height: iframe의 높이 (기본값: 800)
    """
    iframe_html = f'<iframe src="{url}" width="{width}" height="{height}"></iframe>'
    st.markdown(iframe_html, unsafe_allow_html=True)


# 페이지 설정
st.set_page_config(page_title="임베디드 페이지", layout="wide")

# 제목 표시
st.title("임베디드 페이지 예제")
st.write("아래에 임베디드 페이지가 표시됩니다.")

# 임베디드 페이지 표시
show_embedded_page(
    "https://puszleai-my.sharepoint.com/:f:/g/personal/mandu95_puzzle-ai_com/EuMpFSiPx5hNjrQL2TXyIYwBX4300ryjo3abEzYr7dS0mw?e=JbmCuy", width=1200, height=800)

# 실행 예제
if __name__ == "__main__":
    show_embedded_page()
