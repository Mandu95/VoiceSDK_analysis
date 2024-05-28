import pandas as pd


# notion data를 row_name, Properites, URL 추출해서 저장
def extract_properties_to_array(data):

    # 빈 이중배열 선언
    empty_array = [[] for _ in range(3)]

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


def safe_get(d, keys, default=None):
    """안전하게 중첩된 딕셔너리에서 값을 가져오는 헬퍼 함수"""
    for key in keys:
        try:
            d = d[key]
        except (KeyError, TypeError, IndexError):
            return default  # None으로 반환
    return d


# notion의 날짜 데이터는 ISO 8601 날짜 문자열이기 때문 년/월/일로 변환해주는 함수
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

    return df


# notion properties 속성 고려해서 데이터 불러오는 함수
def get_value_from_property(property):
    """개별 속성에서 값을 추출하는 헬퍼 함수"""
    if property['type'] == "multi_select":
        return [safe_get(property, ['multi_select', X, 'name']) for X in range(len(property['multi_select']))] or None
    elif property['type'] == "rollup":
        return get_rollup_value(property)
    elif property['type'] == "last_edited_time":
        return format_date(safe_get(property, ['last_edited_time']))
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
