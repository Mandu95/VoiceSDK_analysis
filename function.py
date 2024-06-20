import pandas as pd
import numpy as np
from datetime import datetime
# notion data를 row_name, Properites, URL 추출해서 저장

################################### notion_DB_call.py에서 참조하는 함수 ##################################


def notion_dic_to_dataframe(data):  # 딕셔너리 dataframe로 변환하는 함수
    count_data = len(data)
    if count_data < 1:
        print("데이터가 없습니다. 확인 부탁드립니다.")
    else:
        try:
            for A in range(count_data):
                data[A] = pd.DataFrame.from_dict(
                    data=data[A], orient="columns")
        except Exception as e:
            print("dic to dataframe 변환 실패 : ", e)
        return data
#########################################################################################################


################################### properties속성으로 데이터프레임 만듦 ##################################
def make_dataframe(data):
    temp_value = []

    # row_name (data[0]) 활용해서 빈 데이터 프레임 생성
    empty_df = pd.DataFrame(columns=data[0])

    for A in range(len(data[1])):
        row_data = []
        for B in data[0]:
            if B in data[1][A] and data[1][A][B] is not None:
                try:
                    row_data.append(get_value_from_property(data[1][A][B]))
                except (KeyError, IndexError, TypeError) as e:
                    print(f"Error accessing {B}: {e}")
                    row_data.append(None)
            else:
                row_data.append(None)  # 데이터가 없는 경우 None 추가
        temp_value.append(row_data)  # 행 데이터를 temp_value에 추가

    # 기존 데이터프레임 생성
    df = pd.concat([empty_df, pd.DataFrame(
        temp_value, columns=data[0])], ignore_index=True)

    # "페이지URL" 열 추가
    df["페이지URL"] = None

    # URL 값을 data[2]에서 가져와서 "페이지URL" 열에 추가
    for i in range(len(data[2])):
        df.at[i, "페이지URL"] = data[2][i]

    return replace_none_with_empty(df)

# none이나 NaN 모두 제거하는 함수


def replace_none_with_empty(df):
    """데이터프레임에서 None 또는 NaN을 빈 문자열로 교체하는 함수"""
    # 모든 NaN 또는 None을 빈 문자열로 교체
    df = df.fillna('')
    return df

#########################################################################################################


################ Notion 호출 한 데이터베이스 데이터 중 properties 속성 데이터만 추출하는 함수 ###############
def extract_properties_to_array(data):

    # 빈 이중배열 선언
    empty_array = [[] for _ in range(4)]

    for idx, notion_data in enumerate(data):
        # notion 데이터 [properties]만 추출
        temp_data = notion_data['properties']

        # notion 데이터 [url]만 추출
        temp_url = notion_data['url']

        # row_name 추출 및 순서 반대로
        row_name = list(temp_data[0].keys())
        row_name.reverse()

        # 빈 이중배열에 row_name과 temp 값 순서대로 추가 0 : row_name, 1 : properties 값, 2: notion 페이지 url 값
        empty_array[idx].append(row_name)
        empty_array[idx].append(temp_data)
        empty_array[idx].append(temp_url)

    return empty_array
#########################################################################################################


########################## notion 데이터 파싱하는 함수 (make dataframe 함수에서 참조) ##########################
# 파싱할 때 에러 발생 시 예외처리하고 파싱 이어가는 함수
def safe_get(d, keys, default=None):
    """안전하게 중첩된 딕셔너리에서 값을 가져오는 헬퍼 함수"""
    for key in keys:
        try:
            d = d[key]
        except (KeyError, TypeError, IndexError):
            return default  # None으로 반환
    return d
# 파싱하는 함수


def get_value_from_property(property):
    """개별 속성에서 값을 추출하는 헬퍼 함수"""
    if property['type'] == "multi_select":
        return [safe_get(property, ['multi_select', X, 'name']) for X in range(len(property['multi_select']))] or None
    elif property['type'] == "rollup":
        return get_rollup_value(property)
    elif property['type'] == "last_edited_time":
        return safe_get(property, ['last_edited_time'])
    elif property['type'] == "relation":
        return [safe_get(relation, ['id']) for relation in property['relation']] if property['relation'] else None
    elif property['type'] == "formula":
        return safe_get(property, ['formula', 'string']) if property['formula']['type'] == "string" else safe_get(property, ['formula', 'number'])
    elif property['type'] == "status":
        return safe_get(property, ['status', 'name'])
    elif property['type'] == "rich_text":
        return safe_get(property, ['rich_text', 0, 'text', 'content'])
    elif property['type'] == "email":
        return safe_get(property, ['email'])
    elif property['type'] == "select":
        return safe_get(property, ['select', 'name'])
    elif property['type'] == "date":
        return safe_get(property, ['date', 'start'])
    elif property['type'] == "number":
        return safe_get(property, ['number'])
    elif property['type'] == "url":
        return safe_get(property, ['url'])
    elif property['type'] == "created_time":
        return safe_get(property, ['created_time'])
    elif property['type'] == "title":
        return safe_get(property, ['title', 0, 'text', 'content']) if safe_get(property, ['title', 0, 'type']) == "text" else None
