import streamlit as st
import logging
import login_function as lf
import Ready_notion_DB
import Mandu_component

# 데이터 로딩 및 초기화 함수
def load_and_initialize_data():
    # 세션 상태를 확인하여 데이터가 이미 로드되었는지 확인
    if 'data_initialized' not in st.session_state:
        # 데이터를 최초로 로딩하는 로직
        cop_manage, contract_manage, etc_manage, Task = Ready_notion_DB.main()
        DF_update_one_Week_cop = Ready_notion_DB.main(cop_manage,"내용 업데이트 업체")
        DF_New_cop = Ready_notion_DB.main(cop_manage,"신규 업체")
        Data_all, Data_buy, Data_sell, Data_no_info = Ready_notion_DB.main(contract_manage,"매입/매출 데이터")

        cop_convert_to_contract= Ready_notion_DB.main([contract_manage,etc_manage],"계약전환률")

        # 세션 상태에 로딩된 데이터를 저장
        st.session_state['product_manage'] = cop_manage
        st.session_state['contract_manage'] = contract_manage
        st.session_state['etc_manage'] = etc_manage
        st.session_state['Task'] = Task
        st.session_state['내용 업데이트 업체'] = DF_update_one_Week_cop
        st.session_state['신규 업체'] = DF_New_cop
        st.session_state['매입/매출 전체 데이터'] = Data_all
        st.session_state['매입/매출 매출 데이터'] = Data_buy
        st.session_state['매입/매출 매입 데이터'] = Data_sell
        st.session_state['매입/매출 정보없음 데이터'] = Data_no_info
        st.session_state['계약전환률'] = cop_convert_to_contract
        
        # 데이터 로드 완료 표시
        st.session_state['data_initialized'] = True

def main_content():
    # 데이터 로딩 함수 호출
    load_and_initialize_data()


    Mandu_component.set_initial_page()

    # 로그아웃 버튼 추가
    lf.add_logout_button()

    # 로드된 데이터를 세션 상태에서 가져옴
    cop_df = st.session_state['product_manage']
    DF_update_one_Week_cop = st.session_state['내용 업데이트 업체']
    DF_New_cop = st.session_state['신규 업체']
    cop_convert_to_contract = st.session_state['계약전환률']
    etc_manage = st.session_state['etc_manage'] 

    # 탭 구성 설정
    tab_titles = ["VoiceEMR", "VoiceENR", "VoiceSDK", "VoiceMARK", "VoiceDOC"]
    tabs = st.tabs(tab_titles)

    # 각 탭에 대한 콘텐츠 배치
    with tabs[0]:

        ###### 첫번째 레이어
        cop_df_VoiceEMR = cop_df[cop_df['제품'] == "VoiceEMR"]
        st.session_state.clicked_item = Mandu_component.component_top_button(cop_df_VoiceEMR,"VoiceEMR")

        ###### 두번째 레이어
        DF_update_one_Week_cop_VoiceEMR = DF_update_one_Week_cop[DF_update_one_Week_cop['제품'] == "VoiceEMR"]
        DF_New_cop_VoiceEMR = DF_New_cop[DF_New_cop['제품'] == "VoiceEMR"]
        Mandu_component.second_layer(DF_update_one_Week_cop_VoiceEMR,DF_New_cop_VoiceEMR,"VoiceEMR")

        ###### 세번째 레이어
        cop_convert_to_contract_VoiceEMR = [item for item in cop_convert_to_contract if "VoiceEMR" in item]
        Mandu_component.third_layer(etc_manage,cop_convert_to_contract_VoiceEMR,"VoiceEMR")

    with tabs[1]:
        cop_df_VoiceENR = cop_df[cop_df['제품'] == "VoiceENR"]
        st.session_state.clicked_item = Mandu_component.component_top_button(cop_df_VoiceENR,"VoiceENR")

        DF_update_one_Week_cop_VoiceENR = DF_update_one_Week_cop[DF_update_one_Week_cop['제품'] == "VoiceENR"]
        DF_New_cop_VoiceENR = DF_New_cop[DF_New_cop['제품'] == "VoiceENR"]
        Mandu_component.second_layer(DF_update_one_Week_cop_VoiceENR,DF_New_cop_VoiceENR,"VoiceENR")

    with tabs[2]:
        cop_df_VoiceSDK = cop_df[cop_df['제품'] == "VoiceSDK"]
        st.session_state.clicked_item = Mandu_component.component_top_button(cop_df_VoiceSDK,"VoiceSDK")

        DF_update_one_Week_cop_VoiceSDK = DF_update_one_Week_cop[DF_update_one_Week_cop['제품'] == "VoiceSDK"]

        DF_New_cop_VoiceSDK = DF_New_cop[DF_New_cop['제품'] == "VoiceSDK"]
        Mandu_component.second_layer(DF_update_one_Week_cop_VoiceSDK,DF_New_cop_VoiceSDK,"VoiceSDK")

    with tabs[3]:
        cop_df_VoiceMARK = cop_df[cop_df['제품'] == "VoiceMARK"]
        st.session_state.clicked_item = Mandu_component.component_top_button(cop_df_VoiceMARK,"VoiceMARK")

        DF_update_one_Week_cop_VoiceMARK = DF_update_one_Week_cop[DF_update_one_Week_cop['제품'] == "VoiceMARK"]
        DF_New_cop_VoiceMARK = DF_New_cop[DF_New_cop['제품'] == "VoiceMARK"]
        Mandu_component.second_layer(DF_update_one_Week_cop_VoiceMARK,DF_New_cop_VoiceMARK,"VoiceMARK")

    with tabs[4]:
        st.markdown("제품 개발을 위한 협약 단계에 있습니다. 차후 데이터가 업로드 되면 표시됩니다.")

def main():
    # 페이지 설정
    st.set_page_config(page_title="PuzzleAI's Dashboard", layout="wide")
    
    # 로그 설정
    logging.basicConfig(filename='data_sync.log', level=logging.INFO, format='%(asctime)s - %(message)s')

    # 세션 상태 초기화
    if 'logged_in' not in st.session_state:
        st.session_state.clear()
        st.session_state['logged_in'] = False
        st.session_state['signup'] = False

    # 로그인 상태 확인
    if st.session_state['logged_in']:
        main_content()
    else:
        if st.session_state['signup']:
            lf.signup_screen()
        else:
            lf.login_screen()

if __name__ == "__main__":
    main()
