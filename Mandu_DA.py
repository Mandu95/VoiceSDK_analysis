import pandas as pd
from datetime import datetime, timedelta
from pandas.tseries.offsets import DateOffset


#################################### 이번달 신규 업체 개수 찾기 ####################################
def new_cop_data(df, colum_name=None):  # 1달 단위 신규 업체 (생성 일시 - 당해 년/당월 기준으로 추출)

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


#################################### 최근 1주 간 정보 업데이트 된 업체 ####################################
def update_one_week_cop(df):
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
    columns_order = ['계약명', '계약총액', '제품 현황 관리', '페이지URL', '제품']
    temp_df = temp_df.reindex(columns=columns_order)
    temp_df_sell = temp_df_sell.reindex(columns=columns_order)
    temp_df_buy = temp_df_buy.reindex(columns=columns_order)
    temp_df_no_info = temp_df_no_info.reindex(
        columns=columns_order)

    return temp_df, temp_df_sell, temp_df_buy, temp_df_no_info

#################################### 데모 to 계약 전환률 #############################################


def DA_cop_convert_to_contract(df):

    contract_df_Demo = df[df['계약구분'] == "데모"]
    contract_df_Demo_values = contract_df_Demo['제품 현황 관리'].unique()

    contract_df_NoDemo = df[df['계약구분'] == "정식"]

    # contract_df_NoDemo에서 '제품 현황 관리' 값이 contract_df_Demo_values와 일치하는 행만 추출
    demo_to_contract_df = contract_df_NoDemo[contract_df_NoDemo['제품 현황 관리'].isin(
        contract_df_Demo_values)]

    return contract_df_Demo, demo_to_contract_df


#################################### 월별/분기별 매출액 #############################################
def moeny_sum_month(df):
    # 산출 근거 : 계약시작일이 당월인 데이터들의 계약 총액의 합계
    # '계약시작일' 열을 날짜 형식으로 변환
    df['계약시작일'] = pd.to_datetime(df['계약시작일'])
    # '계약총액' 열에서 '원'과 쉼표를 제거
    df['계약총액'] = df['계약총액'].replace('[원,]', '', regex=True)

    # 빈 문자열을 NaN으로 변환 후 NaN을 0으로 대체
    df['계약총액'] = pd.to_numeric(
        df['계약총액'], errors='coerce').fillna(0).astype(int)
    # 현재 날짜 정보 가져오기
    current_date = datetime.now()

    # 최근 3개월 데이터 필터링
    three_months_ago = current_date - DateOffset(months=3)
    df_last_3_months = df[df['계약시작일'] >= three_months_ago]
    # total_last_3_months_money_amount = df_last_3_months['계약총액'].sum()
    # 최근 6개월 데이터 필터링
    six_months_ago = current_date - DateOffset(months=6)
    df_last_6_months = df[df['계약시작일'] >= six_months_ago]

    # 이번 달 데이터만 필터링
    this_month_df = df[(df['계약시작일'].dt.year == current_date.year) &
                       (df['계약시작일'].dt.month == current_date.month)]

    return this_month_df, df_last_3_months, df_last_6_months


def moeny_quater(df):
    # 산출 근거 : 계약시작일이 당월인 데이터들의 계약 총액의 합계
    # '계약총액' 열에서 '원'과 쉼표를 제거
    df['계약총액'] = df['계약총액'].replace('[원,]', '', regex=True)
    # 빈 문자열을 NaN으로 변환 후 NaN을 0으로 대체
    df['계약총액'] = pd.to_numeric(
        df['계약총액'], errors='coerce').fillna(0).astype(int)
    df['계약시작일'] = pd.to_datetime(df['계약시작일'])

    # 분기 계산
    df['분기'] = df['계약시작일'].dt.to_period('Q')

    # 각 분기별 데이터프레임을 변수에 할당
    quarter_1_df = df[df['분기'] == '2024Q1']
    quarter_2_df = df[df['분기'] == '2024Q2']
    quarter_3_df = df[df['분기'] == '2024Q3']
    quarter_4_df = df[df['분기'] == '2024Q4']

    return quarter_1_df, quarter_2_df, quarter_3_df, quarter_4_df
