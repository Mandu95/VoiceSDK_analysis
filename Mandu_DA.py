import pandas as pd
from datetime import datetime
import streamlit_function
import re
from Ready_notion_DB import contract_manage, product_manage


#################################### 이번달 신규 업체 개수 찾기 ####################################
def new_cop_data(df, colum_name=None):

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

        # 조건에 맞는 행의 개수
        count_this_month = len(this_month_df)

        return this_month_df, count_this_month
####################################################################################################


#################################### 매출/매입 계약 테이블 생성#############################################
def View_contract_status(df, tab_name="None"):
    # "페이지URL" 열의 행 값을 데이터프레임 첫번째 열의 행 값의 하이퍼링크로 삽입하고 "페이지URL" 열 삭제
    df = streamlit_function.URL_insert(df)

    temp_df = df

    # "계약시작일" 열의 행 값을 기준으로 내림차순 정렬
    temp_df = temp_df.sort_values(by='계약시작일', ascending=False)
    # 계약서 데이터베이스에서 "제품" 열을 기준으로 1차 필터링하는 코드
    temp_df = temp_df[temp_df['제품'] == tab_name]

    # 매출 데이터만 추출
    temp_df_sell = temp_df[temp_df['매입/매출'].astype(
        str).str.contains("매출")]
    # 매출 데이터만 추출
    temp_df_buy = temp_df[temp_df['매입/매출'].astype(
        str).str.contains("매입")]
    # 매출 데이터만 추출
    temp_df_no_info = temp_df[temp_df['매입/매출'].astype(
        str).str.strip() == ""]

    if tab_name is not None:

        # 내가 페이지에 남기고 싶어하는 데이터베이스의 열의 목록
        columns_order = ['계약명', '계약총액', '제품 현황 관리']
        temp_df = temp_df.reindex(columns=columns_order)
        temp_df_sell = temp_df_sell.reindex(columns=columns_order)
        temp_df_buy = temp_df_buy.reindex(columns=columns_order)
        temp_df_no_info = temp_df_no_info.reindex(
            columns=columns_order)

        # 계약서 View 할 때 보여질 선택박스 항목이랑, 데이터베이스 값 반환
        temp_df = extract_column_unique_value(df, "제품 현황 관리")
        temp_df_sell = extract_column_unique_value(
            temp_df_sell, "제품 현황 관리")
        temp_df_buy = extract_column_unique_value(
            temp_df_buy, "제품 현황 관리")
        temp_df_no_info = extract_column_unique_value(
            temp_df_no_info, "제품 현황 관리")

    return temp_df, temp_df_sell, temp_df_buy, temp_df_no_info

# 데이터프레임의 특정 열의 고유 행 값을 추출하기 위한 함수, 고유 값 추출 된 행은 삭제되도록 설계해둠.


def extract_column_unique_value(df, col_name=None):

    if col_name is not None:

        unique_value = df[col_name].unique()
        df = df.drop(
            columns=[col_name])
        unique_value = unique_value.tolist()
        unique_value.insert(0, '전체')
        unique_value = [re.sub(r'\[.*?\]\s*', '', item)
                        for item in unique_value]

        return df, unique_value
####################################################################################################


def mandu_contract_main(tab_name):
    contract_inital_df = contract_manage

    ####### '계약완료' 상태 클릭 됐을 때 보여 질 테이블과 데이터 #######
    all_contract_df, sell_df, buy_df, no_info_df = View_contract_status(
        contract_inital_df, tab_name)

    return all_contract_df, sell_df, buy_df, no_info_df


def mandu_cop_main(tab_name):

    cop_inital_df = product_manage

    ####### 이번달 신규 업체 개수 찾기 #######
    new_cop_df, new_cop_count = new_cop_data(cop_inital_df, "정보 최신화 날짜")

    return new_cop_df, new_cop_count
