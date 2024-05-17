import pandas as pd
from collections import Counter


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


def extract_data(data, row_name):
    count_data = len(data)
    temp_value = []  # 각 데이터를 위한 리스트 초기화
    empty_df = pd.DataFrame(columns=row_name)
    print(empty_df)

    def safe_get(d, keys, default=None):
        """안전하게 중첩된 딕셔너리에서 값을 가져오는 헬퍼 함수"""
        for key in keys:
            try:
                d = d[key]
            except (KeyError, TypeError, IndexError):
                return default
        return d

    if count_data <= 1:
        print("데이터베이스에 입력 된 값이 한 줄 밖에 없습니다.")
        empty_df.loc[0] = [
            safe_get(data, ['납품병원', 'multi_select', 0, 'name']),
            safe_get(data, ['계약구분', 'rollup', 'array', 0, 'select']),
            safe_get(data, ['상태', 'status', 'name']),
            safe_get(data, ['정보 최신화 날짜', 'last_edited_time']),
            safe_get(data, ['라이선스 수', 'rollup', 'number']),
            safe_get(data, ['계약시작일', 'rollup', 'date', 'start']),
            safe_get(data, ['계약관리', 'relation', 0, 'id']),
            safe_get(data, ['계약잔여일', 'formula', 'string']),
            safe_get(data, ['개발언어', 'multi_select', 0, 'name']),
            safe_get(data, ['계약 횟수', 'rollup', 'number']),
            safe_get(data, ['컨택 업체 담당자', 'rich_text']),
            safe_get(data, ['담당자 이메일', 'email']),
            safe_get(data, ['연관 제품', 'select', 'name']),
            safe_get(data, ['계약종료일', 'rollup', 'date', 'start']),
            safe_get(data, ['업체 이름', 'title', 0, 'text', 'content'])
        ]
    else:
        print("입력되어 있는 데이터 총 개수는 : ", count_data)

        for A in range(count_data):
            # print(A, "번째 데이터 이식 시작합니다.")

            row_data = []  # 각 행에 대한 데이터 리스트 초기화

            for B in row_name:
                if B in data[A] and data[A][B] is not None:
                    try:
                        if data[A][B]['type'] == "multi_select":
                            if len(data[A][B]['multi_select']) > 0:
                                row_data.append(
                                    safe_get(data[A], [B, 'multi_select', 0, 'name']))
                            else:
                                row_data.append(None)

                        elif data[A][B]['type'] == "rollup":
                            if data[A][B]['rollup']['type'] == "array":
                                if len(data[A][B]['rollup']['array']) > 0:
                                    row_data.append(
                                        safe_get(data[A], [B, 'rollup', 'array', 0, 'select', 'name']))
                                else:
                                    row_data.append(None)

                            elif data[A][B]['rollup']['type'] == "number":
                                row_data.append(
                                    safe_get(data[A], [B, 'rollup', 'number']))

                            elif data[A][B]['rollup']['type'] == "date":
                                temp = data[A], [B, 'rollup', 'date', 'start']
                                temp = pd.to_datetime(temp, utc=True)
                                temp = temp.strftime("%Y-%m-%d")
                                row_data.append(
                                    safe_get(temp))

                        elif data[A][B]['type'] == "last_edited_time":
                            temp = data[A], [B, 'last_edited_time']
                            temp = pd.to_datetime(temp, utc=True)
                            temp = temp.strftime("%Y-%m-%d")
                            row_data.append(
                                safe_get(temp))

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


def check_data(key_to_check, data):

    if data.get(key_to_check) in data:
        temp = data

    else:
        temp = ""

    return temp
