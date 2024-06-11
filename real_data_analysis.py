import ready_data
import pandas as pd


#    데이터프레임에서 특정 열의 값이 지정된 문자열을 포함하는 행만 추출합니다.
def filter_data_contains(df_data, page_label):
    """
    Args:
    df_data (pd.DataFrame): 데이터프레임
    page_label (str): 필터링할 페이지 라벨

    Returns:
    pd.DataFrame: 필터링된 데이터프레임
    """
    # tab_name에 따라 데이터프레임 필터링
    if page_label in df_data['제품'].unique():
        df_data = df_data[df_data['제품'] == page_label]
    
    return df_data



# # 대시보드 화면에 표출 할 데이터 분석 자료를 모아 둔 함수
# def DA_data(df_data, page_label):
#     result = extract_by_colum(df_data, "상태", page_label)
#     return result


def main(df,page_label):
    filtered_df = filter_data_contains(df, page_label)  # Notion 데이터 프레임 - tab 메뉴 값*대분류) 정제 한 데이터 프레임


    return 0

