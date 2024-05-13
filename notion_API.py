from notion_client import Client
from notion_client.helpers import collect_paginated_api

import function


class notion_API:

    def __init__(self):

        print("notion api 호출 성공")
        notion_token = "secret_LLThxSNKF5WnG6i6ybJPEZTaGO1oUmhnwVHtz9Dt6PD"
        self.notion = Client(auth=notion_token)  # 내 토큰으로 노션 접근

    def notion_readDatabase(self, notion_DB_Key):
        data_list = []

        if type(notion_DB_Key) is not list:
            print("notion key 1개입니다.")
            try:
                data = collect_paginated_api(
                    self.notion.databases.query, database_id=notion_DB_Key
                )
                data_list.append(data)
            except Exception as e:
                print("notion 데이터베이스 접근 실패", e)
                print(
                    "======================================================================================="
                )

            data = function.notion_dic_to_dataframe(data_list)
            return data

        else:
            for A in range(len(notion_DB_Key)):
                print("호출 DB의 Keyid : ", notion_DB_Key[A])

                try:
                    data = collect_paginated_api(
                        self.notion.databases.query, database_id=notion_DB_Key[A]
                    )
                    data_list.append(data)
                except Exception as e:
                    print("notion 데이터베이스 접근 실패", e)

            data = function.notion_dic_to_dataframe(data_list)
            return data_list

    def extract_properties(self, notion_data):
        notion_data = function.notion_dic_to_dataframe(
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
