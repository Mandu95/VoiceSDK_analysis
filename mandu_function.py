import pandas as pd
from collections import Counter

# dic 형태의 데이터에서 데이터를 추출 할 때 Nontype 에러가 발생하지 않도록 해주는 함수


def safe_get(d, keys, default=None):
    """안전하게 중첩된 딕셔너리에서 값을 가져오는 헬퍼 함수"""
    for key in keys:
        try:
            d = d[key]
        except (KeyError, TypeError, IndexError):  # dic 데이터 안에 지목 된 keys가 없다면
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


def notion_function(notion_data):

    notion_data = notion_dic_to_dataframe(
        notion_data
    )  # data 변수의 type은 list, list[0]의 type은 딕셔너리. 딕셔너리를 dataframe 형태로 변환
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
    temp = []

    for A in list_data:
        if A not in temp:

            if A is not None:

                temp.append(A)

    return temp


def count_value(list_data):
    counter = Counter(list_data)
    print(counter)
    return counter


def df_col(data):

    temp = list(data[0].keys())
    # temp.insert(0, "구분")
    temp.reverse()
    print(temp)
    return temp

# 제품 현황 관리 DB 데이터를 표로  View 해주기 위한 함수


def extract_data(data, row_name):
    count_data = len(data)

    # 각 데이터를 위한 리스트 초기화
    temp_value = []

    # 비어 있는 df 선언
    empty_df = pd.DataFrame(columns=row_name)

    # 데이터 길이가 1개일 때는 직
    print("입력되어 있는 데이터 총 개수는 : ", count_data)

    for A in range(count_data):
        # print(A, "번째 데이터 이식 시작합니다.")

        row_data = []  # 각 행에 대한 데이터 리스트 초기화

        for B in row_name:
            if B in data[A] and data[A][B] is not None:
                try:
                    if data[A][B]['type'] == "multi_select":
                        temp = len(data[A][B]['multi_select'])
                        if temp > 0:
                            value_list = []
                            for X in range(temp):
                                value_list.append(
                                    safe_get(data[A], [B, 'multi_select', X, 'name']))

                            row_data.append(value_list)

                        else:
                            row_data.append(None)

                    elif data[A][B]['type'] == "rollup":
                        if data[A][B]['rollup']['type'] == "array":
                            
                            temp = len(data[A][B]['rollup']['array'])
                            if temp > 0:
                                value_list = []

                                for Y in range(temp):
                                    value_list.append(safe_get(data[A], [B, 'rollup', 'array', Y, 'select', 'name']))

                                value_list = find_same_data(value_list)
                                row_data.append(value_list)
                                print(value_list)
                            else:
                                row_data.append(None)
                        elif data[A][B]['rollup']['type'] == "number":
                            row_data.append(
                                safe_get(data[A], [B, 'rollup', 'number']))
                        elif data[A][B]['rollup']['type'] == "date":
                            date_str = safe_get(
                                data[A], [B, 'rollup', 'date', 'start'])
                            row_data.append(format_date(date_str))

                    elif data[A][B]['type'] == "last_edited_time":
                        date_str = safe_get(
                            data[A], [B, 'last_edited_time'])
                        row_data.append(format_date(date_str))

                    elif data[A][B]['type'] == "relation":
                        if len(data[A][B]['relation']) > 0:
                            row_data.append(
                                safe_get(data[A], [B, 'relation', 0, 'id']))
                        else:
                            row_data.append(None)

                    elif data[A][B]['type'] == "formula":
                        if data[A][B]['formula']['type'] == "string":
                            row_data.append(
                                safe_get(data[A], [B, 'formula', 'string']))
                        elif data[A][B]['formula']['type'] == "number":
                            row_data.append(
                                safe_get(data[A], [B, 'formula', 'number']))

                    elif data[A][B]['type'] == "status":
                        row_data.append(
                            safe_get(data[A], [B, 'status', 'name']))

                    elif data[A][B]['type'] == "rich_text":
                        row_data.append(
                            safe_get(data[A], [B, 'rich_text', 0, 'text', 'content']))

                    elif data[A][B]['type'] == "email":
                        row_data.append(safe_get(data[A], [B, 'email']))

                    elif data[A][B]['type'] == "select":
                        row_data.append(
                            safe_get(data[A], [B, 'select', 'name']))

                    elif data[A][B]['type'] == "title":
                        if safe_get(data[A][B], ['title', 0, 'type']) == "text":
                            row_data.append(
                                safe_get(data[A], [B, 'title', 0, 'text', 'content']))
                except (KeyError, IndexError, TypeError) as e:
                    print(f"Error accessing {B}: {e}")
                    row_data.append(None)
            else:
                row_data.append(None)  # 데이터가 없는 경우 None 추가

        temp_value.append(row_data)  # 행 데이터를 temp_value에 추가

    return pd.concat([empty_df, pd.DataFrame(temp_value, columns=row_name)], ignore_index=True)


# 제품 현황 관리 DB에서 제품 value 추출하는 함수 [현재 사용 안함]
def extract_goods_item(data):
    goods_fliter = []
    count = len(data)
    for B in range(count):

        try:

            if data[0][B]['연관 제품']['select']['name'] is not None:

                goods_fliter.append(
                    data[0][B]['연관 제품']['select']['name'])

        except Exception as e:
            print("Database를 다시 확인하시오, 데이터가 비어서 그럴거에요!")

    count_goods_value = count_value(goods_fliter)

    goods_fliter = find_same_data(goods_fliter)

    return goods_fliter

# 제품 현황 관리 DB의 [계약구분]속성과 계약관리 DB의 [계약관리] 데이터를 계약관리 DB의 id 기준으로 맞추는 함수


def change_contract_data(data, df):

    for A in range(len(df)):
        temp = df.loc[A, '계약관리']

        if temp is None:
            continue  # temp가 None이면 건너뛰기

        for B in range(len(data)):

            if temp == data['id'][B]:
                new_value = safe_get(
                    data, ['properties', B, '계약구분', 'select', 'name'])
                df.loc[A, '계약관리'] = new_value

    return df
