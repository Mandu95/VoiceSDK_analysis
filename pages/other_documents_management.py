import streamlit as st
from Data_anal import etc_manage  # 데이터프레임을 data_process 모듈에서 불러옴
import streamlit_function as sf  # streamlit_function 모듈 임포트


def show_other_documents_management():
    st.subheader("기타 문서 관리")
    st.write("업체로 발송 된 견적서, MOU 및 NDA 체결 문서를 볼 수 있습니다:sunglasses:")

    col1, col2 = st.columns([8, 2])

    with col1:
        search_query = st.text_input(
            "",
            value=st.session_state.get('search_query', ''),
            placeholder="문서와 관련 된 업체 또는 병원 이름을 검색해주세요.",
            key='search_input'
        )
        st.session_state['search_query'] = search_query

    with col2:
        # 탭 메뉴를 selectbox로 대체
        tab_label = st.selectbox(
            "문서 구분",
            ["전체", "VoiceEMR", "VoiceENR", "VoiceSDK", "VoiceMARK", "VoiceDOC"],
            key='select_tab'
        )

    # 탭 메뉴와 검색어에 따른 데이터 필터링
    if tab_label == "전체":
        filtered_data = etc_manage
    else:
        filtered_data = etc_manage[etc_manage['문서이름'].str.contains(
            tab_label, case=False, na=False)]

    if search_query:
        filtered_data = filtered_data[filtered_data['문서이름'].str.contains(
            search_query, case=False, na=False)]

    filtered_data = filtered_data.reset_index(drop=True)
    filtered_data.index = filtered_data.index + 1
    filtered_data.index.name = 'No'

    if filtered_data.empty:
        st.markdown(
            """
            <div class="no-data">데이터가 없습니다</div>
            """, unsafe_allow_html=True)
    else:
        items_per_page = 10
        sf.display_html_table_for_other_docs(
            filtered_data, tab_label, items_per_page)


# 호출 예제
if __name__ == "__main__":
    show_other_documents_management()
