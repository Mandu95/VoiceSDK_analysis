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
