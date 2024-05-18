import streamlit as st
import data_process

st.set_page_config(layout="wide")

df = data_process.df

# 페이지 상단 영역
st.subheader("PuzzleAI's 사업부 대시보드")

col9, col10 = st.columns([8, 2])
st.subheader("Notion DB를 기준으로 분석한 자료입니다.:sunglasses:")
table_height = 400  # 테이블 높이 (픽셀 단위)
table_width = 2000  # 테이블 너비 (픽셀 단위)

# 페이지당 항목 수 설정
items_per_page = 10

# 데이터 프레임을 페이지별로 나누는 함수
def paginate_data(dataframe, page_number, items_per_page):
    start_index = (page_number - 1) * items_per_page
    end_index = start_index + items_per_page
    return dataframe.iloc[start_index:end_index]

# 탭메뉴 영역
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["VoiceEMR", "VoiceENR", "VoiceSDK", "VoiceMARK", "VoiceDOC"])

# 각 탭의 데이터를 표시하는 함수
def display_tab(dataframe, tab_label, customers, contracts, demos, unknown):
    col1, col2, col3, col4 = st.columns([3, 3, 3, 3])

    # 메트릭 표시
    with col1:
        st.metric(label="고객", value=customers)
    with col2:
        st.metric(label="정식계약", value=contracts)
    with col3:
        st.metric(label="데모계약", value=demos)
    with col4:
        st.metric(label="파악불가", value=unknown)

    # 메트릭 선택을 위한 라디오 버튼 추가
    metric = st.radio(
        f"Select metric for {tab_label}", 
        ('고객', '정식계약', '데모계약', '파악불가'), 
        key=f"metric_{tab_label}"
    )

    # 선택한 메트릭에 따라 데이터 프레임 필터링
    if metric == '고객':
        filtered_df = dataframe
    elif metric == '정식계약':
        filtered_df = dataframe[dataframe['계약관리'] == '정식']
    elif metric == '데모계약':
        filtered_df = dataframe[dataframe['계약관리'] == '데모']
    elif metric == '파악불가':
        filtered_df = dataframe[dataframe['계약관리'].isnull()]

    # 전체 아이템 수와 페이지 수 계산
    total_items = len(filtered_df)
    total_pages = (total_items + items_per_page - 1) // items_per_page

    # 페이지 번호 입력 받기
    page_number = st.number_input(f'Page number for {tab_label}', min_value=1, max_value=total_pages, step=1, value=1, key=f'page_{tab_label}')
    
    # 페이지 데이터 가져오기
    paged_df = paginate_data(filtered_df, page_number, items_per_page)
    paged_df.index += 1

    # 데이터 프레임 표시
    st.dataframe(paged_df, height=table_height, width=table_width)
    st.write(f"Displaying rows {page_number * items_per_page - (items_per_page - 1)} to {min(page_number * items_per_page, total_items)} of {total_items}")





# 각 탭에 데이터프레임 및 페이징 기능 적용
with tab1:
    voiceemr_data = df[df['연관 제품'] == 'VoiceEMR'].reset_index(drop=True)
    voiceemr_data.index.name='구분'
    count_voiceemr = len(voiceemr_data)
    df.index.name = '구분'

    # 계약 관리가 "정식"인 데이터만 카운트
    temp1 = len(voiceemr_data[voiceemr_data['계약관리'] == '정식'])
    # 계약 관리가 "데모"인 데이터만 카운트
    temp2 = len(voiceemr_data[voiceemr_data['계약관리'] == '데모'])
    # 계약 관리가 비어있는 데이터만 카운트
    temp3 = len(voiceemr_data[voiceemr_data['계약관리'].isnull()])

    display_tab(voiceemr_data, "VoiceEMR", count_voiceemr, temp1, temp2,temp3)
with tab2:
    voiceenr_data = df[df['연관 제품'] == 'VoiceENR'].reset_index(drop=True)
    voiceenr_data.index.name='구분'
    count_voiceenr = len(voiceenr_data)

    # 계약 관리가 "정식"인 데이터만 카운트
    temp1 = len(voiceenr_data[voiceenr_data['계약관리'] == '정식'])
    # 계약 관리가 "데모"인 데이터만 카운트
    temp2 = len(voiceenr_data[voiceenr_data['계약관리'] == '데모'])
    # 계약 관리가 비어있는 데이터만 카운트
    temp3 = len(voiceenr_data[voiceenr_data['계약관리'].isnull()])

    display_tab(voiceenr_data, "VoiceENR", count_voiceenr, temp1, temp2,temp3)


with tab3:
    voicesdk_data= df[df['연관 제품'] == 'VoiceSDK'].reset_index(drop=True)
    voicesdk_data.index.name='구분'
    count_voicesdk = len(voicesdk_data)

    # 계약 관리가 "정식"인 데이터만 카운트
    temp1 = len(voicesdk_data[voicesdk_data['계약관리'] == '정식'])
    # 계약 관리가 "데모"인 데이터만 카운트
    temp2 = len(voicesdk_data[voicesdk_data['계약관리'] == '데모'])
    # 계약 관리가 비어있는 데이터만 카운트
    temp3 = len(voicesdk_data[voicesdk_data['계약관리'].isnull()])
    display_tab(voicesdk_data, "VoiceSDK", count_voicesdk, temp1, temp2,temp3)


with tab4:
    voicemark_data= df[df['연관 제품'] == 'VoiceMARK'].reset_index(drop=True)
    voicemark_data.index.name='구분'
    count_voicemark = len(voicemark_data)

    # 계약 관리가 "정식"인 데이터만 카운트
    temp1 = len(voicemark_data[voicemark_data['계약관리'] == '정식'])
    # 계약 관리가 "데모"인 데이터만 카운트
    temp2 = len(voicemark_data[voicemark_data['계약관리'] == '데모'])
    # 계약 관리가 비어있는 데이터만 카운트
    temp3 = len(voicemark_data[voicemark_data['계약관리'].isnull()])
    display_tab(voicemark_data, "VoiceMARK", count_voicemark, temp1, temp2,temp3)


with tab5:
    voicedoc_data= df[df['연관 제품'] == 'VoiceDOC'].reset_index(drop=True)
    voicedoc_data.index.name='구분'
    count_voicedoc = len(voicedoc_data)

    # 계약 관리가 "정식"인 데이터만 카운트
    temp1 = len(voicedoc_data[voicedoc_data['계약관리'] == '정식'])
    # 계약 관리가 "데모"인 데이터만 카운트
    temp2 = len(voicedoc_data[voicedoc_data['계약관리'] == '데모'])
    # 계약 관리가 비어있는 데이터만 카운트
    temp3 = len(voicedoc_data[voicedoc_data['계약관리'].isnull()])
    display_tab(voicedoc_data, "VoiceDOC", count_voicedoc, temp1, temp2,temp3)