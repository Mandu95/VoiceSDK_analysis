import pandas as pd
from datetime import datetime, timedelta

# from Ready_notion_DB import contract_manage, product_manage


#################################### 이번달 신규 업체 개수 찾기 ####################################
def new_cop_data(df, colum_name=None):   ## 1달 단위 신규 업체 (생성 일시 - 당해 년/당월 기준으로 추출)

    # 현재 날짜
    current_date = datetime.now()

    if colum_name is None:
        temp = 0
        return df, temp

    else:
        df[colum_name] = pd.to_datetime(df[colum_name])
        # 이번 달 데이터 필터링
        this_month_df = df[(df[colum_name].dt.year == current_date.year) &
                           (df[colum_name].dt.month == current_date.month)]



        return this_month_df

def update_one_week_cop(df):  ## 최근 1주 간 정보 업데이트 된 업체
    now = datetime.now().date()
    if '정보 최신화 날짜' in df.columns:
        update_one_week_df = df[pd.to_datetime(
            df['정보 최신화 날짜']).dt.date >= now - timedelta(days=7)]
    else:
        update_one_week_df = pd.DataFrame(columns=df.columns)  # 빈 데이터프레임 반환
    return update_one_week_df




#################################### 매출/매입 계약 테이블 생성 #############################################
def View_contract_status(df):

    temp_df = df

    # 매출 데이터만 추출
    temp_df_sell = temp_df[temp_df['매입/매출'].astype(
        str).str.contains("매출")]
    # 매입 데이터만 추출
    temp_df_buy = temp_df[temp_df['매입/매출'].astype(
        str).str.contains("매입")]
    # 해당없음 데이터만 추출
    temp_df_no_info = temp_df[temp_df['매입/매출'].astype(
        str).str.strip() == ""]



    # 내가 페이지에 남기고 싶어하는 데이터베이스의 열의 목록
    columns_order = ['계약명', '계약총액', '제품 현황 관리','페이지URL','제품']
    temp_df = temp_df.reindex(columns=columns_order)
    temp_df_sell = temp_df_sell.reindex(columns=columns_order)
    temp_df_buy = temp_df_buy.reindex(columns=columns_order)
    temp_df_no_info = temp_df_no_info.reindex(
            columns=columns_order)


    return temp_df, temp_df_sell, temp_df_buy, temp_df_no_info









# ####################### 데이터 분석 main (streamlit_function에서 호출하는 부분) #######################
# def mandu_contract_main(tab_name):
#     contract_inital_df = contract_manage

#     # '제품' 열의 리스트를 문자열로 변환
#     contract_inital_df['제품'] = contract_inital_df['제품'].apply(lambda x: ', '.join(x))

#     ####### 계약서 데이터베이스에서 "제품" 열을 기준으로 1차 필터링하는 코드
#     contract_inital_df = contract_inital_df[contract_inital_df['제품'] == tab_name]

#     ####### "계약시작일" 열의 행 값을 기준으로 내림차순 정렬
#     contract_inital_df = contract_inital_df.sort_values(by='계약시작일', ascending=False)

#     ####### '계약완료' 상태 클릭 됐을 때 보여 질 테이블과 데이터
#     all_contract_df, sell_df, buy_df, no_info_df = View_contract_status(
#         contract_inital_df, tab_name)
#     print(len(all_contract_df[0]))
#     print(len(sell_df[0]))
#     print(len(buy_df[0]))
#     print(len(no_info_df[0]))
#     return all_contract_df, sell_df, buy_df, no_info_df

# def mandu_cop_main(tab_name):
#     cop_inital_df = product_manage
#     ####### 계약서 데이터베이스에서 "제품" 열을 기준으로 1차 필터링하는 코드
#     cop_inital_df = cop_inital_df[cop_inital_df['제품'] == tab_name]
#     ####### "계약시작일" 열의 행 값을 기준으로 내림차순 정렬
#     cop_inital_df = cop_inital_df.sort_values(by='계약시작일', ascending=False)
#     # '제품' 열의 리스트를 문자열로 변환
#     cop_inital_df['개발언어'] = cop_inital_df['개발언어'].apply(lambda x: ', '.join(x))
    
    
#     ###### 이번달 신규 업체 개수 찾기
#     new_cop_df = new_cop_data(cop_inital_df, "정보 최신화 날짜") 

#     ###### 2주 내 업데이트 이력 있는 기업 찾기
#     update_one_week_df = update_one_week_cop(cop_inital_df)

#     columns_order = ['업체 이름', '개발언어', '상태','페이지URL']
#     new_cop_df= new_cop_df.reindex(columns=columns_order)
#     return new_cop_df, update_one_week_df


# mandu_contract_main("VoiceENR")
