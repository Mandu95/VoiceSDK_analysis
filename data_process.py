import notion_DB_call
import mandu_function
import pandas as pd

# notion api 호출해서 DB 연결
nc = notion_DB_call.notion_API()

# 내가 조회하고자 하는 DB 키 정적입력 type = list
all_key = ["69aeff6ca32d4466ad4748dde3939e8b",
           "49e1a704e0ae41679775e9f1194d9068"]

# DB 데이터 추출
data = nc.notion_readDatabase(all_key)

# Dataframe에서 properties 속성만 추출하는 것
data1 = data[0]['properties']


# 표 View 하기 위한 속성 추출
row_name = mandu_function.df_col(data1)

# 값 추출
df = mandu_function.extract_data(data1, row_name)


# data2 = data[1]
# df = mandu_function.connect_db(data2, df)
# print(df[0:1])
# 제품 필터 추출
# goods_filter = mandu_function.extract_goods_item(data)


# database_properties = nc.extract_properties(
#     data)  # dic 형태에서 properties 속성 값만 추출


# count = len(database_properties[0])
# print("DB상에 입력 된 업체 또는 병원 수 :", count)

# for a in range(count):
#     print("병원 또는 업체 : , ", database_properties[0][a]['업체 이름']
#           ['title'][0]['text']['content'])


# status_fliter = []
# for A in range(count):

#     try:
#         if database_properties[0][A]['상태']['status']['name'] is not None:
#             status_fliter.append(
#                 database_properties[0][A]['상태']['status']['name'])

#     except Exception as e:
#         print("Database를 다시 확인하시오, 데이터가 비어서 그럴거에요!")

# status_fliter = mandu_function.find_same_data(status_fliter)


# # 정식, 데모 계약 확인
# contract = 0
# pre_contract = 0

# for C in range(count):

#     try:

#         if database_properties[0][C]['계약구분']['rollup']['array'][0]['select'] is not None:

#             if database_properties[0][C]['계약구분']['rollup']['array'][0]['select']['name'] == "정식":
#                 # print(database_properties[0][C]['업체 이름']
#                 #       ['title'][0]['text']['content'], " ", database_properties[0][C]['계약구분']['rollup']['array'][0]['select']['name'])
#                 contract = contract+1

#             elif database_properties[0][C]['계약구분']['rollup']['array'][0]['select']['name'] == "데모":
#                 # print(database_properties[0][C]['업체 이름']
#                 #       ['title'][0]['text']['content'], " ", database_properties[0][C]['계약구분']['rollup']['array'][0]['select']['name'])
#                 pre_contract = pre_contract+1

#     except Exception as e:
#         print("데이터가 없는 병원, 업체 : , ", database_properties[0][C]['업체 이름']
#               ['title'][0]['text']['content'])
#         print("데이터 확인: , ",
#               database_properties[0][C]['계약구분']['rollup']['array'])


# print("정식계약수 : ", contract)
# print("데모계약수 : ", pre_contract)
