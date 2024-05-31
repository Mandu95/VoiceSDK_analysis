import ready_data
import pandas as pd


# 파싱 완료 된 데이터 프레임 불러오기
def call_data():
    company_df = ready_data.product_manage
    contract_df = ready_data.contract_manage
    etc_df = ready_data.etc_manage
    task_df = ready_data.Task
    return company_df,contract_df,etc_df,task_df


# 데이터프레임 특정 행의 고유 값, 그 고유 값을의 각 개수를 추출하는 함수
def extract_by_colum(df, column_name,page_label):

    if page_label == "VoiceENR" or "VoiceMARK" or "VoiceDOC": 

        temp_values = ['데모요청','사업설명','견적발송','계약중','계약완료']   
        # 특정 열에서 값의 개수를 계산
        value_counts = df[column_name].value_counts()
        
        # 특정 값들의 개수를 추출하여 딕셔너리에 저장
        specific_counts = {value: value_counts.get(value, 0) for value in temp_values}

        return temp_values, specific_counts
    
    elif page_label == "VoiceEMR": 

        temp_values = ['데모요청','사업설명','견적발송','계약완료','데모']   
        # 특정 열에서 값의 개수를 계산
        value_counts = df[column_name].value_counts()
        
        # 특정 값들의 개수를 추출하여 딕셔너리에 저장
        specific_counts = {value: value_counts.get(value, 0) for value in temp_values}

        return temp_values, specific_counts
    
    elif page_label == "VoiceSDK": 

        temp_values = ['최초컨택','자료발송','사업설명','실무자회의','협약','견적발송','계약중','계약완료']   
        # 특정 열에서 값의 개수를 계산
        value_counts = df[column_name].value_counts()
        
        # 특정 값들의 개수를 추출하여 딕셔너리에 저장
        specific_counts = {value: value_counts.get(value, 0) for value in temp_values}

        return temp_values, specific_counts



#    데이터프레임에서 특정 열의 값이 지정된 문자열을 포함하는 행만 추출합니다.
def filter_data_contains(df_data, page_label):
    """
    Args:
    df (pd.DataFrame): 데이터프레임
    column_name = 0 값을 비교할 열 index 넘버
    substring (str): 포함 여부를 확인할 문자열

    Returns:
    pd.DataFrame: 필터링된 데이터프레임
    """


    if page_label == "VoiceEMR":    
        temp = []
        for A in df_data:
            print(A)
            A = A[A.iloc[:, 0].astype(str).str.contains("VoiceEMR", na=False)]
            temp.append(A)

    elif page_label == "VoiceENR":    
        temp = []
        for A in df_data:
            print(A)
            A = A[A.iloc[:, 0].astype(str).str.contains("VoiceENR", na=False)]
            temp.append(A)

    elif page_label == "VoiceMARK":    
        temp = []
        for A in df_data:
            print(A)
            A = A[A.iloc[:, 0].astype(str).str.contains("VoiceMARK", na=False)]
            temp.append(A)


    elif page_label == "VoiceSDK":    
        temp = []
        for A in df_data:
            print(A)
            A = A[A.iloc[:, 0].astype(str).str.contains("VoiceSDK", na=False)]
            temp.append(A)


    elif page_label == "VoiceDOC":    
        temp = []
        for A in df_data:
            print(A)
            A = A[A.iloc[:, 0].astype(str).str.contains("VoiceDOC", na=False)]
            temp.append(A)

    
    df_data = temp
    return df_data


#대시보드 화면에 표출 할 데이터 분석 자료를 모아 둔 함수
def DA_data(df_data, page_label):


    if page_label == "VoiceEMR":    
        result = extract_by_colum(df_data[0],"상태",page_label)

        return result

    elif page_label == "VoiceENR":    
        result = extract_by_colum(df_data[0],"상태",page_label)

        return result

    elif page_label == "VoiceMARK":    
        result = extract_by_colum(df_data[0],"상태",page_label)

        return result


    elif page_label == "VoiceSDK":    
        result = extract_by_colum(df_data[0],"상태",page_label)

        return result

    elif page_label == "VoiceDOC":    
        result = extract_by_colum(df_data[0],"상태",page_label)

        return result

    

def main(page_label):
    notion_df = call_data() # Notion 데이터 프레임 값 호출 (파싱 완료 된 것)
    notion_df = filter_data_contains(notion_df,page_label)  # Notion 데이터 프레임 - tab 메뉴 값*대분류) 정제 한 데이터 프레임

    DA_result = DA_data(notion_df, page_label)
    return notion_df, DA_result






    
