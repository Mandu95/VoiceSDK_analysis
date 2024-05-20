import pandas as pd
from collections import Counter

def notion_dic_to_dataframe(data):  # 딕셔너리 dataframe로 변환하는 함수
    count_data = len(data)
    if count_data < 1:
        print("데이터가 없습니다. 확인 부탁드립니다.")
    else:
        try:
            for A in range(count_data):
                data[A] = pd.DataFrame.from_dict(data=data[A], orient="columns")
        except Exception as e:
            print("dic to dataframe 변환 실패 : ", e)
        return data

# dic 형태의 데이터에서 데이터를 추출 할 때 Nontype 에러가 발생하지 않도록 해주는 함수
def safe_get(d, keys, default=None):
    """안전하게 중첩된 딕셔너리에서 값을 가져오는 헬퍼 함수"""
    for key in keys:
        try:
            d = d[key]
        except (KeyError, TypeError, IndexError):
            return default  # None으로 반환
    return d

# Notion의 날짜 데이터는 ISO 8601 날짜 문자열이기 때문 년/월/일로 변환해주는 함수
def format_date(date_str):
    """ISO 8601 날짜 문자열을 년/월/일 형식으로 변환하는 함수"""
    if date_str:
        try:
            return pd.to_datetime(date_str).strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            return None
    return None

def notion_function(notion_data):
    """Notion 데이터 처리 함수"""
    notion_data = notion_dic_to_dataframe(notion_data)
    count_data = len(notion_data)
    if count_data < 1:
        print("데이터가 없습니다. 확인 부탁드립니다.")
    else:
        try:
            for A in range(count_data):
                notion_data[A] = notion_data[A]["properties"]
        except Exception as e:
            print("[properties] 속성 추출 실패 : ", e)
    print(len(notion_data))
    return notion_data

def find_same_data(list_data):
    """리스트에서 중복되지 않은 데이터 추출 함수"""
    temp = []
    for A in list_data:
        if A not in temp and A is not None:
            temp.append(A)
    return temp

def count_value(list_data):
    """리스트 데이터 카운트 함수"""
    counter = Counter(list_data)
    print(counter)
    return counter

def df_col(data):
    """데이터프레임 컬럼 추출 함수"""
    temp = list(data[0].keys())
    temp.reverse()
    print(temp)
    return temp

def extract_data(data, row_name):
    """제품 현황 관리 DB 데이터를 표로 View 해주기 위한 함수"""
    count_data = len(data)
    temp_value = []
    empty_df = pd.DataFrame(columns=row_name)
    print("입력되어 있는 데이터 총 개수는 : ", count_data)

    for A in range(count_data):
        row_data = []
        for B in row_name:
            if B in data[A] and data[A][B] is not None:
                try:
                    row_data.append(get_value_from_property(data[A][B]))
                except (KeyError, IndexError, TypeError) as e:
                    print(f"Error accessing {B}: {e}")
                    row_data.append(None)
            else:
                row_data.append(None)  # 데이터가 없는 경우 None 추가
        temp_value.append(row_data)  # 행 데이터를 temp_value에 추가

    return pd.concat([empty_df, pd.DataFrame(temp_value, columns=row_name)], ignore_index=True)

def get_value_from_property(property):
    """개별 속성에서 값을 추출하는 헬퍼 함수"""
    if property['type'] == "multi_select":
        return [safe_get(property, ['multi_select', X, 'name']) for X in range(len(property['multi_select']))] or None
    elif property['type'] == "rollup":
        return get_rollup_value(property)
    elif property['type'] == "last_edited_time":
        return format_date(safe_get(property, ['last_edited_time']))
    elif property['type'] == "relation":
        return safe_get(property, ['relation', 0, 'id']) if property['relation'] else None
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
    elif property['type'] == "title":
        return safe_get(property, ['title', 0, 'text', 'content']) if safe_get(property, ['title', 0, 'type']) == "text" else None

def get_rollup_value(property):
    """Rollup 속성에서 값을 추출하는 함수"""
    if property['rollup']['type'] == "array":
        value_list = [safe_get(property, ['rollup', 'array', Y, 'select', 'name']) for Y in range(len(property['rollup']['array']))]
        return find_same_data(value_list) or None
    elif property['rollup']['type'] == "number":
        return safe_get(property, ['rollup', 'number'])
    elif property['rollup']['type'] == "date":
        return format_date(safe_get(property, ['rollup', 'date', 'start']))

# 제품 현황 관리 DB에서 제품 value 추출하는 함수 [현재 사용 안함]
def extract_goods_item(data):
    """제품 현황 관리 DB에서 제품 value 추출하는 함수"""
    goods_fliter = []
    count = len(data)
    for B in range(count):
        try:
            if data[0][B]['연관 제품']['select']['name'] is not None:
                goods_fliter.append(data[0][B]['연관 제품']['select']['name'])
        except Exception as e:
            print("Database를 다시 확인하시오, 데이터가 비어서 그럴거에요!")

    count_goods_value = count_value(goods_fliter)
    goods_fliter = find_same_data(goods_fliter)
    return goods_fliter

# 제품 현황 관리 DB의 [계약구분]속성과 계약관리 DB의 [계약관리] 데이터를 계약관리 DB의 id 기준으로 맞추는 함수
def change_contract_data(data, df):
    """제품 현황 관리 DB의 [계약구분]속성과 계약관리 DB의 [계약관리] 데이터를 계약관리 DB의 id 기준으로 맞추는 함수"""

    for A in range(len(df)):
        temp = df.loc[A, '계약관리']
        if temp is None:
            continue  # temp가 None이면 건너뛰기
        for B in range(len(data)):
            if temp == data['id'][B]:
                new_value = safe_get(data, ['properties', B, '계약구분', 'select', 'name'])
                df.loc[A, '계약관리'] = new_value
    return df


# 기타서류 DB의 [발송 대상]속성과 제품 현황 관리 DB의 [업체 이름] 데이터를 제품 현황 관리 DB의 id 기준으로 맞추는 함수
def change_company_name_data(data, df):
    for A in range(len(df)):
        temp = df.loc[A, '발송 대상']
        if temp is None:
            continue  # temp가 None이면 건너뛰기
        for B in range(len(data)):
            if temp == data['id'][B]:
                new_value = safe_get(data, ['properties', B, '업체 이름', 'select', 'name'])
                df.loc[A, '발송 대상'] = new_value
    return df
