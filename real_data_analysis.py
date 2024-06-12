import pandas as pd
import streamlit_function


def contract_data_analysis(contract_manage, tab_name):

    # "페이지URL" 열의 행 값을 데이터프레임 첫번째 열의 행 값의 하이퍼링크로 삽입하고 "페이지URL" 열 삭제
    contract_manage = streamlit_function.URL_insert(contract_manage)

    # "계약명" 열의 행 값을 기준으로 내림차순 정렬
    contract_manage = contract_manage .sort_values(by='계약명', ascending=False)

    # 계약서 데이터베이스에서 "제품" 열을 기준으로 1차 필터링하는 코드
    contract_manage = contract_manage[contract_manage['제품'].astype(
        str).str.contains(tab_name)]

    # "계약명" 열의 행 값을 기준으로 내림차순 정렬
    contract_manage = contract_manage .sort_values(by='계약명', ascending=False)

    # 계약서 데이터베이스에서 "매입/매출" 열의 행 값을 기준으로 매입/매출/정보없음 구분하는 코드
    # 매출 데이터만 추출
    contract_manage_sell = contract_manage[contract_manage['매입/매출'].astype(
        str).str.contains("매출")]
    # 매출 데이터만 추출
    contract_manage_buy = contract_manage[contract_manage['매입/매출'].astype(
        str).str.contains("매입")]
    # 매출 데이터만 추출
    contract_manage_noinfo = contract_manage[contract_manage['매입/매출'].astype(
        str).str.strip() == ""]

    # 내가 페이지에 남기고 싶어하는 데이터베이스의 열의 목록
    columns_order = ['계약명', '계약총액', '제품 현황 관리']
    contract_manage = contract_manage.reindex(columns=columns_order)
    contract_manage_sell = contract_manage_sell.reindex(columns=columns_order)
    contract_manage_buy = contract_manage_buy.reindex(columns=columns_order)
    contract_manage_noinfo = contract_manage_noinfo.reindex(
        columns=columns_order)

    # 계약서 View 할 때 보여질 선택박스 항목이랑, 데이터베이스 값 반환
    contract_manage = extract_column_unique_value(contract_manage, "제품 현황 관리")
    contract_manage_sell = extract_column_unique_value(
        contract_manage_sell, "제품 현황 관리")
    contract_manage_buy = extract_column_unique_value(
        contract_manage_buy, "제품 현황 관리")
    contract_manage_noinfo = extract_column_unique_value(
        contract_manage_noinfo, "제품 현황 관리")

    return contract_manage, contract_manage_sell, contract_manage_buy, contract_manage_noinfo


# 데이터프레임의 특정 열의 고유 행 값을 추출하기 위한 함수, 고유 값 추출 된 행은 삭제되도록 설계해둠.
def extract_column_unique_value(df, col_name):

    unique_value = df[col_name].unique()
    df = df.drop(
        columns=[col_name])
    unique_value = unique_value.tolist()
    unique_value.insert(0, '전체')

    unique_value = extract_text_data(unique_value)
    return df, unique_value


# 리스트의 값들에서 특정 텍스트를 제거하는 함수
def extract_text_data(list_data):
    import re
    # '제품' 열에서 대괄호 안의 텍스트를 제거하고 이름만 추출
    return [re.sub(r'\[.*?\]\s*', '', item) for item in list_data]


def contract_data_main(tab_name):
    from ready_data import contract_manage

    contract_manage, contract_manage_sell, contract_manage_buy, contract_manage_noinfo = contract_data_analysis(
        contract_manage, tab_name)

    return contract_manage, contract_manage_sell, contract_manage_buy, contract_manage_noinfo


############################### streamlit_function 파일에서 직접 호출하는 함수 ###############################

def calculate_total_amount(df, col_name):
    """
    데이터프레임에서 특정 열의 금액 단위 데이터를 정수형으로 변환하여 전체 합계를 구하는 함수

    Args:
    df (pd.DataFrame): 입력 데이터프레임
    col_name (str): 금액 단위 데이터를 포함하는 열의 이름

    Returns:
    str: 금액 단위로 환산된 전체 금액의 합계
    """
    # 금액 데이터를 정수형으로 변환하여 임시 변수에 저장
    temp_values = df[col_name].replace(
        {',': '', '원': ''}, regex=True).astype(int)

    # 전체 합계 계산
    total_amount = temp_values.sum()

    # 금액 단위로 환산
    formatted_amount = f"{total_amount:,}원"

    return formatted_amount