# notion properties 중 롤업 속성에 대한 별도 함수


def get_rollup_value(property):
    """Rollup 속성에서 값을 추출하는 함수"""
    if property['rollup']['type'] == "array":
        value_list = [safe_get(property, ['rollup', 'array', Y, 'select', 'name'])
                      for Y in range(len(property['rollup']['array']))]
        return find_same_data(value_list) or None
    elif property['rollup']['type'] == "number":
        return safe_get(property, ['rollup', 'number'])
    elif property['rollup']['type'] == "date":
        return format_date(safe_get(property, ['rollup', 'date', 'start']))
# ISO 8601 날짜 변환해주는 함수 (같은 역할 함수가 하나 더 있지만, 날짜 관련 notion properties 이름이 여러 개라 일단 살림)


def format_date(date_str):
    """ISO 8601 날짜 문자열을 년/월/일 형식으로 변환하는 함수"""
    if date_str:
        try:
            return pd.to_datetime(date_str).strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            return None
    return None
# 중복데이터 제거 함수


def find_same_data(list_data):
    """리스트에서 중복되지 않은 데이터 추출 함수"""
    temp = []
    for A in list_data:
        if A not in temp and A is not None:
            temp.append(A)
    return temp
##############################################################################################################


######################################## 관계형 데이터 (id)를 텍스트로 변환하는 함수 ############################
def change_relation_data(dataframe, origin_dataframe, row_name1, row_name2):
    for A in range(len(dataframe)):
        temp = dataframe.loc[A, row_name1]

        if temp is None:
            continue  # temp가 None이면 건너뛰기

        new_values = []
        if isinstance(temp, list):
            for t in temp:
                for B in range(len(origin_dataframe)):
                    if t == origin_dataframe['id'][B]:
                        new_value = new_value = origin_dataframe['properties'][
                            B][row_name2]['title'][0]['plain_text']
                        new_values.append(new_value)
            # 쉼표로 구분된 문자열로 변환하여 할당
            dataframe.loc[A, row_name1] = ', '.join(new_values)
        else:
            for B in range(len(origin_dataframe)):
                if temp == origin_dataframe['id'][B]:
                    new_value = origin_dataframe['properties'][B][row_name2]['title'][0]['plain_text']
                    dataframe.loc[A, row_name1] = new_value

    return dataframe
##############################################################################################################


#################### 데이터 형태 변환 함수가 참조하는 함수, 실질적으로 데이터 형태가 바뀌는 시점 ###################
def convert_currency_format(df, columns):
    """지정된 열을 금액 형식으로 변환하는 함수."""
    for col in columns:
        if col in df.columns:
            # 값이 비어있거나 NaN인 경우를 제외하고 금액 형식으로 변환
            df[col] = df[col].apply(
                lambda x: f"{int(x):,}원" if pd.notnull(x) and is_number(x) else x)
    return df
# 금액 숫자 텍스트로 변환하는 함수


def convert_number_text_format(df, columns):
    """지정된 열을 숫자 텍스트 형식으로 변환하는 함수."""
    for col in columns:
        if col in df.columns:
            # 값이 비어있거나 NaN인 경우를 제외하고 숫자 텍스트 형식으로 변환
            df[col] = df[col].apply(
                lambda x: f"{int(x)}" if pd.notnull(x) and is_number(x) else x)
    return df
# iso8601 표현 방식이 맞는지 확인하는 코드


def convert_is_iso8601(date_str):
    try:
        # 'Z'를 '+00:00'로 변환하여 UTC 시간을 올바르게 처리
        datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False
# 숫자인지 확인하는 코드


def is_number(s):
    """입력이 숫자인지 확인하는 함수."""
    try:
        float(s)
        return True
    except ValueError:
        return False
##############################################################################################################


############################## 데이터 형태 변환, 금액 단위/일반 int 숫자/일반 날짜 ##############################

def Change_data_type(df):
    # 금액 단위로 변환되는 열 목록
    currency_columns = ["계약단가", "라이선스 총액", "계약총액"]
    # 숫자 텍스트로 변환되는 열 목록
    number_columns = ["라이선스 수", "계약잔여일"]

    df = convert_currency_format(df, currency_columns)
    df = convert_number_text_format(df, number_columns)
    # NaN 또는 None 값을 빈 문자열로 대체
    df = df.fillna('')

    return df


def Change_date_iso8601(df, column_names):
    """지정된 열에서 ISO 8601 형식의 날짜와 시간 문자열을 파싱하여 날짜 부분만 추출."""
    if column_names is None:
        return df

    if isinstance(column_names, str):
        column_names = [column_names]  # 단일 열 이름을 리스트로 변환

    for col in column_names:
        if col in df.columns:
            # 새 열을 생성, ISO 8601 형식이 맞다면 날짜만 추출, 아니면 원본 데이터 유지
            df[col] = df[col].apply(
                lambda x: datetime.fromisoformat(
                    x.replace('Z', '+00:00')).date()
                if not pd.isna(x) and convert_is_iso8601(x) else x
            )
    return df

##############################################################################################################
